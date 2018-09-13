from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.contrib.sitemaps.views import sitemap, index as sitemap_index
from django.urls import reverse

from users.views import (ProfileView,
                         RegistrationView,
                         LoginView,
                         LogoutView,
                         UserVerificationView)
from api.urls import urls_api
from infopages.urls import urls_infopages
from shop_cubes.models import CubesCategoryNode, CubesProductCard


class StaticViewSitemap(Sitemap):

    def items(self):
        return [
            'shop:index',
            'infopages:about',
            'infopages:vacancies',
            'infopages:cashback',
            'infopages:faq',
            'infopages:delivery',
            'infopages:contacts',
        ]

    def location(self, item):
        return reverse(item)


sitemaps = {
    "categories": GenericSitemap({
        "queryset": CubesCategoryNode.public.all(),
        "date_field": "modified_at",
    }),
    "products": GenericSitemap({
        "queryset": CubesProductCard.public.all(),
        "date_field": "modified_at",
    }),
    "static-pages": StaticViewSitemap
}


urlpatterns = [
    url(r'^oauth2/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^md-admin/', include('md_admin.urls', namespace='md-admin')),
    url(r'^controls/', include('controls.urls', namespace='controls')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^api/', include(urls_api, namespace='api')),
    url(r'^u/', include('users.urls', namespace="users")),
    url(r'^i/', include(urls_infopages, namespace="infopages")),
    # SITEMAP
    url(r'^sitemap', include([
                             url(r'^\.xml$', sitemap_index, {"sitemaps": sitemaps}),
                             url(r'^-(?P<section>.+)\.xml$', sitemap, {
                                 "sitemaps": sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
                             ])),
    url(r'^ym/payment-success/$', TemplateView.as_view(template_name="payment/payment-success.html")),
    url(r'^ym/payment-fail/$', TemplateView.as_view(template_name="payment/payment-fail.html")),
    url(r'^ym/', include('yandex_money.urls', namespace="yandex-money")),
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
