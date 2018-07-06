from django.conf.urls import url, include

from .views import SessionLoginAPIView, UserOrdersAPIView, UserProfileAPIView, UserCommentsAPIView


urls_users = ([
    url(r'^login/$', SessionLoginAPIView.as_view(), name='login'),
    url(r'^(?P<pk>(([\d]+)))/orders/$', UserOrdersAPIView.as_view(), name="orders"),
    url(r'^(?P<pk>(([\d]+)))/comments/$', UserCommentsAPIView.as_view(), name="comments"),
    url(r'^(?P<pk>(([\d]+)))/profile/$', UserProfileAPIView.as_view(), name="profile"),
], 'users')


