from collections import defaultdict

from rest_framework.views import APIView
from rest_framework.response import Response

from api.core.views import AttributeListAPIView, AttributeAPIView
from shop_cubes.serializers import CubesAttributeValueSerializer
from shop_cubes.models import CubesAttributeValue


# class CubesAttributeValueListAPIView(AttributeListAPIView):

#     model = CubesAttributeValue
#     serializer = CubesAttributeValueSerializer


class CubesAttributeValueListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        av_set = CubesAttributeValue.objects.values('attribute', 'id', 'name').order_by('attribute')
        av_mapping = defaultdict(list)
        for item in av_set:
            instance = {}
            instance['id'] = item['id']
            instance['name'] = item['name']
            av_mapping[item['attribute']].append(instance)
        return Response(av_mapping)


class CubesAttributeValueAPIView(AttributeAPIView):

    model = CubesAttributeValue
    serializer = CubesAttributeValueSerializer
