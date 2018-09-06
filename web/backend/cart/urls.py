from django.conf.urls import url, include

from .views import CartPageView, PaymentPageView


urlpatterns = [
    url(r'^$', CartPageView.as_view(), name='details'),
    url(r'^payment/$', PaymentPageView.as_view(), name='payment')
]
