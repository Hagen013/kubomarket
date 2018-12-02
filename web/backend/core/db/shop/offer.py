from django.db import models

from ..base import Named, Describable
from .offer_identifier import OfferIdentifier


class BaseOffer(models.Model):

    """
    Абстрактный класс предложения, производного от предложения.
    Имеет поле цены, в виде числа. Имеет ряд дополнительных полей.

    old_price - старая цена

    model - модель
    vendor - производитель

    is_in_stock - в продаже
    is_sale - в распродаже (вычисляется автоматически из old_price)
    is_new - новинка
    is_bestseller - бестселлер
    """
    class Meta():
        abstract = True
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    # Offer price
    price = models.PositiveIntegerField(
        verbose_name='Цена',
        blank=False
    )

    purchase_price = models.PositiveIntegerField(
        verbose_name='Цена закупки',
        blank=False,
        default=0
    )

    old_price = models.PositiveIntegerField(
        verbose_name='Старая цена',
        default=0
    )

    vendor = models.CharField(
        max_length=255,
        verbose_name='Производитель'
    )

    # хранится ли на складе в принципе
    stored = models.BooleanField(
        verbose_name='был закуплен',
        default=False
    )

    #
    amount = models.PositiveIntegerField(
        verbose_name='количество на складе',
        default=0
    )

    is_in_stock = models.BooleanField(
        default=False,
        verbose_name='В наличии'
    )
    is_sale = models.BooleanField(
        default=False,
        editable=False,
        verbose_name='В распродаже'
    )
    is_new = models.BooleanField(
        default=False,
        verbose_name='Новинка'
    )
    is_bestseller = models.BooleanField(
        default=False,
        verbose_name='Бестселлер'
    )
    is_recomended = models.BooleanField(
        default=False,
        verbose_name='Рекомендуемый'
    )
    is_displayed_in_selections = models.BooleanField(
        default=False,
        verbose_name='Отображаемый в коллекциях'
    )
    recently_bought = models.BooleanField(
        default=False,
        verbose_name='Куплен недавно'
    )
    # Возвращает полный адрес офера в Django

    @property
    def offer_identifier(self):
        return OfferIdentifier(self._meta.app_label,
                               self._meta.model_name,
                               self.pk)

    def save(self, *args, **kwargs):
        if not(self.old_price is None):
            self.is_sale = self.price < self.old_price
        super(BaseOffer, self).save(*args, **kwargs)


class Offer(BaseOffer, Named, Describable):

    class Meta():
        abstract = True
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
