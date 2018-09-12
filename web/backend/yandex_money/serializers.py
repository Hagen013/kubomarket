from core.serializers import DynamicFieldsModelSerializer

from .models import Payment


class PaymentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Payment
        fields = (
            'id',
            'user',
            'order',
            'uuid',
            'status',
            'pub_date',
            'customer_number',
            'order_amount',
            'payment_type',
            'order_number',
            'cps_email',
            'cps_phone',
            'is_payed',
            'url',
            'is_expired'
        )
        read_only_fields = (
            'id',
            'uuid',
            'status',
            'pub_date',
            'is_payed',
            'url',
            'is_expired'
        )
