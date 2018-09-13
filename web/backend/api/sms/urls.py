from django.conf.urls import url

from .views import SMSAPIView


urls_sms = ([
    url(r'^$', SMSAPIView.as_view())
])
