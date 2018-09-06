from .models import Order2

from tasks.sms_notifications import sms_notify
from tasks.mail_notifications import mail_notify


def order_on_save(sender, instance, **kwargs):
    pass

