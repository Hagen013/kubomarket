from django.conf.urls import url, include

from .views import YmlApiView


urls_mywarehouse = ([
    url(r'^yml\.xml/$', YmlApiView.as_view()),
])
