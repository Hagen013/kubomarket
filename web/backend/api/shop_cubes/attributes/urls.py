from django.conf.urls import url, include

from .views import (CubesAttributeListAPIView,
                    CubesAttributeAPIView,
                    CubesAttributeValueListApiView,
                    CubesAttributeValueApiView)

urls_attributes = ([
    url(r'^$', CubesAttributeListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>(([\d]+)))/$', CubesAttributeAPIView.as_view(), name="details"),
    url(r'^(?P<pk>(([\d]+)))/values/$', CubesAttributeValueListApiView.as_view(), name="values-list"),
    url(r'^(?P<attribute_pk>(([\d]+)))/values/(?P<value_pk>(([\d]+)))/$', CubesAttributeValueApiView.as_view(), name="value")
])
