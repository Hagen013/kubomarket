from django.conf import settings
from django.db import transaction

from config.celery import app
from celery.schedules import crontab

from cart.models import Order2
from delivery.cdek import Client as ClientSDEK
from delivery.pickpoint import Client as ClientPickpoint
from delivery.rupost import Client as ClientRupost
from cart.serializers import OrderSerializer
from cart.utils import pickpoint_to_cdek_code, rupost_to_cdek_code


@app.task
def sync_sdek_orders(pks):
    errors = []
    invalid = []
    
    qs = Order2.objects.filter(public_id__in=pks)
    client = ClientSDEK(settings.SDEK_USER, settings.SDEK_PASSWORD)
    serializer = OrderSerializer(qs, many=True)
    results = client.get_orders_statuses(serializer.data)['Order']
    with transaction.atomic():
        for order in results:
            error_code = order.get('ErrorCode', None)
            if error_code is not None:
                error_item = {
                    "Number": order['Number'],
                    "ErrorCode": order['ErrorCode'],
                    "Msg": order['Msg']
                }
                errors.append(error_item)
            else:
                dispatch_number = order['DispatchNumber']
                order_id = order['Number']
                if len(order_id) > 4:
                    order_id = "KU" + order_id
                status_description = order['Status']['Description']
                cdek_status_code = int(order['Status']['Code'])
                status_date = order['Status']['Date']
                
                instance = Order2.objects.get(public_id=order_id)
                instance.delivery_status['service'] = "sdek"
                instance.delivery_status['change_date'] = status_date
                instance.delivery_status['dispatch_number'] = dispatch_number
                instance.delivery_status['state_description'] = status_description
                instance.delivery_status['service_status_code'] = cdek_status_code
                instance.delivery_status['status_code'] = cdek_status_code
                instance.delivery_status['history'] = []
                for snapshot in order['Status']['State']:
                    item = {
                        "change_date": snapshot['Date'],
                        "state_description": snapshot['Description'],
                        "service_status_code": snapshot['Code'],
                        "city_code": snapshot['CityCode']
                    }
                    instance.delivery_status['history'].append(item)
                if cdek_status_code == 4:
                    instance.state = "вручен"
                instance.save()

    return errors


@app.task
def sync_pickpoint_orders(pks):
    error_pks = []
    empty_pks = []
    error_tracking_pks = []
    empty_tracking_pks = []
    invalid = []
    orders = []
    count = 0

    client = ClientPickpoint(settings.PICKPOINT_USER, settings.PICKPOINT_PASSWORD)
    client.login()

    for pk in pks:
        invoice_pk = pk
        if invoice_pk.startswith('KU'):
            invoice_pk = invoice_pk[2:]
            
        info_response = client.get_order_info(invoice_pk)
        if info_response.status_code == 200:
            result = info_response.json()
            if len(result) !=0:
                result = result[0]
                invoice_number = result['InvoiceNumber']
                invoice_sum = float(result['Sum'].replace(',', '.'))
                track_response = client.track_sending(invoice_number)
                if track_response.status_code == 200:
                    track_result = track_response.json()
                    if len(track_result) != 0:
                        last_status = track_result[-1]
                        last_status = track_result[-1]
                        change_date = last_status['ChangeDT']
                        state_message = last_status['StateMessage']
                        status_code = int(last_status['State'])
                        instance = {
                            "id": pk,
                            "service": "pickpoint",
                            "change_date": change_date,
                            "dispatch_number": invoice_number,
                            "state_description": state_message,
                            "service_status_code": status_code,
                            "status_code": pickpoint_to_cdek_code(status_code),
                            "sum": invoice_sum,
                            "history": []
                        }
                        for state in track_result:
                            history_state = {
                                "change_date": state['ChangeDT'],
                                "state_description": state['StateMessage'],
                                "service_status_code": state['State'],
                            }
                            instance['history'].append(history_state)
                        orders.append(instance)
                    else:
                        empty_tracking_pks.append(pk)
                else:
                    error_tracking_pks.append(pk)
            else:
                empty_pks.append(pk)
        else:
            error_pks.append(pk)

        
    with transaction.atomic():
        for item in orders:
            instance = Order2.objects.get(public_id=item['id'])
            item.pop('id')
            instance.delivery_status = item
            if instance.delivery_status['service_status_code'] == 111:
                instance.state = 'вручен'
            instance.save()
            count += 1
            
    return {
        "error_pks": error_pks,
        "empty_pks": empty_pks,
        "error_tracking_pks": error_tracking_pks,
        "empty_tracking_pks": empty_tracking_pks,
        "invalid": invalid,
        "count": count
    }


