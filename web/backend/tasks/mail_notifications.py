from cart.models import Order2
from core.utils import MailSender

from config.celery import app


@app.task
def mail_notify(pk):
    instance = Order2.objects.get(id=pk)
    email = instance.data['customer']['email']
    MailSender(
        "Спасибо за заявку",
        "mail_templates/thanks_for_order.html",
        email,
        context={
            "order": instance
        }
    ).send()
    instance.notified_by_email = True
    instance.save()


