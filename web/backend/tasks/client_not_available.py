import requests

from django.core.mail import EmailMessage
from django.conf import settings

from config.celery import app
from cart.models import Order2
from core.utils import SMSMessage, MailSender

EMAIL_REPLY_TO = "info@kubomarket.ru"


@app.task(retry_kwargs={'max_retries': 0})
def notify_client(order_id):
    instance = Order2.objects.get(public_id=order_id)
    phone_code = "7"
    phone = phone_code + instance.data["customer"]["phone"]
    message = "Уважаемый клиент, мы не смогли до вас дозвониться для подтверждения заказа {public_id}".format(
        public_id=order_id
    )
    sms = SMSMessage(
        phone=phone,
        message=message,
    )
    sms.send()

    email = instance.data['customer']['email']
    if email != "":
        title = "Заказ: {public_id}: не удалось дозвониться для подтверждения".format(public_id=order_id)
        text = "Уважаемый клиент, Kubomarket.Ru не удалось до вас дозвониться по предоставленному телефону +{phone} для подтверждения заказа: {public_id}".format(
            phone=phone,
            public_id=order_id
        )
        email = EmailMessage(
            title,
            text,
            to=[email],
            reply_to=[EMAIL_REPLY_TO],
        )
        email.send()


@app.task(retry_kwargs={'max_retries': 0})
def send_rupost_id(order_id, dispatch_number):
    instance = Order2.objects.get(public_id=order_id)
    instance = Order2.objects.get(public_id=order_id)
    phone_code = "7"
    phone = phone_code + instance.data["customer"]["phone"]
    if len(dispatch_number) > 0:

        message = "Номер вашего почтового отправления: {dispatch_number}".format(
            dispatch_number=dispatch_number
        )
        sms = SMSMessage(
            phone=phone,
            message=message,
        )
        sms.send()

        email = instance.data['customer']['email']
        if email != "":
            title = "Заказ: {public_id}: почтовый идентификатор".format(public_id=order_id)
            text = "Уважаемый клиент, по вашему заказу {public_id} сформирована почтовая посылка с номером: {dispatch_number}".format(
                dispatch_number=dispatch_number,
                public_id=order_id
            )
            email = EmailMessage(
                title,
                text,
                to=[email],
                reply_to=[EMAIL_REPLY_TO],
            )
            email.send()
