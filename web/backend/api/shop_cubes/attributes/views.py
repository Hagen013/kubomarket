from api.core.views import (AttributeListAPIView,
                            AttributeAPIView,
                            AttributeValueListApiView,
                            AttributeValueApiView)


from shop_cubes.models import CubesAttribute, CubesAttributeValue
from shop_cubes.serializers import CubesAttributeSerializer, CubesAttributeValueSerializer


class CubesAttributeListAPIView(AttributeListAPIView):

    model = CubesAttribute
    serializer_class = CubesAttributeSerializer


class CubesAttributeAPIView(AttributeAPIView):

    model = CubesAttribute
    serializer = CubesAttributeSerializer


class CubesAttributeValueListApiView(AttributeValueListApiView):
    
    model = CubesAttributeValue
    serializer_class = CubesAttributeValueSerializer


class CubesAttributeValueApiView(AttributeValueApiView):
    
    model = CubesAttributeValue
    serializer_class = CubesAttributeValueSerializer
