from django.http import Http404
from django.core.exceptions import PermissionDenied

from rest_framework.views import APIView
from rest_framework import generics, pagination, status
from rest_framework.response import Response

from cart.models import Order2
from cart.serializers import OrderSerializer


class OrderAPIView(APIView):

    def get(self, request, uuid, *args, **kwargs):
        try:
            instance = Order2.objects.get(id=uuid)
        except Order2.DoesNotExist:
            raise Http404
        serializer = OrderSerializer(instance)
        return Response(serializer.data)

    def put(self, request, uuid, *args, **kwargs):
        try:
            instance = Order2.objects.get(id=uuid)
        except Order2.DoesNotExist:
            raise Http404
        serializer = OrderSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uuid, *args, **kwargs):
        return Response({
        })


class OrderPagination(pagination.PageNumberPagination):
    page_size = 100


class OrderListAPIView(generics.ListAPIView):

    model = Order2
    serializer_class = OrderSerializer
    pagination_class = OrderPagination

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = OrderSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def get_queryset(self):
        return self.model.objects.all().order_by('-created_at')

