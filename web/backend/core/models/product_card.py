from collections import OrderedDict
import json
import random
import math
import re

from django.db.models import Max, Manager
from django.db import models
from django.db import IntegrityError
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.conf import settings

#from polymorphic.models import PolymorphicModel
#from polymorphic.managers import PolymorphicManager


from ..db.shop import OfferIdentifier
from ..db.shop import OfferPage
from ..db.image import Image
from ..db.base import Weighable, Dimensional, Named, TimeStamped, Orderable
from ..db import Orderable
from ..utils import disallowed_before_creation, DisallowedBeforeCreationException,\
    md5_file_checksum


class PublicProductCardManager(Manager):

    def get_queryset(self):
        return super(PublicProductCardManager, self).get_queryset().\
            filter(is_in_stock=True)


class ProductCard(OfferPage, Image, Weighable, Dimensional):

    class Meta:
        abstract = True
        pass

    # Custom managers
    public = PublicProductCardManager()

    # KEY-CLASSES
    attributevalues_relation_class = None
    attributevalue_class = None
    product_model_class = None

    # KEYS AND M2M
    attribute_values = None
    product_model = None

    # Image
    upload_image_to = None
    image_key_attribute = 'get_image_name'

    # Search
    update_search = False

    vendor_code = models.CharField(
        verbose_name="Артикул",
        max_length=1024,
        db_index=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-_a-z\d]+$',
                message='vendor_code valid error',
            )
        ]
    )

    product_type = models.CharField(
        verbose_name="Тип продукта",
        max_length=128,
        choices=(
            ("", "Не задано"),
            ("CUBE", "CUBE"),
            ("BAG", "BAG"),
            ("SUITCASE", "SUITCASE"),
            ("PURSE", "PURSE")
        ),
        default="",
        blank=True,
    )

    @property
    def data_for_delivery(self):
        result = {
            "product_type": self.product_type,
            "price": self.price,
            "purchase_price": self.purchase_price,
            "vendor": self.vendor
        }
        if self.weigh:
            result['weigh'] = math.ceil(self.weigh/1000)
        if self.dimensions:
            result['dimensions'] = self.dimensions
        return result

    product_aditional_image_class = None

    @property
    def get_image_name(self):
        return self.model.replace('/', '-')

    model = models.CharField(
        verbose_name="Модель",
        max_length=1024,
        db_index=True
    )

    def get_url(self):
        return self.slug

    @disallowed_before_creation
    def add_attribute_value(self, attribute_value_instance):
        if attribute_value_instance.pk:
            try:
                self.attributevalues_relation_class.objects.create(
                    product=self,
                    attribute_value=attribute_value_instance
                )
            except IntegrityError:
                pass
        else:
            raise DisallowedBeforeCreationException('attributes_value_instance must be creatied')

    @disallowed_before_creation
    def del_attribute_value(self, attribute_value_instance):
        if attribute_value_instance.pk:
            try:
                self.attributevalues_relation_class.objects.get(
                    product=self,
                    attribute_value=attribute_value_instance
                ).delete()
            except ObjectDoesNotExist:
                pass
        else:
            raise DisallowedBeforeCreationException('attribute_value_instance must be creatied')

    @disallowed_before_creation
    def del_attribute_values(self, values_list):
        relations_to_delete = self.attributevalues_relation_class.objects.filter(
            product=self,
            attribute_value__in=values_list
        ).delete()

    @disallowed_before_creation
    def clear_attribute_value(self):
        self.attributevalues_relation_class.objects.filter(
            product=self
        ).delete()

    def set_int_value(self, value, attribute):
        value = int(value)
        related_products_count = self.attributevalues_relation_class.objects.filter(
            attribute_value__in=self.attribute_values.filter(attribute=attribute)
        ).count()
        attribute_key = attribute.key.split("__")[-1]
        slug = "__int__{value}__{key}".format(
            value=value,
            key=attribute_key
        )
        value_name = "{value} {unit}".format(
            value=value,
            unit=attribute.unit
        )
        if related_products_count == 1:
            # Перезапись
            attribute_value = self.attribute_values.get(attribute=attribute)
            attribute_value._int_value = value
            attribute_value.name = value_name
            attribute_value.slug = slug
            attribute_value.save()
        else:
            # Создание
            try:
                attribute_value = self.attributevalue_class.objects.get(
                    slug=slug
                )
            except ObjectDoesNotExist:
                attribute_value = self.attributevalue_class(
                    attribute=attribute,
                    attribute_type=attribute.attribute_type,
                    slug=slug,
                    name=value_name,
                    _int_value=value
                )
                attribute_value.save()
            self.add_attribute_value(attribute_value)

    @property
    @disallowed_before_creation
    def attributes(self):
        result = OrderedDict()
        for av in self.attribute_values.select_related().order_by(
            '-attribute__order',
            '-order'
        ):
            result[av.attribute] = result.get(
                av.attribute,
                []
            ) + [av]
        return result

    @property
    @disallowed_before_creation
    def additional_images(self):
        return self.product_aditional_image_class.objects.filter(
            product=self
        ).order_by('order', 'id')

    @property
    def public_id(self):
        return self.get_public_id()

    @property
    def has_photo(self):
        return self.image != self.image.field.default

    @property
    @disallowed_before_creation
    def photo_checksums(self):
        checksums = set()
        images = self.product_aditional_image_class.objects.filter(
            product=self,
        )
        if self.has_photo:
            checksums.add(md5_file_checksum(self.image.path))
        for image in images:
            checksums.add(md5_file_checksum(image.image.path))
        return checksums

    def generate_image_from_main(self):
        max_order = self.product_aditional_image_class.objects.filter(
            product=self,
        ).aggregate(Max('order'))['order__max']
        if max_order is None:
            max_order = 0
        else:
            max_order += 1
        instance = self.product_aditional_image_class(
            product=self,
            image=self.image,
            order=max_order,
        )
        instance.save()

    def replace_main_image_by_file(self, image_file):
        self.generate_image_from_main()
        self.image = image_file
        update_search = not settings.DEBUG
        self.save(update_search=update_search)

    def replace_main_image_by_additional(self, image_id):
        try:
            instance = self.product_aditional_image_class.objects.get(id=image_id)
            self.generate_image_from_main()
            self.image = instance.image
            update_search = not settings.DEBUG
            self.save(update_search=update_search)
            instance.delete()
        except self.product_aditional_image_class.DoesNotExist:
            pass

    def add_photo(self, filename):
        fp = open(filename, 'rb')
        img_file = File(fp)
        if self.has_photo:
            instance = self.product_aditional_image_class(
                product=self,
                image=img_file,
            )
            instance.save()
        else:
            self.image = img_file
            self.save()
        fp.close()

    def get_public_id(self):
        msg = "Method get_public_id() must be implemented by subclass: `{}`"
        raise NotImplementedError(msg.format(self.__class__.__name__))

    def get_scoring(self):
        scoring = 0
        if self.has_photo:
            if self.scoring != 0:
                scoring = self.scoring
            else:
                scoring = random.randint(100, 150)
        return scoring

    def get_image_url(self):
        return self.image.url

    def get_modifications(self):
        if self.product_model is not None:
            return self.product_model.products.exclude(id=self.id)
        return []

    @property
    def modifications(self):
        return self.get_modifications()

    @property
    def html_free_description(self):
        return re.sub("<.*?>", "", self.description).strip()

    def __str__(self):
        return 'Product card: {0}'.format(self.slug)

    def save(self, update_search=False, *args, **kwargs):
        self.update_search = update_search
        self.scoring = self.get_scoring()

        super(ProductCard, self).save(*args, **kwargs)


