import xml.etree.ElementTree as ET
from random import randint
import requests

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from django.contrib.auth import get_user_model

from core.db.base import TimeStamped
from core.utils import MailSender
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from jsonschema import validate as jsonschema_validate
from jsonschema.exceptions import ValidationError as JsonSchemaValidationError

User = get_user_model()

MERCHANT_ID = settings.MERCHANT_ID
MERCHANT_LOGIN = settings.MERCHANT_LOGIN
MERCHANT_PASSWORD = settings.MERCHANT_PASSWORD
XML_FORMAT = 3
API_URL = "https://payments.demo.paysecure.ru/orderstate/orderstate.cfm"


class Order2(TimeStamped):

    class Meta():
        verbose_name = 'Заказ2'
        verbose_name_plural = 'Заказы2'

    def __init__(self, *args, **kwargs):
        super(Order2, self).__init__(*args, **kwargs)
        # Взятие исходного состояния, чтобя при сохранении,
        # в засисимости от его изменение отправиь уведомления etc
        self.__original_state = self.state

    data = JSONField()
    EMAIL_REGEXP = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    ORDER_DATA_JSONSCHEMA = {
        "type": "object",
        "properties": {
            "geo": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "code": {"type": "string", "pattern": "^([0-9]{13})|([0-9]{17})|([0-9]{19})$"}
                },
                "required": ["city", "code"],
                "additionalProperties": False,
            },
            "customer": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string",
                              "pattern": "(^$)|({EMAIL_REGEXP})".format(EMAIL_REGEXP=EMAIL_REGEXP)},
                    "phone": {"type": "string", "pattern": "^([0-9]{10})$"},
                    "address": {"type": "string"},
                },
                "required": ["name", "email", "phone", "address"],
                "additionalProperties": False,
            },
            "delivery": {
                "type": "object",
                "properties": {
                    "is_mod_selected": {"type": "boolean"},
                    "mod": {
                        "type": "object",
                        "properties": {
                            "type": {"type": ["string", "null"],
                                     "pattern": "^(curier|delivery_points|postal_service)"},
                            "code": {"type": ["string", "null"],
                                     "pattern": "^([-_a-zA-Z0-9]+)__(sdek_point|pick_point_point)$"},
                            "price": {"type": ["integer", "null"], "minimum": 0}

                        },
                        "required": ["type", "code", "price"],
                        "additionalProperties": False,
                    }
                },
                "required": ["is_mod_selected", "mod"],
                "additionalProperties": False,
            },
            "payment": {
                "type": "object",
                "properties": {
                    "mod": {
                        "type": "string",
                        "pattern": "^(cash|card_upon_receipt|card)$"
                    }
                },
                "required": ["mod"],
                "additionalProperties": False,
            },
            "cart": {
                "type": "object",
                "properties": {
                    "total_price": {"type": "integer", "minimum": 0},
                    "items": {
                        "type": "object",
                        "patternProperties": {
                            "^[-_a-z]+__[-_a-z]+__[\d]+$": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "price": {"type": "integer", "minimum": 0},
                                    "quantity": {"type": "integer", "minimum": 0},
                                    "total_price": {"type": "integer", "minimum": 0},
                                    "image": {"type": "string"},
                                    "vendor_code": {"type": "string"},
                                    "url": {"type": "string"},
                                },
                                "required": ["name", "price", "quantity", "total_price", "image", "url"],
                                "additionalProperties": False,
                            },
                        }

                    }

                },
                "required": ["total_price", "items"],
                "additionalProperties": False,
            }
        },
        "required": ["geo", "customer", "delivery", "payment", "cart"],
        "additionalProperties": False,
    }
    manager_notes = models.TextField(
        max_length=2000,
        verbose_name='Служебные заметки',
        blank=True
    )

    ORDER_STATE = (
        ("новый", "Новый"),
        ("недозвон", "Недозвон"),
        ("доставка", "Доставка"),
        ("согласован", "Согласован"),
        ("выполнен", "Выполнен"),
        ("отменён", "Отменён"),
        ("отменён: недозвон", "Отменён: недозвон"),
    )
    state = models.CharField(
        max_length=100,
        verbose_name='Состояние заказа',
        choices=ORDER_STATE,
        default=ORDER_STATE[0][0]
    )

    ORDER_SOURCE = (
        ('cart', 'Корзина'),
        ('callback', 'Обратный звонок'),
        ('product-page', 'Страница товара')
    )
    source = models.CharField(
        max_length=128,
        verbose_name='Источник заказа',
        choices=ORDER_SOURCE,
        default=ORDER_SOURCE[0][0],
    )

    assist_key = models.CharField(
        max_length=128,
        default=0,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='vendor_code valid error',
            )
        ]
    )

    assist_status = models.CharField(
        max_length=64,
        default="",
        blank=True,
        choices=(
            ("", ""),
            ("in_process", "in_process"),
            ("approved", "approved"),
        )
    )

    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def clean(self):
        try:
            jsonschema_validate(self.data, self.ORDER_DATA_JSONSCHEMA)
        except JsonSchemaValidationError as e:
            raise ValidationError(message=e.message)

    @property
    def total_price(self):
        return sum((
            self.data['delivery']['mod']['price'] and int(self.data['delivery']['mod']['price']) or 0,
            int(self.data['cart']['total_price'])
        ))

    @property
    def beautify_delivery_mod(self):
        return {
            "curier": "Доставка курьером",
            "delivery_points": "Доставка в пункт выдачи",
            "postal_service": "Доставка Почтой России",
        }[self.data['delivery']['mod']["type"]]

    def present_account(self):
        email = self.data.get('customer').get('email')
        if settings.DEBUG:
            URL = "http://localhost:8000"
        else:
            URL = "https://kubomarket.ru"

        if email:
            MailSender(
                "Оплата заказа #{id}".format(id=self.id),
                "mail_templates/present_account.html",
                email,
                context={
                    "order": self,
                    "URL": URL
                }
            ).send_mail()
            self.assist_status = "in_process"
        else:
            raise AttributeError("For present account required email.")

    def refresh_payment_status(self):
        response = requests.post(
            API_URL,
            data={
                "Merchant_ID": MERCHANT_ID,
                "Login": MERCHANT_LOGIN,
                "Password": MERCHANT_PASSWORD,
                "Format": XML_FORMAT,
                "Ordernumber": str(self.id)
            }
        )
        result = ET.ElementTree(ET.fromstring(response.text))
        is_approved = any((os.text == "Approved" for os in result.findall("order/orderstate")))
        if is_approved:
            self.assist_status = "approved"
        return self.assist_status

    def __str__(self):
        return "Заказ №{0}".format(str(self.id))

    def save(self, *args, **kwargs):
        is_new = not self.id
        if is_new:
            self.assist_key = "".join((str(randint(0, 9)) for _ in range(128)))

        super(Order2, self).save(*args, **kwargs)

        email = self.data['customer']['email']
        if email:
            if is_new:
                MailSender(
                    "Спасибо за заявку",
                    "mail_templates/thanks_for_order.html",
                    email,
                    context={
                        "order": self
                    }
                ).send_mail()

        self.__original_state = self.state


