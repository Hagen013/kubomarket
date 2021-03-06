from rest_framework_elasticsearch.es_serializer import ElasticSerializer
from rest_framework import serializers
from rest_framework.fields import empty

from .search_indexes import ProductCardIndex, CategoryIndex


class ElasticGenericSerializer(ElasticSerializer):

    def es_instance(self):
        return self.es_repr(self.data)


class ElasticProductCardSerializer(ElasticGenericSerializer):

    class Meta:
        es_model = ProductCardIndex

    id = serializers.IntegerField()
    offer_identifier = serializers.CharField()
    name = serializers.CharField()
    absolute_url = serializers.CharField()
    price = serializers.IntegerField()
    vendor = serializers.CharField()
    search_scoring = serializers.IntegerField()
    vendor_code = serializers.CharField()
    image = serializers.ImageField(use_url=True)
    thumbnail = serializers.ImageField(use_url=True)


class ElasticProductCardCustomSerializer:

    class Meta:
        es_model = ProductCardIndex
        fields = [
            "id",
            "offer_identifier",
            "name",
            "absolute_url",
            "price",
            "vendor",
            "search_scoring",
            "vendor_code"
        ]

    def __init__(self, instance):
        self.instance = instance

    def to_representation(self, instance):
        representation = {}
        for field in self.Meta.fields:
            representation[field] = str(getattr(instance, field))
            representation['image'] = instance.image.url,
            representation['thumbnail'] = instance.thumbnail.url
            representation['is_in_stock'] = str(instance.is_in_stock).lower()
        for value in instance.attribute_values.all():
            attribute = value.attribute
            key = attribute.key
            if key not in representation.keys():
                representation[key] = [value.id, ]
            else:
                representation[key].append(value.id)
        return representation

    def save(self, using=None, index=None, validate=True, **kwargs):
        instance = self.es_instance()
        instance.save(using=using, index=index, validate=validate, **kwargs)

    def delete(self, using=None, index=None, **kwargs):
        instance = self.es_instance()
        instance.delete(using=using, index=index, **kwargs)

    def get_es_model(self):
        if not hasattr(self.Meta, 'es_model'):
            raise ValueError(
                'Can not find es_model value'
            )
        return self.Meta.es_model

    def get_es_instance_pk(self, data):
        try:
            return getattr(data, 'id')
        except KeyError:
            raise ValueError(
                'Can not save object without id'
            )

    def es_repr(self):
        data = self.to_representation(self.instance)
        data['meta'] = dict(id=self.get_es_instance_pk(self.instance))
        model = self.get_es_model()
        return model(**data)

    def es_instance(self):
        return self.es_repr()
