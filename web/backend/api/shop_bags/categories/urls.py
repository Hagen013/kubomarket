from django.conf.urls import url, include

from .views import (CubesCategoryPriceAPIView,
                    CubesCategoryFiltersAPIView,
                    CubesCategoryAPIView,
                    CubesCategoryNodeInputsAPIView,
                    CubesCategoryNodeOutputsAPIView,
                    CubesCategoryNodeListAPIView)   

urls_categories = ([
    url(r'^$',
        CubesCategoryNodeListAPIView.as_view(),
        name='list'),
    url(r'^(?P<pk>(([\d]+)))/$',
        CubesCategoryAPIView.as_view(),
        name='category'),
    url(r'^(?P<pk>(([\d]+)))/inputs/$',
        CubesCategoryNodeInputsAPIView.as_view(),
        name='inputs'),
    url(r'^(?P<pk>(([\d]+)))/outputs/$',
        CubesCategoryNodeOutputsAPIView.as_view(),
        name='outputs'),
    url(r'^(?P<pk>([-_\.\d\w]+))/prices/$',
        CubesCategoryPriceAPIView.as_view(),
        name='prices'),
    url(r'^(?P<pk>([-_\.\d\w]+))/filters/$',
        CubesCategoryFiltersAPIView.as_view(),
        name='filters'),
], 'categories')

