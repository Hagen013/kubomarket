from django.conf.urls import url, include

from .views import OrderAPIView, OrderListAPIView


urls_order = ([
    url(r'^(?P<uuid>(([\d]+)))/$', OrderAPIView.as_view()),
    url(r'^list/$', OrderListAPIView.as_view()),
])
