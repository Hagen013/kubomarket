from django.conf.urls import url, include

from .views import CartPageView


urlpatterns = [
    url(r'^$', CartPageView.as_view(), name='details'),
]
