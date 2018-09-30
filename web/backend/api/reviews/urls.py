from django.conf.urls import url, include

from .views import CubesProductCardReviewListAPIView, CubesProductCardReviewAPIView

urls_reviews = ([
    url(r'^$', CubesProductCardReviewListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>(([\d]+)))/$', CubesProductCardReviewAPIView.as_view(), name='details'),
])
