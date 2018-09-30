import os

from django.http import Http404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import LimitOffsetPagination

from shop_cubes.models import CubesProductCardReview
from shop_cubes.serializers import PrivateCubesProductCardReviewSerializer


class CubesProductCardReviewListAPIView(generics.ListAPIView):

    queryset = CubesProductCardReview.objects.all().order_by('-created_at')
    serializer_class = PrivateCubesProductCardReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUser,)


class CubesProductCardReviewAPIView(APIView):

    model = CubesProductCardReview
    serializer_class = PrivateCubesProductCardReviewSerializer
    permission_classes = (IsAdminUser, )

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, *args, **kwargs):
        instance = self.get_object(pk)
        serializer = self.serializer_class(
            instance=instance,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk, *args, **kwargs):
        instance = self.get_object(pk)
        instance.delete()
        return Response(
            status=status.HTTP_200_OK
        )
