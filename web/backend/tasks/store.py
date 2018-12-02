import requests

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.conf import settings

from celery.signals import beat_init
from celery.schedules import crontab
from config.celery import app

from shop_cubes.models import CubesProductCard as Product


stock_url = "https://online.moysklad.ru/api/remap/1.1/report/stock/all/"
LOGIN = settings.STORE_LOGIN
PASSWORD = settings.STORE_PASSWORD

def get_full_code(code):
    return 'cubemarket-{code}'.format(code=code)

@app.task
def sync_store():
    rows = []
    limit = 100
    offset = 0
    page_size = 100

    contains_rows = True

    while contains_rows:
        payload = {'limit': limit, 'offset': offset}
        response = requests.get(
            stock_url,
            auth=(LOGIN, PASSWORD),
            params=payload
        )
        data = response.json()
        received_rows = data['rows']
        if len(received_rows) == 0:
            contains_rows = False
        rows += received_rows
        offset += page_size
        
    with transaction.atomic():
        for row in rows:
            code = get_full_code(row['code'])
            quantity = row['quantity']
            instance_found = False
            try:
                instance = Product.objects.get(
                    vendor_code=code
                )
                instance_found = True
            except ObjectDoesNotExist:
                pass
            if instance_found:
                instance.stored = True
                instance.amount = int(quantity)
                instance.save()


app.add_periodic_task(
    crontab(minute=0,  hour='*/1'),
    sync_store.s(),
    name='sync_store',
)