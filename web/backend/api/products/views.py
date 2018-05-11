from hashlib import md5

from django.core.cache import cache
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shop_cubes.models import CubesProductCard
from core.models import ProductCard
from core.serializers import ProductCardSerializer


class ProductCardListAPIView(APIView):
    """
    Клас для работы со списком товаров
    """

    default_limit = 100
    default_offset = 0
    default_ordering = '-scoring'

    model = ProductCard
    serializer = ProductCardSerializer

    def get(self, request, *args, **kwargs):
        return Response({})


class ProductCardAPIView(APIView):
    """
    Класс для работы с отдельной сущностью карточки товара
    """
    model = ProductCard
    serializer = ProductCardSerializer

    def get(self, request, pk, *args, **kwargs):
        try:
            instance = self.model.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer(instance)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class ProductCardAttributesAPIView(APIView):
    """
    Класс отображения информации о карточке товара
    """
    def get(self, request, pk, *args, **kwargs):
        try:
            product = CubesProductCard.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        attrs = product.attributes
        items = {}
        for key, values in attrs.items():
            items[key.id] = list(map(lambda x: {'id': x.id, 'name': x.name}, values))
        content = {
            'attributes': items
        }
        return Response(content)

    def put(self, request, pk, *args, **kwargs):
        try:
            product = CubesProductCard.objects.get(pk=pk)
        except CubesProductCard.DoesNotExist:
            raise Http404

        product.height = int(request.data['height'])
        product.width = int(request.data['width'])
        product.length = int(request.data['depth'])
        product.weigh = int(request.data['weight'])

        product.save()

        recieved_attributes = request.data['attributes']
        recieved_values = set()
        for attribute in recieved_attributes:
            selected_values = attribute['selected_values']
            values_set = set(map(lambda x: x['id'], selected_values))
            recieved_values.update(values_set)
        stored_values = set(map(lambda x: x.id, product.attribute_values.all()))
        ids_to_delete = stored_values.difference(recieved_values)
        ids_to_add = recieved_values.difference(stored_values)
        relations_to_delete = product.attributevalues_relation_class.objects.filter(
                                product=product,
                                attribute_value__in=ids_to_delete
                            )
        deleted_count = relations_to_delete.count()
        added_count = 0

        relations_to_delete.delete()
        values_to_add = product.attributevalue_class.objects.filter(id__in=ids_to_add)
        for value in values_to_add:
            product.add_attribute_value(value)
            added_count += 1
        return Response({
            'deleted': deleted_count,
            'added': added_count
        })


class CubesProductCardImagesAPIView(APIView):

    def get(self, request, pk, *args, **kwargs):
        product = self.get_product(pk)
        additional_images = []
        for image in product.additional_images:
            additional_images.append({
                'id': image.id,
                'url': image.image.url,
                'order': image.order,
                'thumbnail': image.thumbnail.url
            })
        return Response({
            'additional': additional_images,
            'main': product.image.url,
            'thumbnail': product.thumbnail.url
        })

    def put(self, request, pk, *args, **kwargs):
        product = self.get_product(pk)
        changed = 0
        for instance in product.additional_images:
            order = request.data[str(instance.id)]['order']
            if order != instance.order:
                instance.order = order
                instance.save()
                changed += 1
        return Response({
            'changed': changed
        })

    def get_product(self, pk):
        try:
            product = CubesProductCard.objects.get(id=pk)
        except CubesProductCard.DoesNotExist:
            raise Http404
        return product


class CubesProductCardImageUploadAPIView(APIView):

    def get(self, request, pk, *args, **kwargs):
        self.check_permissions(request)
        task_id = request.GET.get('task_id')
        state = cache.get(task_id)
        return Response({
            'is_ready': state
        })

    def put(self, request, pk, *args, **kwargs):
        self.check_permissions(request)
        try:
            product = CubesProductCard.objects.get(id=pk)
        except CubesProductCard.DoesNotExist:
            raise Http404
        image_file = request.data.get('file', None)
        if image_file is not None:
            task_str = str(pk) + image_file.name
            task_id = md5(task_str.encode()).hexdigest()
            cache.set(task_id, False)
            product.replace_main_image_by_file(image_file)
            cache.set(task_id, True)
        else:
            image = request.data.get('image', None)
            if image is not None:
                task_str = str(pk) + image['url']
                task_id = md5(task_str.encode()).hexdigest()
                cache.set(task_id, False)
                product.replace_main_image_by_additional(image['id'])
                cache.set(task_id, True)
        return Response({
            'detail': 'acknowledged',
            'task_id': task_id
        })

    def check_permissions(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied


class ProductCardModificationsAPIView(APIView):

    model = ProductCard
    serializer = ProductCardSerializer

    def get(self, request, pk, *args, **kwargs):
        try:
            instance = self.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer(instance.modifications, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
