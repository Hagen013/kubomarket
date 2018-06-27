from unidecode import unidecode
import json

from django.db import models
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify
from djchoices import DjangoChoices, ChoiceItem

from ..db import WebPage, DisplayableManager, Named, Describable
from ..db import Orderable
from ..utils import disallowed_before_creation


class AttributeType(DjangoChoices):

    Choice = ChoiceItem(1, 'Choice')
    MultipleChoice = ChoiceItem(2, 'MultipleChoice')
    Integer = ChoiceItem(3, 'Integer')
    Bool = ChoiceItem(4, 'Bool')
    Color = ChoiceItem(5, 'Color')


class Attribute(Named, Describable, Orderable):

    class Meta:
        abstract = True
        verbose_name = 'атрибут'
        verbose_name_plural = 'атрибуты'

    # Класс значений, используется для reverse-lookup'a
    # TODO возможно переделать на:
    #   * attribute_value
    #   * attribute_group
    value_class = None

    # FIELDS
    # pk группы атрибута, может быть равна None
    category_node_group = None

    key = models.CharField(
        max_length=512,
        verbose_name='ключ',
        unique=True,
        validators=[RegexValidator(
            regex='^[-_a-z\d]+$',
            message='Недопустимые символы для ключа атрибута',
            code='nomatch')
        ]
    )

    attribute_type = models.PositiveSmallIntegerField(
        choices=AttributeType.choices,
        db_index=True,
        verbose_name='тип атрибута'
    )

    is_default_filter = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="фильтр по умолчанию"
    )

    unit = models.CharField(
        blank=True,
        max_length=256,
        verbose_name='Единица измерения'
    )


    @disallowed_before_creation
    def add_value(self, name, slug, value=None):
        return self.value_class.objects.create_value(
            attribute=self,
            name=name,
            value=value,
            slug=slug,
        )

    @property
    def values(self):
        return self.value_class.objects.filter(attribute=self)

    @property
    def values_json(self):
        values = self.value_class.objects.filter(attribute=self).values("name", "id")
        values = list(map(lambda x: {"name": x["name"], "id": x["id"], "active": False}, values))
        return json.dumps(values)

    def __init__(self, *args, **kwargs):
        super(Attribute, self).__init__(*args, **kwargs)
        # Сохранение исходного типа атрибута (изменение запрещено)
        self.__original_attribute_type = self.attribute_type

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        # После создания атрибута запрещено изменять его тип
        if self.id and self.__original_attribute_type != self.attribute_type:
            raise models.FieldError("Can`t change attribute_type after create")
        self.__original_attribute_type = self.attribute_type
        super(Attribute, self).save(force_insert,
                                    force_update,
                                    *args,
                                    **kwargs)

    def __str__(self):
        return self.name

    def clean(self):
        """
        Основная логика на релейшн классах
        """
        pass
