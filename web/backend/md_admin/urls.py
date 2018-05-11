from django.conf.urls import url

from .views import AdminTemplateView, AdminLoginView

urlpatterns = [
    url(r'^$', AdminTemplateView.as_view(), name='main'),
    url(r'^login/$', AdminLoginView.as_view(), name='login'),
]
