from django.conf.urls import url, include

from .views import (OrderAPIView,
                   OrderListAPIView,
                   OrderPaymentsAPIView,
                   OrderPaymentsDetailsAPIView)


urls_order = ([
    url(r'^(?P<uuid>(([\d]+)))/$', OrderAPIView.as_view()),
    url(r'^list/$', OrderListAPIView.as_view()),
    url(r'^(?P<pk>(([\d]+)))/payments/$', OrderPaymentsAPIView.as_view()),
    url(r'^(?P<order_pk>(([\d]+)))/payments/(?P<payment_pk>(([\d]+)))/$', OrderPaymentsAPIView.as_view())
])