@app.task
def sync_postal_orders(pks):
    qs = Order2.objects.filter(public_id__in=pks)
    client = ClientRupost(settings.RUPOST_USER, settings.RUPOST_PASSWORD)
    for instance in qs:
        service = instance.delivery_status['service']
        if service == "rupost":
            dispatch_number = instance.delivery_status['dispatch_number']
            tracking_history = client.get_operation_history(dispatch_number)

            finance_parameters_list = list(map(lambda x: x['FinanceParameters'], tracking_history))
            finance_parameters_list = list(filter(lambda x: x['Payment'] is not None, finance_parameters_list))
            invoice_sum = finance_parameters_list[0]['Payment']
            invoice_sum = float(str(invoice_sum)[:-2])

            last_state = tracking_history[-1]
            operation_parameters = last_state['OperationParameters']
            oper_type = operation_parameters['OperType']
            oper_attribute = operation_parameters['OperAttr']
            oper_date = str(operation_parameters['OperDate'])
            state_description = "{0} ({1})".format(
                oper_type['Name'],
                oper_attribute['Name']
            )
            instance.delivery_status['state_description'] = state_description
            instance.delivery_status['service_status_code'] = oper_type['Id']
            instance.delivery_status['status_code'] = rupost_to_cdek_code(oper_type['Id'])
            instance.delivery_status['change_date'] = oper_date
            instance.delivery_status['sum'] = invoice_sum

            history = []
            for item in tracking_history:
                history_state_description = "{0} ({1})".format(
                    item['OperationParameters']['OperType']['Name'],
                    item['OperationParameters']['OperAttr']['Name']
                )
                history_log_item = {
                    "state_description": history_state_description,
                    "change_date": str(item['OperationParameters']['OperDate']),
                    "service_status_code": item['OperationParameters']['OperType']['Id']
                }
                history.append(history_log_item)
            instance.delivery_status['history'] = history
            instance.save


def sort_orders_by_delivery_service():
    sdek_orders_pks = []
    pickpoint_orders_pks = []
    postal_orders_pks = []
    unknown = []
    
    qs = Order2.objects.all().order_by('-created_at')
    for instance in qs:
        if instance.data['delivery']['is_mod_selected']:
            delivery_type = instance.data['delivery']['mod']['type']
            if delivery_type == 'curier':
                sdek_orders_pks.append(instance.public_id)
            elif delivery_type == 'postal_service':
                postal_orders_pks.append(instance.public_id)
            elif delivery_type == 'delivery_points':
                code = instance.data['delivery']['mod']['code']
                if code is not None:
                    if 'sdek' in code:
                        sdek_orders_pks.append(instance.public_id)
                    else:
                        pickpoint_orders_pks.append(instance.public_id)
                else:
                    sdek_orders_pks.append(instance.public_id)
            else:
                # Unknown delivery_type
                unknown.append(pk)
    return {
        "sdek": sdek_orders_pks,
        "pickpoint": pickpoint_orders_pks,
        "rupost": postal_orders_pks
    }


@app.task
def sync_delivery_statuses():
    sorted_pks = sort_orders_by_delivery_service()
    sync_sdek_orders.delay(sorted_pks['sdek'])
    sync_pickpoint_orders.delay(sorted_pks['pickpoint'])
    sync_postal_orders.delay(sorted_pks['rupost'])


app.add_periodic_task(
    crontab(minute=0,  hour='*/12'),
    sync_delivery_statuses.s(),
    name='sync_delivery_statuses',
)
