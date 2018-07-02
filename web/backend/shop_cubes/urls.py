from django.conf.urls import url, include
from django.views.generic import TemplateView

from .views import CubesCategoryPageView, CubesProductPageView, IndexPage


urlpatterns = [
    url(r'^$', IndexPage.as_view()),
    url(r'^catalog/(?P<url>(($)|([-_\.\d\w/]+/$)))', CubesCategoryPageView.as_view(), name='category'),
    url(r'^product/(?P<slug>(($)|([-_\.\d\w/]+/$)))', CubesProductPageView.as_view(), name='product'),
]
