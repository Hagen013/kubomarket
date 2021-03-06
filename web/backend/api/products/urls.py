from django.conf.urls import url, include

from .views import (ProductCardAPIView,
                    ProductCardAttributesAPIView,
                    CubesProductCardImagesAPIView,
                    CubesProductCardImageUploadAPIView,
                    ProductCardModificationsAPIView)

urls_product = ([
    url(r'^(?P<pk>(([\d]+)))/$', ProductCardAPIView.as_view(), name='info'),
    url(r'^(?P<pk>(([\d]+)))/images/$', CubesProductCardImagesAPIView.as_view(), name='images'),
    url(r'^(?P<pk>(([\d]+)))/image/$', CubesProductCardImageUploadAPIView.as_view(), name='image'),
    url(r'^(?P<pk>(([\d]+)))/attributes/$', ProductCardAttributesAPIView.as_view(), name="attributes"),
    url(r'^(?P<pk>(([\d]+)))/modifications/$', ProductCardModificationsAPIView.as_view(), name="modifications")
])
