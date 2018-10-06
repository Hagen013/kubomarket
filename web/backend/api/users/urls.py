from django.conf.urls import url, include

from .views import (UserApiView,
                    UserListAPIView,
                    SessionLoginAPIView,
                    UserOrdersAPIView,
                    UserProfileAPIView,
                    SessionAuthAPIView,
                    SubscribesAPIView)


urls_users = ([
    url(r'^$', UserListAPIView.as_view(), name="default"),
    url(r'^login/$', SessionLoginAPIView.as_view(), name="login"),
    url(r'^auth/$', SessionAuthAPIView.as_view(), name="auth"),
    url(r'^subscribes/$', SubscribesAPIView.as_view(), name="subscribes"),
    url(r'^(?P<pk>(([\d]+)))/$', UserApiView.as_view(), name="details"),
    url(r'^(?P<pk>(([\d]+)))/orders/$', UserOrdersAPIView.as_view(), name="orders"),
    url(r'^(?P<pk>(([\d]+)))/profile/$', UserProfileAPIView.as_view(), name="profile"),
], 'users')
