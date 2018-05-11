from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CategoryNodeGroupAPIView(APIView):
    
    model = None
    serializer = None

    def get(self, request, pk):
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


class CategoryNodeGroupValuesAPIView(APIView):
    """
    Класс, отображающий при GET запросе список AttriuteValue,
    связанный cо списком Attribute, имеюших в качестве foreign-key
    id CategoryNodeGroup, указанной в url запроса
    """

    model = None
    attribute_model = None

    value_model = None
    value_serializer = None

    def get(self, request, pk):
        values = self.value_model.objects.filter(
            attribute__in=self.attribute_model.objects.filter(
                category_node_group=pk
            )
        )
        serializer = self.value_serializer(values, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
