from django.apps import AppConfig
from django.db.models.signals import post_save, pre_delete


class ShopCubesConfig(AppConfig):
    name = 'shop_cubes'
    verbose_name = 'Shop cubes'

    def ready(self):
        from .signals import product_on_save, product_on_delete
        from .models import CubesProductCard

        post_save.connect(product_on_save, CubesProductCard)
        pre_delete.connect(product_on_delete, CubesProductCard)
