from django.conf.urls import url

from .views import SearchResultsView, SearchByCodeView

urlpatterns = [
    url(r'^by-code/(?P<line>.+)/$', SearchByCodeView.as_view(), name='results-by-code'),
    url(r'^(?P<line>.+)/$', SearchResultsView.as_view(), name='results'),
]