class ProductAditionalImage(Image, Orderable):

    class Meta:
        abstract = True

    upload_image_to = None
    image_key_attribute = 'get_image_name'

    product = None

    @property
    def get_image_name(self):
        return self.product.model.replace('/', '-')


class ProductModel(Named):

    class Meta:
        abstract = True


class ProductVideoReview(TimeStamped, Orderable):

    class Meta:
        abstract = True

    product = None

    youtube_code = models.CharField(
        db_index=True,
        max_length=64,
        blank=True,
        verbose_name="код Youtube"
    )

    @property
    def url(self):
        return "https://www.youtube.com/watch?v={code}".format(self.code)


class ProductCardReview(TimeStamped):

    class Meta:
        abstract = True
        ordering = ['-created_at']

    user = None
    product = None

    RATING_CHOICES = (
        (10, '10'),
        (9, '9'),
        (8, '8'),
        (7, '7'),
        (6, '6'),
        (5, '5'),
        (4, '4'),
        (3, '3'),
        (2, '2'),
        (1, '1'),
        (0, '0')
    )

    REVIEW_STATUSES = (
        ("новый", "Новый"),
        ("одобрен", "Одобрен"),
        ("отклонен", "Отклонен"),
    )

    status = models.CharField(
        max_length=32,
        verbose_name='статус отзыва',
        choices=REVIEW_STATUSES,
        default=REVIEW_STATUSES[0][0]
    )

    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES,
        default=0
    )

    content = models.TextField(
        verbose_name="Review text",
        blank=False
    )
    
    def __str__(self):
        return "{0} - User: {1}".format(
            self.product.id,
            self.user.id
        )
