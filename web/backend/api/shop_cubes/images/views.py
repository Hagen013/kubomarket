from hashlib import md5

from django.core.cache import cache
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shop_cubes.models import CubesProductCard, CubesProductAdditionalImage
from tasks.images import add_cubes_image_from_file


class AdditionalImageAPIView(APIView):
    """
    Класс отображения и изменения сущностей AdditionalImage с
    с помощью API
    """

    image_class = None

    def get(self, request, image_id, *args, **kwargs):
        try:
            instance = self.image_class.objects.get(id=image_id)
        except image_class.DoesNotExist:
            raise Http404
        return Response({
            'id': instance.id,
            'url': instance.image.url,
            'product': instance.product.id,
            'order': instance.order,
        })

    def delete(self, request, image_id, *args, **kwargs):
        self.check_permissions(request)
        try:
            instance = self.image_class.objects.get(id=image_id)
            instance.delete()
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            status=status.HTTP_200_OK
        )

    def check_permissions(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied


class AdditionalImageUploadAPIView(APIView):

    image_class = None
    product_class = None

    def get(self, request, *args, **kwargs):
        self.check_permissions(request)
        task_id = request.GET.get('task_id')
        state = cache.get(task_id)
        return Response({
            'is_ready': state
        })

    def post(self, request, *args, **kwargs):
        self.check_permissions(request)
        image_file = request.FILES['file']
        slug = request.POST.get('product_slug')
        task_str = slug+image_file.name
        task_id = md5(task_str.encode()).hexdigest()
        cache.set(task_id, False)
        add_cubes_image_from_file(slug, image_file)
        cache.set(task_id, True)
        return Response({
            'detail': 'acknowledged',
            'task_id': task_id
        })

    def check_permissions(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied


class CubesAdditionalImageUploadAPIView(AdditionalImageUploadAPIView):

    product_class = CubesProductCard
    image_class = CubesProductAdditionalImage


class CubesAdditionalImageAPIView(AdditionalImageAPIView):

    image_class = CubesProductAdditionalImage