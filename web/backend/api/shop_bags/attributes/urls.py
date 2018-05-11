from django.conf.urls import url, include

from .views import (CubesAttributeListAPIView,
                    CubesAttributeAPIView)

urls_attributes = ([
    url(r'^$', CubesAttributeListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>(([\d]+)))/$', CubesAttributeAPIView.as_view(), name="details")
])
