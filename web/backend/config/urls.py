from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views import defaults as default_views
from django.views.generic import TemplateView

from users.views import ProfileView, RegistrationView, LoginView, LogoutView
from api.urls import urls_api


urlpatterns = [
    url(r'^oauth2/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^md-admin/', include('md_admin.urls', namespace='md-admin')),
    url(r'^controls/', include('controls.urls', namespace='controls')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^api/', include(urls_api, namespace='api')),
    url(r'^faq/', TemplateView.as_view(template_name="pages/infopages/faq.html")),
    url(r'^delivery-and-payment/', TemplateView.as_view(
        template_name="pages/infopages/delivery-and-payment.html")),
    url(r'^contacts/', TemplateView.as_view(template_name="pages/infopages/contacts.html")),
    url(r'^order-check/', TemplateView.as_view(template_name="pages/infopages/order-check.html")),
    url(r'^registration/', RegistrationView.as_view()),
    url(r'^profile/', ProfileView.as_view()),
    url(r'^login/', LoginView.as_view()),
    url(r'^logout/', LogoutView.as_view()),
    url(r'^', include('shop_cubes.urls', namespace='shop'))
]

if settings.DEBUG:

    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request')}),
        url(r'^403/$', default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        from django.conf.urls.static import static

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
