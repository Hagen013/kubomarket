from .models import Order2

from tasks.sms_notifications import sms_notify
from tasks.mail_notifications import mail_notify


def order_on_save(sender, instance, **kwargs):
    if instance.total_price > 0:
        if not instance.notified_by_sms:
            sms_notify(instance.id)
        if not instance.notified_by_email and instance.data["customer"]["email"] != "":
            mail_notify(instance.id)

