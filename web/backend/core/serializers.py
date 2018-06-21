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


class CategoryNodeSerializer(DynamicFieldsModelSerializer):

    level = serializers.IntegerField()
    depth = serializers.IntegerField()

    class Meta:
        fields = (
            'id',
            'name',
            'title',
            '_meta_title',
            '_meta_keywords',
            '_meta_description',
            'url',
            'absolute_url',
            'level',
            'depth',
            'scoring',
            'search_scoring'
        )


class CategoryNodeInputRelationSerializer(serializers.Serializer):

    input_node = serializers.IntegerField(source='input_node.id')
    output_node = serializers.IntegerField(source='output_node.id')


class CategoryNodeAdditionalRelationSerializer(serializers.Serializer):
    
    input_node = serializers.IntegerField(source='input_node.id')
    output_node = serializers.IntegerField(source='output_node.id')


class AttributeValueSerializer(DynamicFieldsModelSerializer):
    
    id = serializers.IntegerField()
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


class AttributeSerializer(DynamicFieldsModelSerializer):
    
    id = serializers.IntegerField()
    name = serializers.CharField()
    key = serializers.CharField()
    attribute_type = serializers.IntegerField()
    category_node_group = serializers.IntegerField(source='category_node_group_id')
    values = AttributeValueSerializer(many=True)
    
    class Meta:
        fields = (
            'id',
            'name',
            'key',
            'attribute_type',
            'category_node_group',
            'values'
        )


class CategoryNodeGroupSerializer(DynamicFieldsModelSerializer):
    
    class Meta:
        fields = (
            "id",
            "name",
            "order"
        )
