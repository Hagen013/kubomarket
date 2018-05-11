from rest_framework import serializers

from cart.models import Order2


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order2
        fields = (
            'id',
            'data',
            'state',
            'source',
            'manager_notes',
            'created_at',
            'modified_at'
        )
