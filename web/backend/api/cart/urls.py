from django.conf.urls import url, include

from .views import (CartAPIView,
                    CartTotalPriceAPIView,
                    CartItemsAPIView,
                    CartDetalItemAPIView,
                    CartItemsQuantiyAPIView,
                    CartMakeOrderAPIView)


urls_cart = ([
    url(
        r'^$',
        CartAPIView.as_view()
    ),  # CART - GET
    url(
        r'^total_price/$',
        CartTotalPriceAPIView.as_view()
    ),  # TOTAL PROCE - GET
    url(
        r'^items_quantiy/$',
        CartItemsQuantiyAPIView.as_view()
    ),
    url(
        r'^items/$',
        CartItemsAPIView.as_view()
    ),  # CART ITEMS - GET
    url(
        r'^items/(?P<offer_identifier>[-_a-z]+__[-_a-z]+__[\d]+)/$',
        CartDetalItemAPIView.as_view()
    ),  # DETAL ITEM
    url(
        r'^make_order/$',
        CartMakeOrderAPIView.as_view()
    )  # MAKE ORDER
], 'cart')
