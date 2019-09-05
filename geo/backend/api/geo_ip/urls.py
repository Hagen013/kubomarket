from django.conf.urls import url, include

from .views import GeoIpAPIView, GeoIpCoordinatesAPIView

geo_ip_urls = (
    [
        url(r'^$', GeoIpAPIView.as_view()),
        url(r'^coordinates/$', GeoIpCoordinatesAPIView.as_view()),
    ],
    'geo_ip'
)
