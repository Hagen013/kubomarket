from django.conf import settings

from config.celery import app
from celery.schedules import crontab

from cart.models import Order2
from delivery.sdek import Client as ClientSDEK
from delivery.pickpoint import Client as ClientPickpoint
from delivery.rupost import Client as ClientRupost
from cart.serializers import OrderSerializer


@app.task
def sync_sdek_orders(pks):
    qs = Order2.objects.filter(id__in=pks)
    client = ClientSDEK(settings.SDEK_USER, settings.SDEK_PASSWORD)
    serializer = OrderSerializer(qs, many=True)
    results = client.get_orders_statuses(serializer.data)


@app.task
def sync_pickpoint_orders(pks):
    qs = Order2.objects.filter(id__in=pks)
    client = ClientPickpoint(settings.PICKPOINT_USER, settings.PICKPOINT_LOGIN)
    serializer = OrderSerializer(qs, many=True)
    for instance in serializer.data:
        pass


@app.task
def sync_postal_orders(pks):
    qs = Order2.objects.filter(id__in=pks)
    client = ClientRupost(settings.RUPOST_USER, settings.RUPOST_LOGIN)
    serializer = OrderSerializer(qs, many=True)
    for instance in serializer.data:
        pass
    


@app.task
def sync_delivery_statuses():
    sdek_orders_pks = []
    pickpoint_orders_pks = []
    postal_orders_pks = []
    qs = Order2.objects.all()
    for instance in qs:
        if instance.data['delivery']['is_mod_selected']:
            delivery_type = instance.data['delivery']['mod']['type']
            if delivery_type == 'curier':
                sdek_orders_pks.append(instance.id)
            elif delivery_type == 'postal_service':
                postal_orders_pks.append(instance.id)
            elif delivery_type == 'delivery_points':
                code = instance.data['delivery']['mod']['code']
                if code is not None:
                    if 'sdek' in code:
                        sdek_orders_pks.append(instance.id)
                    else:
                        postal_orders_pks.append(instance.id)
            else:
                # Unknown delivery_type
                pass
