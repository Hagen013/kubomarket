import datetime
import requests
import time

from django.template.loader import render_to_string
from django.utils.timezone import now, pytz
from django.conf import settings
from celery.signals import beat_init
from celery.schedules import crontab

from config.celery import app
from shop_cubes.models import CubesProductCard, CubesCategoryNode

MYWAREHOUSE_YML_FILE = settings.MYWAREHOUSE_YML_PATH + "yml.xml"

API_URL = "https://online.moysklad.ru/api/remap/1.1/report/stock/all"
AUTH = (settings.MYWAREHOUSE_LOGIN, settings.MYWAREHOUSE_PASSWORD)
CUBES_STORE = settings.MYWAREHOUSE_CUBES_STORE


@app.task
def generate_mywarehouse_yml_file():
    cubes = CubesProductCard.objects.all()

    context = {'date': now().strftime('%Y-%m-%d %H:%M'),
               'cubes': cubes,
               }

    xml_raw = render_to_string(template_name="myWarehouse/yml.xml", context=context)
    with open(MYWAREHOUSE_YML_FILE, "w") as fp:
        fp.write(xml_raw)


app.add_periodic_task(
    crontab(minute=7,  hour='*/2'),
    generate_mywarehouse_yml_file.s(),
    name='generate_mywarehouse_yml_file',
)


@beat_init.connect
def configure_workers(**kwargs):
    import os.path
    if not os.path.isfile(MYWAREHOUSE_YML_FILE):
        generate_mywarehouse_yml_file.delay()


@app.task
def sync_mywarehouse():
    vendor_codes_in_stock = set()
    with requests.Session() as session:
        session.auth = AUTH
        limit = 100
        params = {
            'offset': 0,
            'limit': limit,
            'store.id': CUBES_STORE,
        }
        page_num = 0
        while True:
            resp = session.get(API_URL, params=params)
            rows = resp.json()['rows']
            if not rows:
                break
            for row in rows:
                quantity = int(row['quantity'])
                if quantity <= 0:
                    continue
                upid = row['article']
                vendor_codes_in_stock.add(upid)
            page_num += 1
            params['offset'] = page_num * limit
            time.sleep(0.25)  # Не более 5 запросов в секунду с одного адреса от одного пользователя

    CubesProductCard.objects.filter(vendor_code__in=vendor_codes_in_stock).update(is_in_stock=True)


app.add_periodic_task(
    crontab(minute=0,  hour=12, day_of_week="*"),
    sync_mywarehouse.s(),
    name='sync_mywarehouse',
)
