from math import inf

from django.db import models
from django_hosts.resolvers import reverse

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
    upload_image_to = 'images/Cubes_additional'

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

    upload_image_to = 'images/Cubes'

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

        return reverse('product', kwargs={'slug': self.slug}, host="Cubes")

    @disallowed_before_creation
    def get_public_id(self):
        return self.public_id_prefix + str(self.id)

    def get_meta_title(self):
        return "{0} — купить недорого в интернет-магазине PresidentCubes".format(
            self.name
        )

    def get_meta_description(self):
        return "{0} купить в интернет-магазине сумок и рюкзаков PresidentCubes. \
    Недорогие цены, обширный каталог товаров от производителей. Доставка по Москве и России. \
    ".format(
            self.name
        )

    def get_meta_keywords(self):
        return self.name.lower()

    @disallowed_before_creation
    def get_product_type(self):
        tips_values = sorted(self.attribute_values.filter(attribute__key='tip'),
                             key=lambda x: {'chemodany': 1,
                                            'sumki': 2,
                                            'ryukzaki': 3,
                                            'meshki': 4,
                                            'koshelki': 5,
                                            'penaly': 6}.get(x.value, inf)
                             )
        if len(tips_values):
            return {
                "chemodany": "SUITCASE",
                "sumki": "BAG",
                "meshki": "BAG",
                "ryukzaki": "BACKPACK",
                "koshelki": "PURSE",
                "penaly": "PURSE",
            }.get(tips_values[0].value, "")
        else:
            return ""

    @property
    def yml_product_type(self):
        if (self.product_type in {"BAG", "BACKPACK", "PURSE"}) and \
                (self.price - self.purchase_price >= 2000):
            return {
                "BAG": 6,
                "BACKPACK": 7,
                "PURSE": 8
            }[self.product_type]

        else:

            return {
                "SUITCASE": 2,
                    "BAG": 3,
                    "BACKPACK": 4,
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
        return reverse('category', kwargs={'url': self.url}, host='Cubes')

    def get_meta_title(self):
        return "Купить {0}{1} — недорого в интернет-магазине PresidentCubes".format(
            self.title[:1].lower(),
            self.title[1:]
        )

    def get_meta_description(self):
        return "Купить {0}{1} в интернет-магазине сумок и рюкзаков PresidentCubes. \
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
