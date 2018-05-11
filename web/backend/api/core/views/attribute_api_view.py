from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AttributeAPIView(APIView):
    """
    Базовый класс vie для отображения атрибута по id, обновления и удаления записии
    Для работы необходимо определить не абстрактный класс атрибута и его сериализатор
    """
    model = None
    serializer = None

    def get(self, request, pk, *args, **kwargs):
        try:
            instance = self.model.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer(instance)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
    # def put(self, request, pk, *args, **kwargs):
    #     return Response({})

    # def delete(self, request, pk, *args, **kwargs):
    #     return Response({})
