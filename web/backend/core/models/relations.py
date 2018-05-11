from django.db import models
from django.core.exceptions import ValidationError

from .attribute_value import AttributeType


class CategoryNodeAttributeValueRelation(models.Model):

    """
    Промежуточная таблица для m2m-связи между CategoryNode
    и AttributeValue
    """
    class Meta:
        abstract = True
        unique_together = (('category', 'attributevalue'))

    category = None
    value = None

    def __init__(self, *args, **kwargs):
        super(CategoryNodeAttributeValueRelation, self).__init__(*args,
                                                                 **kwargs)

    def clean(self):
        """
        TODO доделать
          (Вероятно количество связей у категории должно быть равно её уровню,
           Но проблема в том, что это вычисляется в обратную сторону)
          * Не может быть связей с root категорией(у которой нулевой уровень);
        """
        pass


class CategoryNodeInputRelation(models.Model):

    """
    Промежуточный класс для m2m-связи между CategoryNode
    и входными узлами
    """
    class Meta:
        abstract = True

    input_node = None
    output_node = None
    group = None
    added_attribute_value = None

    def __init__(self, *args, **kwargs):
        super(CategoryNodeInputRelation, self).__init__(*args,
                                                        **kwargs)


class CategoryNodeAdditionalRelation(models.Model):

    """
    Промежуточный класс для m2m-связи между CategoryNode
    и дополнительными узлами дерева
    """
    class Meta:
        abstract = True

    input_node = None
    output_node = None

    def __init__(self, *args, **kwargs):
        super(CategoryNodeAdditionalRelation, self).__init__(*args,
                                                             **kwargs)


class ProductCardAttributeValueRelation(models.Model):

    """
    Промежуточный класс для m2m-связи между ProductCart
    и AttributeValue

    Механика:
      * не может быть одновременно у 1ого товара True и False
      * не может быть для Choice для одного товара несколько значений
      * не может быть больше одного численного значения
      ------------------------------------------------------------------------
      Выше можно обощить, не может быть больше одной связи, между атрибутом и
      продуктом, если тип атрибута Bool, Choice и Integer
    """
    class Meta:
        abstract = True
        unique_together = (('product', 'attribute_value'))

    product = None
    attribute_value = None

    def clean(self):
        # Не может быть больше одной связи, между атрибутом и
        # продуктом, если тип атрибута Bool, Choice и Integer
        if self.attribute_value.attribute_type in {
            AttributeType.Bool,
            AttributeType.Choice,
            AttributeType.Integer
        }:
            qs = self.__class__.objects.filter(
                product=self.product,
                attribute_value__attribute=self.attribute_value.attribute
            )
            if qs:
                msg = "Valid Error in {0}".format(self.__class__)
                raise ValidationError(msg)


class AttributeValueFilterRelation(models.Model):

    """
    Класс промежуточной таблицы, обеспечивающей M2M-свзязь,
    между Attribute и AttributeValue, описывающей связь значений атрибутов с 
    атрибутами, которые нужно отобразить в фильтрации
    """
    class Meta:
        abstract = True
        unique_together = (('attribute', 'attribute_value'))

    attribute = None
    attribute_value = None
