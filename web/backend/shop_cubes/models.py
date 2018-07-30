from math import inf

from django.db import models
from django.urls import reverse

from mptt.models import TreeForeignKey

from core.models import (CategoryNodeGroup,
                         Attribute,
                         AttributeValue,
                         CategoryNode,
                         ProductCard,
                         ProductModel,
                         ProductAditionalImage,
                         CategoryNodeInputRelation,
                         CategoryNodeAdditionalRelation,
                         CategoryNodeAttributeValueRelation,
                         CategoryNodeOutdatedUrl,
                         ProductCardAttributeValueRelation,
                         AttributeValueFilterRelation)

from core.utils import disallowed_before_creation, DisallowedBeforeCreationException


class CubesCategoryNodeGroup(CategoryNodeGroup):
    pass


class CubesAttributeValueFilterRelation(AttributeValueFilterRelation):

    attribute = models.ForeignKey(
        "CubesAttribute",
        on_delete=models.CASCADE,
        db_index=True
    )

    attribute_value = models.ForeignKey(
        "CubesAttributeValue",
        on_delete=models.CASCADE,
        db_index=True
    )


class CubesAttributeValue(AttributeValue):

    attribute_filter_relation_class = CubesAttributeValueFilterRelation

    attribute = models.ForeignKey(
        'CubesAttribute',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_index=True,
        related_name='values'
    )

    filters = models.ManyToManyField(
        'CubesAttribute',
        blank=True,
        related_name='filter_values',
        through=attribute_filter_relation_class   
    )


class CubesAttribute(Attribute):

    value_class = CubesAttributeValue

    category_node_group = models.ForeignKey(
        'CubesCategoryNodeGroup',
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True,
        default=None
    )


class CubesProductCardAttributeValueRelation(ProductCardAttributeValueRelation):

    product = models.ForeignKey(
        'CubesProductCard',
        on_delete=models.CASCADE,
        db_index=True
    )
    attribute_value = models.ForeignKey(
        'CubesAttributeValue',
        on_delete=models.CASCADE,
        db_index=True
    )


class CubesProductAdditionalImage(ProductAditionalImage):
    upload_image_to = 'images/cubes_additional'

    product = models.ForeignKey(
        'CubesProductCard',
        on_delete=models.CASCADE,
        db_index=True,
    )


class CubesProductModel(ProductModel):
    pass


