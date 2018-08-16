from django.conf.urls import url, include

from .views import (ProductCardAPIView,
                    ProductCardAttributesAPIView,
                    CubesProductCardImagesAPIView,
                    CubesProductCardImageUploadAPIView,
                    ProductCardModificationsAPIView,
                    ProductCardDescriptionImagesAPIView,
                    ProductReviewListAPIView,
                    ProductReviewAPIView)

urls_product = ([
    url(r'^(?P<pk>(([\d]+)))/$', ProductCardAPIView.as_view(), name='info'),
    url(r'^(?P<pk>(([\d]+)))/images/$', CubesProductCardImagesAPIView.as_view(), name='images'),
    url(r'^(?P<pk>(([\d]+)))/image/$', CubesProductCardImageUploadAPIView.as_view(), name='image'),
    url(r'^(?P<pk>(([\d]+)))/attributes/$', ProductCardAttributesAPIView.as_view(), name="attributes"),
    url(r'^(?P<pk>(([\d]+)))/modifications/$', ProductCardModificationsAPIView.as_view(), name="modifications"),
    url(r'^(?P<pk>(([\d]+)))/description/images/$', ProductCardDescriptionImagesAPIView.as_view(), name="description-images"),
    url(r'^(?P<product_pk>(([\d]+)))/video-reviews/$', ProductReviewListAPIView.as_view(), name="video-reviews"),
    url(r'^(?P<product_pk>(([\d]+)))/video-reviews/(?P<pk>(([\d]+)))/$', ProductReviewAPIView.as_view(), name="video-review")
])
