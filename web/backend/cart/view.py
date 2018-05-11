from hashlib import md5

from django.views.generic import TemplateView, ListView, DetailView
from django.http import Http404
from django.conf import settings

from .models import Order2


API_URL = "https://payments.demo.paysecure.ru/pay/order.cfm"
MERCHANT_ID = settings.MERCHANT_ID


class AssistPayment(TemplateView):
    template_name = 'assistpayment.html'
    context_object_name = 'products'

    def post(self, request, *args, **kwargs):
        self.order = self.get_order()
        return super(AssistPayment, self).post(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.order = self.get_order()
        return super(AssistPayment, self).get(self, request, *args, **kwargs)

    def get_order(self):
        pk = self.kwargs.get('pk')
        key = self.kwargs.get('key')
        try:
            order = Order2.objects.get(pk=pk)
            if order.assist_key == key:
                return order
            else:
                raise Http404
        except Order2.DoesNotExist:
            raise Http404

    def get_context_data(self, *args, **kwargs):
        context = super(AssistPayment, self).get_context_data(**kwargs)
        context['order'] = self.order
        context['assist'] = {
            "API_URL": API_URL,
            "Merchant_ID": MERCHANT_ID,
            "OrderNumber": self.order.id,
            "OrderAmount": self.order.total_price,
            "LastName": self.order.data['customer']['name'],
            "Email": self.order.data['customer']['email'],
        }
        return context
