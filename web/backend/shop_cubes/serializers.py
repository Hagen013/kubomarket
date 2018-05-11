from core.serializers import (ProductCardSerializer,
                              CategoryNodeSerializer,
                              CategoryNodeInputRelationSerializer,
                              CategoryNodeAdditionalRelationSerializer,
                              CategoryNodeGroupSerializer,
                              AttributeSerializer,
                              AttributeValueSerializer)
from shop_cubes.models import (CubesProductCard,
                              CubesCategoryNode,
                              CubesCategoryNodeGroup,
                              CubesAttribute,
                              CubesAttributeValue)


class CubesProductCardSerializer(ProductCardSerializer):

    class Meta(ProductCardSerializer.Meta):
        model = CubesProductCard


class CubesCategoryNodeSerializer(CategoryNodeSerializer):

    class Meta(CategoryNodeSerializer.Meta):
        model = CubesCategoryNode


class CubesAttributeValueSerializer(AttributeValueSerializer):

    class Meta(AttributeValueSerializer.Meta):
        model = CubesAttributeValue


class CubesAttributeSerializer(AttributeSerializer):

    # переопределяем поле для работы с ModelSerializer, использующим
    # не абстрактную модель
    values = CubesAttributeValueSerializer(many=True)

    class Meta(AttributeSerializer.Meta):
        model = CubesAttribute


class CubesCategoryNodeInputRelationSerializer(CategoryNodeInputRelationSerializer):
    pass


class CubesCategoryNodeAdditionalRelationSerializer(CategoryNodeAdditionalRelationSerializer):
    pass


class CubesCategoryNodeGroupSerializer(CategoryNodeGroupSerializer):
    
    class Meta(CategoryNodeGroupSerializer.Meta):
        model = CubesCategoryNodeGroup
