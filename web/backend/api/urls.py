from django.conf.urls import url, include

# application level api urls imports
from .shop_cubes.urls import urls as urls_cubes

# common api urls imports
from .cart.urls import urls_cart
from .search.urls import urls_search
from .md_admin.urls import urls_admin
from .yml.urls import urls_yml
from .products.urls import urls_product
from .order.urls import urls_order
from .users.urls import urls_users
from .payment.urls import urls_payment
from .sms.urls import urls_sms
from .mail.urls import urls_mail
from .mywarehouse.urls import urls_mywarehouse


urls_api = ([
    # APPLICATION LEVEL API URLS
    url(r'^cubes/', include(urls_cubes)),
    # COMMON API URLS
    url(r'^cart/', include(urls_cart)),
    url(r'^search/', include(urls_search, namespace="search")),
    url(r'^admin/', include(urls_admin)),
    url(r'^products/', include(urls_product)),
    url(r'^order/', include(urls_order)),
    url(r'^users/', include(urls_users)),
    url(r'^payments/', include(urls_payment)),
    url(r'^mail/', include(urls_mail)),
    url(r'^sms/', include(urls_sms)),
    url(r'^yml/', include(urls_yml)),
    url(r'^my-warehouse/', include(urls_mywarehouse))
], 'api')
