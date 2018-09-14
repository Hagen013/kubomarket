import requests

from django.conf import settings
from config.celery import app

from cart.models import Order2


@app.task
def sms_notify(order_id):
    instance = Order2.objects.get(public_id=order_id)
    phone_code = "7"
    to = phone_code + instance.data["customer"]["phone"]
    msg = "Ваш заказ № {order_id} поступил в обработку, и в ближайшее время\
 с Вами свяжется оператор для уточнения деталей заказа. Kubomarket.Ru".format(
        order_id=order_id
    )
    payload = {
        "api_id": settings.SMS_SECRET_KEY,
        "msg": msg,
        "to": to,
        "from": "Kubomarket",
        "json": "1"
    }
    response = requests.get(url=settings.SMS_URL, params=payload)
    if response.json()["status"] != "OK":
        raise Error("SMS notification failed")
    else:
        instance.notified_by_sms = True
        instance.save()
