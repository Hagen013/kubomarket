from django.conf.urls import url

from .views import EmailAPIView


urls_mail = ([
    url(r'^$', EmailAPIView.as_view())
])
