from rest_framework import serializers

from .models import (Attribute,
                     AttributeValue,
                     ProductCard)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    Serializer модели, принимающий дополнительный аргумент
    'disallowed_fields', который специфицирует неиспользуемые для
    сериализации поля
    """
    def __init__(self, *args, **kwargs):
        # Исключаем из аргументов класса-родителя аргументы полей
        fields = kwargs.pop('fields', None)
        disallowed_fields = kwargs.pop('disallowed_fields', None)

        # Инициализация ModelSerializer
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        _fields = None
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            _fields = existing.difference(allowed)
        elif disallowed_fields is not None:
            disallowed = set(disallowed_fields)
            existing = set(self.fields)
            _fields = existing.intersection(disallowed)

        if _fields is not None:
            for field in _fields:
                self.fields.pop(field)


class ProductCardSerializer(DynamicFieldsModelSerializer):

    image = serializers.ImageField(use_url=True)
    thumbnail = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductCard
        fields = (
            'id',
            'offer_identifier',
            'name',
            'absolute_url',
            'price',
            'vendor',
            'search_scoring',
            'vendor_code',
            'image',
            'thumbnail'
        )


class ProductCardStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCard
        fields = (
            'vendor_code',
            'amount',
            'stored'
        )


class CategoryNodeInputRelationSerializer(serializers.Serializer):

    input_node = serializers.IntegerField(source='input_node.id')
    output_node = serializers.IntegerField(source='output_node.id')


class CategoryNodeAdditionalRelationSerializer(serializers.Serializer):
    
    input_node = serializers.IntegerField(source='input_node.id')
    output_node = serializers.IntegerField(source='output_node.id')


class AttributeValueSerializer(DynamicFieldsModelSerializer):
    
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    slug = serializers.CharField()
    attribute = serializers.IntegerField(source='attribute_id')
    attribute_type = serializers.IntegerField()
    value = serializers.CharField()
    
    class Meta:
        fields = (
            'id',
            'name',
            'slug',
            'attribute',
            'attribute_type',
            'value'
        )
        read_only_fields = (
            'id',
        )


class AttributeSerializer(DynamicFieldsModelSerializer):
    
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    key = serializers.CharField()
    attribute_type = serializers.IntegerField()
    values = AttributeValueSerializer(many=True, read_only=True, required=False)
    unit = serializers.CharField(allow_blank=True)
    
    class Meta:
        fields = (
            'id',
            'name',
            'key',
            'attribute_type',
            'unit',
            'values'
        )
        read_only_fields = (
            'id',
            'values'
        )

    def create(self, validated_data):
        values = validated_data.pop("values")
        return super(AttributeSerializer, self).create(validated_data)


    def update(self, instance, validated_data):
        values = validated_data.pop("values")
        return super(AttributeSerializer, self).update(instance, validated_data)


class CategoryNodeGroupSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        fields = (
            "id",
            "name",
            "order"
        )


class CategoryNodeSerializer(DynamicFieldsModelSerializer):

    _title = serializers.CharField()
    absolute_url = serializers.CharField()
    level = serializers.IntegerField()
    depth = serializers.IntegerField()
    attribute_values = AttributeValueSerializer(required=False)

    class Meta:
        fields = (
            'id',
            'name',
            '_title',
            '_meta_title',
            '_meta_keywords',
            '_meta_description',
            'url',
            'absolute_url',
            'level',
            'depth',
            'scoring',
            'search_scoring',
            'description',
            'parent',
            'attribute_values'
        )
        read_only_fields = (
            'id',
            'url',
            'absolute_url',
            'level',
            'depth',
            'parent'
        )
    
    ## СРОЧНЫЕ КОСТЫЛИ
    def update(self, instance, validated_data):
        name = validated_data["name"]
        _title = validated_data["_title"]
        _meta_title = validated_data["_meta_title"]
        _meta_description = validated_data["_meta_description"]
        _meta_keywords = validated_data["_meta_keywords"]
        description = validated_data["description"]
        scoring = validated_data["scoring"]
        search_scoring = validated_data["search_scoring"]

        instance._title = _title
        instance.name = name
        instance.search_scoring = search_scoring
        instance.scoring = scoring
        instance._meta_title = _meta_title
        instance._meta_keywords = _meta_keywords
        instance._meta_description = _meta_description
        instance.description = description

        instance.save()
        return instance


class ProductVideoReviewSerializer(DynamicFieldsModelSerializer):

    order = serializers.IntegerField(required=False)

    class Meta:
        fields = (
            'id',
            'youtube_code',
            'product',
            'created_at',
            'modified_at',
            'order',
            'url'
        )
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'url'
        )


class PublicProductCardReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'user',
            'product',
            'content',
            'rating',
            'status',
            'created_at'
        )
        read_only_fields = (
            'id',
            'status',
            'created_at'
        )


class PrivateProductCardReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'user',
            'product',
            'content',
            'rating',
            'status',
            'created_at'
        )
        read_only_fields = (
            'id',
            'created_at'
        )
