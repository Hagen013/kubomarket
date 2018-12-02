from rest_framework import serializers

from django.contrib.auth.models import User

from core.serializers import (ProductCardSerializer,
                              ProductCardStoreSerializer,
                              CategoryNodeSerializer,
                              CategoryNodeInputRelationSerializer,
                              CategoryNodeAdditionalRelationSerializer,
                              CategoryNodeGroupSerializer,
                              AttributeSerializer,
                              AttributeValueSerializer,
                              ProductVideoReviewSerializer,
                              PublicProductCardReviewSerializer,
                              PrivateProductCardReviewSerializer)

from shop_cubes.models import (CubesProductCard,
                              CubesCategoryNode,
                              CubesCategoryNodeGroup,
                              CubesAttribute,
                              CubesAttributeValue,
                              CubesProductVideoReview,
                              CubesProductCardReview
                              )
from users.serializers import UserSerializer


class CubesProductCardSerializer(ProductCardSerializer):

    class Meta(ProductCardSerializer.Meta):
        model = CubesProductCard


class CubesProductCardStoreSerializer(ProductCardStoreSerializer):

    class Meta(ProductCardStoreSerializer.Meta):
        model = CubesProductCard


class CubesAttributeValueSerializer(AttributeValueSerializer):

    class Meta(AttributeValueSerializer.Meta):
        model = CubesAttributeValue


class CubesCategoryNodeSerializer(CategoryNodeSerializer):

    attribute_values = CubesAttributeValueSerializer(many=True, required=False)

    class Meta(CategoryNodeSerializer.Meta):
        model = CubesCategoryNode


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


class CubesProductVideoReviewSerializer(ProductVideoReviewSerializer):

    product = serializers.PrimaryKeyRelatedField(queryset=CubesProductCard.objects.all())

    class Meta(ProductVideoReviewSerializer.Meta):
        model = CubesProductVideoReview


class PublicCubesProductCardReviewSerializer(PublicProductCardReviewSerializer):

    product = serializers.PrimaryKeyRelatedField(queryset=CubesProductCard.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta(PublicProductCardReviewSerializer.Meta):
        model = CubesProductCardReview


class PrivateCubesProductCardReviewSerializer(PrivateProductCardReviewSerializer):

    product = CubesProductCardSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta(PrivateProductCardReviewSerializer.Meta):
        model = CubesProductCardReview
        read_only_fields = (
            "id",
            "product",
            "user"
        )
