from django.conf.urls import url, include

from .views import SessionLoginAPIView


urls_users = ([
    url(r'^login/$', SessionLoginAPIView.as_view(), name='login')
], 'users')

