import xml.etree.ElementTree as ET

import requests
from config.celery import app
from celery.schedules import crontab
from django.conf import settings

from cart.models import Order2

MERCHANT_ID = settings.MERCHANT_ID
MERCHANT_LOGIN = settings.MERCHANT_LOGIN
MERCHANT_PASSWORD = settings.MERCHANT_PASSWORD
XML_FORMAT = 3
API_URL = "https://payments.demo.paysecure.ru/orderstate/orderstate.cfm"


@app.task
def sync_assist_order(order_id):
    response = requests.post(
        API_URL,
        data={
            "Merchant_ID": MERCHANT_ID,
            "Login": MERCHANT_LOGIN,
            "Password": MERCHANT_PASSWORD,
            "Format": XML_FORMAT,
            "Ordernumber": str(order_id)
        }
    )
    result = ET.ElementTree(ET.fromstring(response.text))
    is_approved = any((os.text == "Approved" for os in result.findall("order/orderstate")))
    if is_approved:
        Order2.objects.filter(id=order_id).update(assist_status="approved")


@app.task
def sync_assist():
    for order in Order2.objects.filter(assist_status="in_process"):
        sync_assist_order.delay(order.id)


app.add_periodic_task(
    crontab(minute='*/15'),
    sync_assist.s(),
    name='sync_assist',
)