class CubesProductCard(ProductCard):

    attributevalues_relation_class = CubesProductCardAttributeValueRelation
    attributevalue_class = CubesAttributeValue
    product_aditional_image_class = CubesProductAdditionalImage
    product_model_class = CubesProductModel

    public_id_prefix = 'b-247-'

    upload_image_to = 'images/cubes'

    attribute_values = models.ManyToManyField(
        attributevalue_class,
        blank=True,
        related_name='referring_nodes',
        through=attributevalues_relation_class
    )

    product_model = models.ForeignKey(
        CubesProductModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    def get_absolute_url(self):

        return reverse('shop:product', kwargs={'slug': self.slug})

    @disallowed_before_creation
    def get_public_id(self):
        return self.vendor_code.split('-')[-1]

    @property
    def public_id(self):
        return self.get_public_id()

    def get_meta_title(self):
        if len(self._meta_title) == 0:
            return "{0} — купить кубики Рубика недорого в интернет-магазине Kubomarket.Ru".format(
                self.name
            )
        else:
            return self._meta_title

    def get_meta_description(self):
        if len(self._meta_description) == 0:
            return "{0} — купить в интернет-магазине кубиков Рубика Kubomarket.Ru. Недорогие цены, обширный каталог товаров от производителей. Доставка по Москве и России.".format(
                self.name
            )
        else:
            return self.meta_description

    def get_meta_keywords(self):
        return self.name.lower()

    @disallowed_before_creation
    def get_product_type(self):
        return "CUBE"

    @property
    def yml_product_type(self):
        if (self.product_type in {"BAG", "CUBE", "PURSE"}) and \
                (self.price - self.purchase_price >= 2000):
            return {
                "BAG": 6,
                "CUBE": 7,
                "PURSE": 8
            }[self.product_type]

        else:

            return {
                "SUITCASE": 2,
                    "BAG": 3,
                    "CUBE": 4,
                    "PURSE": 5
            }[self.product_type]

    def save(self, update_product_type=True, *args, **kwargs):
        if update_product_type:
            try:
                self.product_type = self.get_product_type()
            except DisallowedBeforeCreationException:
                self.product_type = ""

        super(CubesProductCard, self).save(*args, **kwargs)


class CubesCategoryNodeInputRelation(CategoryNodeInputRelation):

    class Meta:
        unique_together = (("input_node", "output_node"),)

    node_class = "CubesCategoryNode"

    input_node = models.ForeignKey(
        node_class,
        on_delete=models.CASCADE,
        db_index=True,
        blank=True,
        related_name='input_node_reverse',
    )
    output_node = models.ForeignKey(
        node_class,
        on_delete=models.CASCADE,
        db_index=True,
        blank=True,
        related_name='output_node_reverse',
    )
    group = models.ForeignKey(
        'CubesCategoryNodeGroup',
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True,
        default=None
    )
    added_attribute_value = models.ForeignKey(
        'CubesAttributeValue',
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True,
        default=None
    )


class CubesCategoryNodeAdditionalRelation(CategoryNodeAdditionalRelation):

    node_class = "CubesCategoryNode"


class CubesCategoryNodeAttributeValueRelation(CategoryNodeAttributeValueRelation):

    category = models.ForeignKey(
        'CubesCategoryNode',
        on_delete=models.CASCADE,
        db_index=True,
    )

    attributevalue = models.ForeignKey(
        'CubesAttributeValue',
        on_delete=models.CASCADE,
        db_index=True,
    )


class CubesCategoryNodeOutdatedUrl(CategoryNodeOutdatedUrl):

    node = models.ForeignKey(
        'CubesCategoryNode',
        on_delete=models.CASCADE,
        db_index=True,
    )


class CubesCategoryNode(CategoryNode):

    inputs_relation_class = CubesCategoryNodeInputRelation
    related_relation_class = CubesCategoryNodeAdditionalRelation
    attributevalues_relation_class = CubesCategoryNodeAttributeValueRelation
    outdated_url_class = CubesCategoryNodeOutdatedUrl

    product_card_class = CubesProductCard

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        db_index=True,
        related_name='childs'
    )

    attribute_values = models.ManyToManyField(
        'CubesAttributeValue',
        blank=True,
        related_name='categories',
        through=attributevalues_relation_class
    )

    inputs = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='outputs',
        through=inputs_relation_class,
    )

    related_nodes = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='referring_nodes',
        through=related_relation_class,
    )

    def get_absolute_url(self):
        return reverse('shop:category', kwargs={'url': self.url})

    def get_meta_title(self):
        return "Купить {0}{1} — недорого в интернет-магазине www.kubomarket.ru".format(
            self.title[:1].lower(),
            self.title[1:]
        )

    def get_meta_description(self):
        return "Купить {0}{1} в интернет-магазине сумок и рюкзаков www.kubomarket.ru. \
    Недорогие цены, обширный каталог товаров от производителей. Доставка по Москве и России. \
    ".format(
            self.title[:1].lower(),
            self.title[1:]
        )

    def get_meta_keywords(self):
        return self.title.lower()


class CubesImagesRegisterRecord(models.Model):

    class Meta:
        unique_together = (("product", "url"),)

    product = models.ForeignKey(
        CubesProductCard,
        on_delete=models.CASCADE,
        related_name='images_register_records'
    )

    url = models.CharField(
        db_index=True,
        unique=False,
        max_length=1024,
        verbose_name='url'
    )
