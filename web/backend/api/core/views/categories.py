from django.http import Http404
from django.db.models import Max, Min, Count
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.postgres.search import SearchVector

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CategoryFiltersAPIView(APIView):

    """
    На текущем этапе реализованы фильтры по цене
    В дальнейшем при возникновении необходимости данный
    класс должен быть переопределен для выдачи всех необходимых
    фильтров
    """

    model = None

    def get(self, request, pk=None):
        try:
            category = self.model.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        price_lte = request.GET.get('price__lte', None)
        price_gte = request.GET.get('price__gte', None)
        if (price_lte is not None) and (price_gte is not None):
            try:
                price_lte = int(price_lte)
                price_gte = int(price_gte)
                return Response(
                    category.products.filter(price__lte=price_lte, price__gte=price_gte).values(
                        'vendor').annotate(count=Count('vendor')).order_by('-count')
                )
            except (ValueError, TypeError):
                pass
        return Response(
            category.products.values('vendor').annotate(count=Count('vendor')).order_by('-count'),
            status=status.HTTP_200_OK
        )


class CategoryPriceAPIView(APIView):

    """
    Класс API-view,  возвращающий максимальную и минимальную цены
    Вынесен в отдельный от базового API категории view в виду
    """

    model = None

    def get(self, request, pk=None):
        try:
            instance = self.model.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(instance.products.aggregate(Min('price'), Max('price')))


class CategoryAPIView(APIView):

    """
    Общий класс API-view для категории.
    В качестве параметра использует ID категории из url
    """
    model = None
    serializer = None

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

    def put(self, request, pk, *args, **kwargs):
        try:
            instance = self.model.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, pk, *args, **kwargs):
        return Response({
        })

    def delete(self, request, pk, *args, **kwargs):
        return Response({
        })


class CategoryNodeInputsAPIView(APIView):

    """
    Класс для работы с входными узлами категории дерева
    """
    model = None
    serializer = None

    def get(self, request, pk, *args, **kwargs):
        try:
            instance = self.model.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer(instance.inputs.all(), many=True)
        return Response(
            serializer.data,
        )

    def put(self, request, pk, *args, **kwargs):
        return Response({
        })

    def post(self, request, pk, *args, **kwargs):
        return Response({
        })

    def delete(self, request, pk, *args, **kwargs):
        return Response({
        })


class CategoryNodeOutputsAPIView(APIView):

    """
    Класс для работы с выходными узлами категории дерева
    """
    model = None
    serializer = None

    def get(self, request, pk, *args, **kwargs):
        try:
            instance = self.model.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer(instance.outputs.all(), many=True)
        return Response(
            serializer.data,
        )

    def put(self, request, pk, *args, **kwargs):
        return Response({
        })

    def post(self, request, pk, *args, **kwargs):
        return Response({
        })

    def delete(self, request, pk, *args, **kwargs):
        return Response({
        })


class CategoryAdditionalNodesAPIView(APIView):

    """
    Класс для работы с входными узлами категории дерева
    """

    model = None
    serializer = None

    def get(self, request, pk, *args, **kwargs):
        return Response({
        })

    def put(self, request, pk, *args, **kwargs):
        return Response({
        })

    def post(self, request, pk, *args, **kwargs):
        return Response({
        })

    def delete(self, request, pk, *args, **kwargs):
        return Response({
        })


class CategoryNodeInputRelationAPIView(APIView):

    """
    Класс для работы с M2M-таблицей основных связей дерева
    """

    model = None
    serializer = None

    def get(self, request, pk, *args, **kwargs):
        return Response({
        })

    def put(self, request, pk, *args, **kwargs):
        return Response({
        })

    def post(self, request, pk, *args, **kwargs):
        return Response({
        })

    def delete(self, requst, pk, *args, **kwargs):
        return Response({
        })


class CategoryNodeAdditionalRelationAPIView(APIView):

    """
    Класс для работы с M2M-таблицей дополнительных связей дерева
    """

    model = None
    serializer = None

    def get(self, request, pk, *args, **kwargs):
        return Response({
        })

    def put(self, request, pk, *args, **kwargs):
        return Response({
        })

    def post(self, request, pk, *args, **kwargs):
        return Response({
        })

    def delete(self, requst, pk, *args, **kwargs):
        return Response({
        })


class CategoryNodeListAPIView(APIView):

    """
    Класс для работы со списком категорий
    """

    default_limit = 100
    default_offset = 0
    default_ordering = 'level'

    model = None
    serializer = None

    def get(self, request, *args, **kwargs):
        ordering = request.GET.get('ordering', '_depth')
        offset = int(request.GET.get('offset', self.default_offset))
        limit = int(request.GET.get('limit', self.default_limit))
        search_query = request.GET.get('search', None)
        if search_query is None:
            qs = self.model.objects.all().order_by(ordering)[offset:limit]
            count = self.model.objects.all().count()
        else:
            qs = self.model.objects.annotate(search=SearchVector('name')).filter(search=search_query)
            count = qs.count()
            qs = qs[offset:limit]
        serializer = self.serializer(qs, many=True)
        return Response(
            {
                'count': count,
                'results': serializer.data
            },
            status=status.HTTP_200_OK
        )
