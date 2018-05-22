from api.core.views import (CategoryAPIView,
                            CategoryNodeListAPIView,
                            CategoryFiltersAPIView,
                            CategoryPriceAPIView,
                            CategoryNodeInputsAPIView,
                            CategoryNodeOutputsAPIView,
                            CategoryAdditionalNodesAPIView,
                            CategoryNodeAdditionalRelationAPIView,
                            CategoryNodeInputRelationAPIView)

from shop_cubes.models import CubesCategoryNode
from shop_cubes.serializers import CubesProductCardSerializer, CubesCategoryNodeSerializer


class CubesCategoryPriceAPIView(CategoryPriceAPIView):

    model = CubesCategoryNode


class CubesCategoryFiltersAPIView(CategoryFiltersAPIView):

    model = CubesCategoryNode


class CubesCategoryAPIView(CategoryAPIView):

    """
    Общий класс API-view для категории.
    В качестве параметра использует ID категории из url
    """
    model = CubesCategoryNode
    serializer = CubesCategoryNodeSerializer


class CubesCategoryNodeInputsAPIView(CategoryNodeInputsAPIView):

    """
    Класс для работы с входными узлами категории дерева
    """
    model = CubesCategoryNode
    Serializer = CubesCategoryNodeSerializer

    def get(self, request, pk, *args, **kwargs):
        try:
            instance = self.model.objects.get(id=pk)
        except self.model.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.Serializer(instance.inputs.all(), many=True)
        return Response(
            serializer.data,
        )


class CubesCategoryNodeOutputsAPIView(CategoryNodeOutputsAPIView):

    """
    Класс для работы с выходными узлами категории дерева
    """
    model = CubesCategoryNode
    Serializer = CubesCategoryNodeSerializer

    def get(self, request, pk, *args, **kwargs):
        try:
            instance = self.model.objects.get(id=pk)
        except self.model.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.Serializer(instance.outputs.all(), many=True)
        return Response(
            serializer.data,
        )


class CubesCategoryAdditionalNodesAPIView(CategoryAdditionalNodesAPIView):

    model = CubesCategoryNode
    serializer = CubesCategoryNodeSerializer


class CubesCategoryNodeListAPIView(CategoryNodeListAPIView):

    model = CubesCategoryNode
    serializer = CubesCategoryNodeSerializer
