from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from ..db import WebPage, DisplayableManager, Named, Describable
from .attribute import AttributeType


class AttributeValueManager(models.Manager):

    def create_value(self, attribute, name, slug, description, value=None):
        """
        """
        attribute_type = attribute.attribute_type
        if not value:
            if attribute_type in {1, 2}:
                name = str(name)
                value = str(slug)
            elif attribute_type == 3:
                name = str(name)
                value = int(name)
            elif attribute_type == 4:
                name = str(name)
                value = bool(name)
            elif attribute_type == 5:
                raise TypeError("Сolor attribute requires a value parameter")

        instance = self.model(
            name=name,
            attribute=attribute,
            attribute_type=attribute_type,
            slug=slug,
            description=description,
        )
        instance.value = value
        instance.full_clean()
        instance.save()
        return instance


class AttributeValue(Named, Describable):

    """
    Таблица значений атрибутов:
    Имеет поля:
        * attribute - атрибут (должен быть переопределен в дочернем классе)
        * attribute_type - денормализованное поле attribute

        * value - вычисляемое значение

        [ПОЛЯ ЗНАЧЕНИЙ]
        * str_value - строковое значение (attribute_type Choice, MultipleChoice, Color)
        * bool_value - булево значение (attribute_type Boolean)
        * int_value - целочисленное значение (attribute_type Integer)

    Механика:
        * невозможно изменить тип атрибута после создания
        * нельзя создавать больше 2-ух булевых полей на атрибут
        * choice_value - уникален для атрибута
        * только одно из значений (str|int|bool)_value должно быть использовано
        для сериализации значения
    """
    class Meta:
        abstract = True
        verbose_name = 'Значение атрибута'
        verbose_name_plural = 'Значения атрибутов'
        unique_together = (("attribute",
                            "_str_value",
                            "_int_value",
                            "_bool_value",
                            ),)

    attribute = None
    objects = AttributeValueManager()

    attribute_type = models.PositiveSmallIntegerField(
        choices=AttributeType.choices,
        db_index=True,
        verbose_name='типа атрибута'
    )

    # Колонки значений
    _str_value = models.CharField(
        verbose_name="Значение ",
        max_length=512,
        default=None,
        db_index=True,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[-_a-z\d]+$',
                message='slug valid error',
            )
        ]
    )
    _int_value = models.IntegerField(
        verbose_name="Значение",
        default=None,
        db_index=True,
        null=True,
        blank=True
    )
    _bool_value = models.NullBooleanField(
        verbose_name="Значение",
        default=None,
        db_index=True,
        null=True,
        blank=True,

    )

    slug = models.CharField(
        max_length=256,
        blank=False,
        unique=True,
        db_index=True,
        verbose_name='slug',
        validators=[
            RegexValidator(
                regex=r'^[-_a-z\d]+$',
                message='slug valid error',
            )
        ]
    )

    order = models.PositiveIntegerField(
        verbose_name="Порядок",
        default=0,
    )

    __attr_type_value_field_mapping = {
        1: '_str_value',
        2: '_str_value',
        3: '_int_value',
        4: '_bool_value',
        5: '_str_value'
    }

    @property
    def _value_field(self):
        return self.__attr_type_value_field_mapping[self.attribute_type]

    @property
    def value(self):
        if self.attribute_type:
            return getattr(self, self._value_field)
        else:
            raise AttributeError("attribute_type is not defined")

    @property
    def has_description(self):
        return len(self.description) > 0

    @value.setter
    def value(self, value):
        if self.attribute_type:
            setattr(self, self._value_field, value)
        else:
            raise AttributeError("attribute_type is not defined")

    def __str__(self):
        return str(self.value)

    def clean(self):
        # attribute_type должен совпадать с родительским
        if self.attribute_type != self.attribute.attribute_type:
            msg = "attribute_type is not equal attribute.attribute_type"
            raise ValidationError(msg)
        # только одно <_str|_bool|_int>_value должно быть не None
        # в зависимости от attribute_type
        if self.attribute_type == AttributeType.Bool:
            if not all((self._int_value is None,
                        self._str_value is None,
                        self._bool_value is not None)):
                raise ValidationError('AttributeType.Bool')

        if self.attribute_type == AttributeType.Integer:
            if not all((self._int_value is not None,
                        self._str_value is None,
                        self._bool_value is None)):
                raise ValidationError('AttributeType.Integer')

        if self.attribute_type in {AttributeType.Choice,
                                   AttributeType.MultipleChoice,
                                   AttributeType.Color}:

            if not all((self._int_value is None,
                        self._str_value is not None,
                        self._bool_value is None)):
                raise ValidationError('AttributeType.Choice')
