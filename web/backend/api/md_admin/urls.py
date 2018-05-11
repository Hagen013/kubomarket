from django.conf.urls import url, include
from .views import AuthenticationCheckAPIView

urls_admin = ([
    url(r'^is_staff/$', AuthenticationCheckAPIView.as_view(), name='is_staff')
])
