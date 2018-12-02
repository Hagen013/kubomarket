from datetime import datetime

from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.conf import settings

from yandex_money.forms import PaymentForm
from yandex_money.models import Payment

from .models import Order2


class CartPageView(TemplateView):

    template_name = "pages/cart.html"


class PaymentPageView(TemplateView):

    template_name = 'payment/payment.html'
    model = Payment

    def get_payment(self, uuid):
        try:
            instance = self.model.objects.get(uuid=uuid)
            if instance.is_expired:
                raise Http404
            return instance
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, uuid, *args, **kwargs):
        self.payment = self.get_payment(uuid)
        return super(PaymentPageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PaymentPageView, self).get_context_data(**kwargs)
        context['payment'] = self.payment
        context['order'] = self.payment.order
        context['shopId'] = settings.YANDEX_MONEY_SHOP_ID
        context['scid'] = settings.YANDEX_MONEY_SCID
        context['form'] = PaymentForm(instance=self.payment)
        return context



class TestView(TemplateView):

    template_name = "receipt.html"

    def get_context_data(self, *args, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        instance = Order2.objects.get(public_id="KU1894091840")
        context['order'] = instance
        context['date'] = datetime.now().strftime("%d.%m.%Y")
        return context