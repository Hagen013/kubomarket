from django.conf.urls import url, include

from .views import SearchAPIView, SearchByCodeAPIView
from .views import FacetesSearchAPIView


urls_search = ([
    url(r'^by-code/$', SearchByCodeAPIView.as_view(), name='json-search-by-code'),
    url(r'^$', SearchAPIView.as_view(), name='json-search'),
    url(r'^facetes/', FacetesSearchAPIView.as_view(), name='facetes')
], 'search')

