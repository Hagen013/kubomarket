from functools import wraps
from unidecode import unidecode

import requests
from hashlib import md5

from django.conf import settings

from django.template.defaultfilters import slugify as dj_slugify
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
EMAIL_REPLY_TO = "info@kubomarket.ru"


class DisallowedBeforeCreationException(Exception):
    pass


def disallowed_before_creation(fn):
    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        if not self.id:
            msg = "Method {0} of {1} class instance is disallowed before creation".format(
                fn.__name__,
                self.__class__.__name__
            )
            raise DisallowedBeforeCreationException(msg)
        return fn(self, *args, **kwargs)
    return wrapped


def slugify(s):
    return dj_slugify(unidecode(s))


def md5_file_checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


class MailSender():

    def __init__(self, title, template, recipient, context={}):
        self.title = title
        self.template = template
        self.recipient = recipient
        self.context = context

    def render_template(self):
        return render_to_string(self.template, {"title": self.title, **self.context})

    def send(self):
        title = self.title
        html_message = self.render_template()
        email = EmailMessage(
            self.title,
            html_message,
            to=[self.recipient],
            reply_to=[EMAIL_REPLY_TO],
        )

        email.content_subtype = "html"
        email.send()
 