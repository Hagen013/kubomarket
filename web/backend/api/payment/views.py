import uuid

from django.http import Http404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from yandex_money.models import Payment
from yandex_money.serializers import PaymentSerializer

from cart.models import Order2


class OrderPaymentAPIView(APIView):

    permission_classes = (IsAdminUser,)
    model = Order2
    serializer_class = PaymentSerializer

    def get_order(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def post(self, request, pk, *args, **kwargs):
        instance = self.get_order(pk)
        user = instance.user
        cps_phone = instance.data['customer']['phone']
        if len(cps_phone) == 0:
            cps_phone = None
        cps_email = instance.data['customer']['email']
        if len(cps_email) == 0:
            cps_email = None

        payment = Payment(
            order=instance,
            user=user,
            order_amount=instance.total_price,
            order_number=instance.public_id,
            cps_phone=cps_phone,
            cps_email=cps_email
        )
        if user is not None:
            payment.customer_number = user.id

        payment.save()
        serializer = self.serializer_class(instance.payments.all(), many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
