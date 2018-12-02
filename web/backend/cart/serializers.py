from core.serializers import DynamicFieldsModelSerializer

from tasks.sms_notifications import sms_notify
from tasks.mail_notifications import mail_notify

from .models import Order2


class OrderSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Order2
        fields = (
            'id',
            'public_id',
            'data',
            'state',
            'source',
            'manager_notes',
            'client_notes',
            'created_at',
            'modified_at',
            'delivery_status',
            'user',
            'cpa'
        )
        read_only_fields = (
            'id',
            'user',
            'public_id'
        )


class OrderPrivateSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Order2
        fields = (
            'id',
            'public_id',
            'data',
            'state',
            'source',
            'manager_notes',
            'client_notes',
            'created_at',
            'modified_at',
            'delivery_status',
            'user',
            'cpa',
            'store'
        )
        read_only_fields = (
            'id',
            'user',
            'public_id'
        )
