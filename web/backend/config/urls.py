from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views import defaults as default_views
from django.views.generic import TemplateView

from api.urls import urls_api


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^md-admin/', include('md_admin.urls', namespace='md-admin')),
    url(r'^controls/', include('controls.urls', namespace='controls')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^api/', include(urls_api, namespace='api')),
    url(r'^', include('shop_cubes.urls', namespace='shop'))
]

if settings.DEBUG:

    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        from django.conf.urls.static import static

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
