from django.views.generic import TemplateView
from yandex_money.forms import PaymentForm
from yandex_money.models import Payment


class CartPageView(TemplateView):

    template_name = "pages/cart.html"


class PaymentPageView(TemplateView):
    template_name = 'payment.html'

    def get_context_data(self, **kwargs):
        payment = Payment(order_amount=123)
        payment.save()

        ctx = super(PaymentPageView, self).get_context_data(**kwargs)
        ctx['form'] = PaymentForm(instance=payment)
        return ctx
