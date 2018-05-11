from collections import namedtuple
from datetime import datetime

import logging
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from core.db.shop import OfferIdentifier

# Get an instance of a logger

# Корзина -- сервер-сайд структура данных, находящаяся в сессии
# Является кешируемым коллектором для товаров, совмесимым с Django-cache
#
# Связь - OfferIdentifier
#
# cart = {
#     'created_at': "2016-03-09T08:18:20.860968", # ISO DATE
#     'modified_dt': "2016-03-09T08:18:52.860968",
#     'items': {
#          str(OfferIdentifier)
#         'shop_watches__watchesproductpage__46317' : {
#             'name': 'Часы Бога',
#             'price': 12000,
#             'quantity': 2,
#             'total_price': 24000,
#             'image': '/media/image/ofer123.jpg',
#             'url': '/catalog/watches/caio-gt-1234/'
#             'added_at': "2016-03-09T08:18:52.860968",
#             'vendor_code': 'wenger-1155215',
#             'data_for_delivery': {...}
#         },
#         'shop_watches__watchesproductpage__46457' : {
#             ...
#             ...
#         },
#         'shop_watches__watchesproductpage__463' : {
#             ...
#             ...
#         }
#     ],
#     'total_price': 123,
#     'items_quantiy': 2
# }
#
#


class Cart(object):

    CART_SESSION_ID = 'cart'

    def __init__(self, request):
        # Инициализация корзины пользователя
        self.session = request.session
        cart = self.session.get(self.CART_SESSION_ID)
        if not cart:
            # Сохраняем корзину пользователя в сессию
            now_time = datetime.now().isoformat()
            cart = self.session[self.CART_SESSION_ID] = {
                'created_at': now_time,
                'modified_at': now_time,
                'items': {},
                'total_price': 0,
                'items_quantiy': 0,
            }
        self.cart = cart

    # Добавление товара в корзину
    def add_offer(self, offer_identifier):
        item = self.cart['items'].get(offer_identifier)
        # если такой товар уже есть, то прибавиьт 1
        if not item:
            offer = OfferIdentifier.from_str(offer_identifier).get()
            new_item = {
                'name': offer.name,
                'price': offer.price,
                'quantity': 1,
                'total_price': offer.price,
                'image': offer.thumbnail.url,       # !!! with image
                'url': offer.get_absolute_url(),    # !!! displayable,
                'vendor_code': offer.vendor_code,
                'added_at': datetime.now().isoformat(),
                'data_for_delivery': offer.data_for_delivery,
                'vendor': offer.vendor,
            }
            self.cart['items'][offer_identifier] = new_item
            self.save()
        else:
            item['quantity'] += 1
            item['total_price'] = item['quantity'] * item['price']
            self.save()

    def delete_offer(self, offer_identifier):
        del self.cart['items'][offer_identifier]
        self.save()

    def update_offer_quantity(self, offer_identifier, quantity):
        item = self.cart['items'][offer_identifier]
        item['quantity'] = quantity
        item['total_price'] = item['price'] * quantity
        self.save()

    def calculate_total_price(self):
        self.cart['total_price'] = 0
        for _, item in self.cart['items'].items():
            self.cart['total_price'] += item['total_price']

    def calculate_items_quantiy(self):
        self.cart['items_quantiy'] = len(self.cart['items'])

    # TODO синхронизация корзины с базой
    def refresh_cart(self):
        for item in self.cart.items:
            pass

    # Сохранение данных в сессию
    def save(self):
        self.calculate_total_price()
        self.calculate_items_quantiy()
        self.cart['modified_at'] = datetime.now().isoformat()
        self.session[self.CART_SESSION_ID] = self.cart
        self.session.modified = True

    # очистка корзины
    def clear(self):
        del self.session[self.CART_SESSION_ID]
        self.session.modified = True
