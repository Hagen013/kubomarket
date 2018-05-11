from api.core.views import AttributeListAPIView, AttributeAPIView
from shop_cubes.models import CubesAttribute
from shop_cubes.serializers import CubesAttributeSerializer


class CubesAttributeListAPIView(AttributeListAPIView):

    model = CubesAttribute
    serializer = CubesAttributeSerializer


class CubesAttributeAPIView(AttributeAPIView):

    model = CubesAttribute
    serializer = CubesAttributeSerializer
