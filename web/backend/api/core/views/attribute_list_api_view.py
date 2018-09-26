from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AttributeListAPIView(APIView):
    """
    Базовый класс view для отображения списка атрибутов и создания новых
    сущностей с помощью http-метода post
    Для работы необходимо определить не абстрактный класс атрибута и его сериализатор
    """
    model = None
    serializer_class = None

    def get(self, request, *args, **kwargs):
        qs = self.model.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