class Order(models.Model):

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        # Взятие исходного состояния, чтобя при сохранении,
        # в засисимости от его изменение отправиь уведомления etc
        self.__original_state = self.state

    class Meta():
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    # USER FIELDS
    customer_name = models.CharField(
        max_length=256,
        verbose_name='ФИО',
        blank=True
    )
    email = models.EmailField(
        verbose_name='E-mail',
        blank=True
    )
    phone_number = models.CharField(
        max_length=12,
        verbose_name='Телефон',
        blank=True
    )
    client_notes = models.TextField(
        max_length=2000,
        verbose_name='Пожелания',
        blank=True
    )
    address = models.TextField(
        max_length=2000,
        verbose_name='Адрес доставки',
        blank=True
    )
    # SERVICE FIELDS
    managet_notes = models.TextField(
        max_length=2000,
        verbose_name='Служебные заметки',
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Последнее изменение'
    )
    ORDER_STATE = (
        ("новый", "Новый"),
        ("недозвон", "Недозвон"),
        ("доставка", "Доставка"),
        ("согласован", "Согласован"),
        ("выполнен", "Выполнен"),
        ("отменён", "Отменён"),
        ("отменён: недозвон", "Отменён: недозвон"),
    )
    state = models.CharField(
        max_length=100,
        verbose_name='Состояние заказа',
        choices=ORDER_STATE,
        default=ORDER_STATE[0][0]
    )

    ORDER_SOURCE = (
        ('cart', 'Корзина'),
        ('callback', 'Обратный звонок'),
        ('product-page', 'Страница товара')
    )
    source = models.CharField(
        max_length=128,
        verbose_name='Источник заказа',
        choices=ORDER_SOURCE,
        default=ORDER_SOURCE[0][0],
    )

    ORDER_DELIVERY_MODE = (
        ('', 'не выбрано'),
        ('SDEK_COURIER', 'курьером'),
        ('SDEK_POINT', 'постамат сдэк'),
        ('PICK_POINT', 'pickpoint'),
        ('POST_SERVICE', 'почта России')
    )
    delivery_mode = models.CharField(
        max_length=128,
        verbose_name="способ доставки",
        choices=ORDER_DELIVERY_MODE,
        default=ORDER_DELIVERY_MODE[0][0],
        blank=True,
    )

    delivery_code = models.CharField(
        max_length=128,
        verbose_name="код доставки",
        default="",
        blank=True
    )

    delivery_mode_selected = models.BooleanField(
        verbose_name="способ доставки выбран",
        default=False
    )

    def __str__(self):
        return("Заказ №{0}".format(str(self.id),)
               )

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        is_new = not self.id
        super(Order, self).save(force_insert, force_update, *args, **kwargs)
        # if is_new:
        #     notification_new_order.delay(self.phone_number, self.email, self.id)
        # elif self.state != self.__original_state:
        #     if self.state == "доставка":
        # notification_delivery.delay(self.phone_number, self.email, self.id)

        self.__original_state = self.state


class OrderItem(models.Model):

    class Meta():
        verbose_name = 'Пункт Заказа'
        verbose_name_plural = 'Пункты Заказа'

    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE)
    name = models.CharField(
        max_length=512,
        verbose_name='Название'
    )

    # TODO валидация
    price = models.PositiveIntegerField(
        verbose_name='Цена'
    )
    total_price = models.PositiveIntegerField(
        verbose_name='Полная цена'
    )
    full_url = models.CharField(
        max_length=512,
        verbose_name='URL',
    )
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')

    vendor_code = models.CharField(
        verbose_name="Артикул",
        max_length=1024,
    )
