from hashlib import md5
import uuid
import time

from django.core.cache import cache
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from shop_cubes.models import CubesProductCard
from shop_cubes.models import CubesAttribute
from shop_cubes.models import CubesAttributeValue
from core.models import ProductCard
from core.serializers import ProductCardSerializer
from tasks.images import save_description_image


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
    attribute_class = CubesAttribute

    def check_permissions(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied

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
            items[key.id] = list(map(lambda x: {'id': x.id, 'name': x.name, 'value': x.value}, values))
        content = {
            'attributes': items
        }
        return Response(content)

    def put(self, request, pk, *args, **kwargs):
        self.check_permissions(request)

        try:
            product = CubesProductCard.objects.get(pk=pk)
        except CubesProductCard.DoesNotExist:
            raise Http404

        product.height = int(request.data['height'])
        product.width = int(request.data['width'])
        product.length = int(request.data['depth'])
        product.description = request.data['description']

        product.save()
        stored_non_int_values = {value for value in product.attribute_values.all() if value.attribute_type != 3}
        stored_attribtes_ids = {value.attribute.id for value in stored_non_int_values}

        attributes = request.data['attributes']
        int_attributes = list(filter(lambda x: x['attribute_type'] == 3, attributes))
        non_int_attributes = list(filter(lambda x: x['attribute_type'] != 3, attributes))

        for attribute in int_attributes:
            values_list = attribute['selected_values']
            if len(values_list) > 0:
                value = values_list[0]
                if type(value) != dict:
                    if value == '':
                        # Удаление связи
                        values_to_delete = product.attribute_values.filter(attribute__id=attribute['id'])
                        product.del_attribute_values(values_to_delete)
                    else:
                        # Добавление/перерисовка связи
                        attribute_found = True
                        try:
                            attribute = self.attribute_class.objects.get(
                                id=attribute['id'],
                                attribute_type=3
                            )
                        except ObjectDoesNotExist:
                            attribute_found = False
                        if attribute_found:
                            try:
                                product.set_int_value(value, attribute)
                            except ValueError:
                                pass

        recieved_values = set()
        for attribute in non_int_attributes:
            selected_values = attribute['selected_values']
            values_set = set(map(lambda x: x['id'], selected_values))
            recieved_values.update(values_set)

        values_ids = {value.id for value in stored_non_int_values}
        ids_to_delete = values_ids.difference(recieved_values)
        ids_to_add = recieved_values.difference(values_ids)
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


class ProductCardDescriptionImagesAPIView(APIView):

    allowed_image_extensions = {'jpg', 'png', 'jpeg'}

    def get(self, request, pk, *args, **kwargs):
        self.check_permissions(request)
        task_id = request.GET.get('task_id')
        state = cache.get(task_id)
        return Response({
            'is_ready': state
        })

    def post(self, request, pk, *args, **kwargs):
        self.check_permissions(request)
        image_file = request.FILES['file']
        task_id = self.get_task_id(image_file.name)
        filename = self.get_hashed_filename(image_file.name, task_id)
        print(filename)
        if filename is None:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        cache.set(task_id, False)
        save_description_image(image_file, filename)
        cache.set(task_id, True)
        return Response({
            'detail': 'acknowledged',
            'filename': filename,
            'task_id': task_id
        })

    def check_permissions(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied

    def get_task_id(self, filename):
        value = str(time.time()) + filename
        hashed = md5(value.encode()).hexdigest()
        return hashed
        
    def get_hashed_filename(self, filename, taks_id):
        extension = filename.split('.')[-1]
        print(extension)
        if extension not in self.allowed_image_extensions:
            return None
        else:
            return "{0}.{1}".format(
                taks_id,
                extension
            )

            
