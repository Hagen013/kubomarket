import re

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException


from cart.cart import Cart
from cart.models import Order, OrderItem, Order2
from core.db.shop import OfferIdentifier
from tasks.mail_notifications import (anton_new_order_notification,
                                      client_new_order_notification)
from cart.serializers import OrderSerializer


class BaseCartAPIView(APIView):

    def initial(self, request, *args, **kwargs):
        """
        Получение корзины до вызова любого обработчика
        """
        super(BaseCartAPIView, self).initial(request, *args, **kwargs)
        self.cart = Cart(request)


class CartAPIView(BaseCartAPIView):

    def get(self, request, format=None):
        return(Response(self.cart.cart))


class CartTotalPriceAPIView(BaseCartAPIView):

    def get(self, request, format=None):
        return(Response(self.cart.cart['total_price']))


class CartItemsQuantiyAPIView(BaseCartAPIView):

    def get(self, request, format=None):
        return(Response(self.cart.cart['items_quantiy']))


class CartItemsAPIView(BaseCartAPIView):

    def get(self, request, format=None):
        return(Response(self.cart.cart['items']))

    def delete(self, request, format=None):
        self.cart.clear()
        return(Response(status=status.HTTP_200_OK))


class CartDetalItemAPIView(BaseCartAPIView):

    def get(self, request, offer_identifier, format=None):
        try:
            return(Response(self.cart.cart['items'][offer_identifier]))
        except KeyError:
            return(Response(status=status.HTTP_404_NOT_FOUND))

    def delete(self, request, offer_identifier):
        try:
            self.cart.delete_offer(offer_identifier)
            return(Response(status=status.HTTP_200_OK))
        except KeyError as error:
            return(Response(status=status.HTTP_404_NOT_FOUND))

    def put(self, request, offer_identifier):
        try:
            self.cart.add_offer(offer_identifier)
            return(Response(self.cart.cart['items'][offer_identifier]))
        except ObjectDoesNotExist:
            return(Response(status=status.HTTP_400_BAD_REQUEST))

    def post(self, request, offer_identifier):
        try:
            quantity = int(request.data['quantity'])
            if quantity > 0:
                self.cart.update_offer_quantity(offer_identifier,
                                                quantity)
                return(Response(self.cart.cart['items'][offer_identifier]))
            else:
                return(Response(status=status.HTTP_400_BAD_REQUEST))
        except KeyError:
            return(Response(status=status.HTTP_400_BAD_REQUEST))


class CartMakeOrderAPIView(BaseCartAPIView):

    def post(self, request, format=None):

        order_data = request.data['data']
        order_data['cart'] = {
            'total_price': self.cart.cart['total_price'],
            'items': dict(
                (
                    ((key, dict(
                        (ikey, value[ikey])
                        for ikey in [
                                "name",
                                "price",
                                "quantity",
                                "total_price",
                                "image",
                                "url",
                                "vendor_code"
                            ])
                      )
                        for key, value in self.cart.cart['items'].items()
                     )
                )
            )
        }

        user = request.user if request.user.is_authenticated() else None

        order = Order2(
            data=order_data,
            user=user,
            source=request.data.get('source', ''),
            client_notes=request.data.get('client_notes', '')
        )

        try:
            order.full_clean()
        except ValidationError as e:
            return Response(status=400, data=e.messages)

        order.save()
        serializer = OrderSerializer(order)

        self.cart.clear()
        return Response(
            serializer.data
        )
