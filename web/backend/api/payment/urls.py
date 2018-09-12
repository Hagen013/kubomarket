from django.conf.urls import url, include

from .views import OrderPaymentAPIView


urls_payment = ([
    url(r'^orders/(?P<pk>(([\d]+)))/$', OrderPaymentAPIView.as_view())
])
