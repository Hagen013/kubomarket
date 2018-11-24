import os

from django.http import Http404, HttpResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db import IntegrityError, transaction

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import LimitOffsetPagination

from yandex_money.models import Payment
from yandex_money.serializers import PaymentSerializer

from core.utils import MailSender
from cart.models import Order2
from cart.serializers import OrderSerializer
from tasks.receipts import generate_receipt
from tasks.client_not_available import notify_client


class OrderAPIView(APIView):

    def check_user_permissions(self, user, instance):
        if not user.is_authenticated:
            raise PermissionDenied
        if not (((user.is_staff)) or ( (instance.user is not None) and (user.id == instance.user.id))):
            raise PermissionDenied

    def get(self, request, uuid, *args, **kwargs):
        try:
            instance = Order2.objects.get(id=uuid)
        except Order2.DoesNotExist:
            raise Http404
        self.check_user_permissions(request.user, instance)
        serializer = OrderSerializer(instance)
        return Response(serializer.data)

    def put(self, request, uuid, *args, **kwargs):
        try:
            instance = Order2.objects.get(id=uuid)
        except Order2.DoesNotExist:
            raise Http404
        self.check_user_permissions(request.user, instance)
        serializer = OrderSerializer(instance, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['state'] == 'отменён: недозвон' and instance.state != serializer.validated_data['state']:
                notify_client.delay(instance.public_id)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    
class OrderListAPIView(generics.ListAPIView):

    queryset = Order2.objects.all().order_by('_order', '-created_at')
    serializer_class = OrderSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUser,)

    def filter_queryset(self, qs):
        params = self.request.query_params
        phone = params.get('phone', None)
        name = params.get('name', None)
        public_id = params.get('public_id', None)
        if phone is not None:
            qs = qs.filter(
                data__customer__phone__icontains=phone,
            )
        if name is not None:
            qs = qs.filter(
                data__customer__name__icontains=name
            )
        if public_id is not None:
            qs = qs.filter(
                public_id__icontains=public_id
            )
        return qs
        

    def get_queryset(self):
        qs = self.filter_queryset(self.queryset)
        return qs
        

class OrderPaymentsAPIView(APIView):

    permission_classes = (IsAdminUser,)
    model = Order2
    serializer_class = PaymentSerializer

    def get_order(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        instance = self.get_order(pk)
        serializer = self.serializer_class(instance.payments.all(), many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request, pk, *args, **kwargs):
        email = request.data['email']
        instance = self.get_order(pk)
        user = instance.user
        cps_phone = instance.data['customer']['phone']
        if len(cps_phone) == 0:
            cps_phone = None
        else:
            cps_phone = '+7' + cps_phone
        cps_email = instance.data['customer']['email']
        if len(cps_email) == 0:
            cps_email = None

        payment = Payment(
            order=instance,
            user=user,
            order_number=instance.public_id,
            order_amount=instance.total_price,
            cps_phone=cps_phone,
            cps_email=cps_email
        )
        if user is not None:
            payment.customer_number = user.id

        try:
            payment.save()
        except IntegrityError:
            with transaction.atomic():
                count = 1
                for item in instance.payments.all().order_by("-pub_date"):
                    item.order_number = instance.public_id + "-" + str(item.pk)
                    item.save()
                for item in instance.payments.all().order_by("-pub_date"):
                    item.order_number = instance.public_id + "-" + str(count)
                    item.save()
                    count += 1
        payment.save()

        MailSender(
            "Оплата заказа",
            "mail_templates/payment.html",
            email,
            context={
                "BASE_URL": "https://www.kubomarket.ru",
                "uuid": payment.uuid,
                "order": payment.order
            }
        ).send()

        serializer = self.serializer_class(instance.payments.all(), many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class OrderPaymentsDetailsAPIView(APIView):

    model = Payment
    serializer_class = PaymentSerializer
    permission_classes = (IsAdminUser,)

    def get_instance(self, order_pk, payment_pk):
        try:
            return self.model.objects.get(order__pk=order_pk, pk=payment_pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, order_pk, payment_pk, *args, **kwargs):
        instance = self.get_instance(order_pk, payment_pk)
        serializer = self.serializer_class(instance)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, order_pk, payment_pk, *args, **kwargs):
        instance = self.get_instance(order_pk, payment_pk)
        if not instance.is_payed:
            instance.delete()
            return Response(
                status=status.HTTP_200_OK
            )
        return Response(
            status=status.HTTP_403_FORBIDDEN
        )


class OrderReceiptAPIView(APIView):

    permission_classes = (IsAdminUser,)
    model = Order2

    def get_order(self, pk):
        try:
            return Order2.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        self.order = self.get_order(pk)
        filename = generate_receipt(pk)
        if os.path.exists(filename):
            with open(filename, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filename)
                return response
        raise Http404
