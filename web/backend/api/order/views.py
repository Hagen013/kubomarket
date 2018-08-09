from django.http import Http404
from django.core.exceptions import PermissionDenied

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import LimitOffsetPagination

from cart.models import Order2
from cart.serializers import OrderSerializer


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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class OrderListAPIView(generics.ListAPIView):

    queryset = Order2.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUser,)
