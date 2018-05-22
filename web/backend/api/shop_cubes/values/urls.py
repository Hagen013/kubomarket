from django.conf.urls import url, include

from .views import (CubesAttributeValueListAPIView,
                    CubesAttributeValueAPIView)

urls_values = ([
    url(r'^$', CubesAttributeValueListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>(([\d]+)))/$', CubesAttributeValueAPIView.as_view(), name="details")
])
