from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from products.models import Basket
from orders.forms import OrderCreateForm
from orders.models import Order


class CreateOrderTemplateView(CreateView):
    model = Order
    template_name = 'orders/order-create.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('orders:success')

    stripe.api_key = settings.STRIPE_SECRET_KEY


    def post(self, request, *args, **kwargs):
        super(CreateOrderTemplateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        line_items = []
        for basket in baskets:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url=f"{settings.DOMAIN_NAME}{reverse('orders:success')}",
            cancel_url=f"{settings.DOMAIN_NAME}{reverse('orders:cancel')}")

        return HttpResponseRedirect(checkout_session.url, HTTPStatus.SEE_OTHER)

    def get_context_data(self, **kwargs):
        context = super(CreateOrderTemplateView, self).get_context_data()
        context['title'] = 'Store - Creating Order'
        return context

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(CreateOrderTemplateView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    event = None
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    print(payload)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'checkout.session.completed':
        checkout_session_id = int(event.data.object.metadata.order_id)
        order = Order.objects.get(id=checkout_session_id)
        order.update_after_payment()
        print("Payment is successful!")
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(HTTPStatus.OK)


class OrderTemplateView(TemplateView):
    template_name = 'orders/order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderTemplateView, self).get_context_data()
        context['title'] = 'Store - Order'


class OrdersTemplateView(TemplateView):
    template_name = 'orders/orders.html'

    def get_context_data(self, **kwargs):
        context = super(OrdersTemplateView, self).get_context_data()
        context['title'] = 'Store - Orders'


class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'

    def get_context_data(self, **kwargs):
        context = super(SuccessTemplateView, self).get_context_data()
        context['title'] = 'Store - The successful order'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/cancel.html'
