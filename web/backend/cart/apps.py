from django.apps import AppConfig
from django.db.models.signals import post_save, pre_delete


class CartConfig(AppConfig):
    name = 'cart'

    def ready(self):
        from .signals import order_on_save
        from .models import Order2
        post_save.connect(order_on_save, Order2)
