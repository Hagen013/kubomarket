from django.conf.urls import url, include
from django.views.generic import TemplateView

from .views import (RegistrationView,
                    RegistrationAftercheckView,
                    ProfileView,
                    LoginView,
                    LogoutView,
                    UserVerificationView)


urlpatterns = [
    url(r'^registration/$', RegistrationView.as_view(), name="registration"),
    url(r'^profile/$', ProfileView.as_view(), name="profile"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^registration-success', RegistrationAftercheckView.as_view(), name="aftercheck"),
    url(r'^(?P<pk>\d+)/(?P<token>.+)/$', UserVerificationView.as_view()),
]

