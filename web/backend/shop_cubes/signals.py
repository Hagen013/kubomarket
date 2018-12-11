from .models import CubesProductCard
from django.db.models.signals import post_save, pre_delete

from tasks.elastic import update_es_product, delete_es_product
from tasks.yandex_market import generate_yml_file


def product_on_save(sender, instance, **kwargs):
    update_index = instance.update_search
    #generate_yml_file.delay()
    if update_index:
        update_es_product(instance.id)


def product_on_delete(sender, instance, **kwargs):
    update_index = instance.update_search
    if update_index:
        delete_es_product(instance.id)
