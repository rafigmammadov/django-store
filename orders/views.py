from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from orders.forms import OrderCreateForm
from orders.models import Order
from products.models import Basket


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
            success_url=f"{settings.DOMAIN_NAME}{reverse('orders:success')}?order_id={self.object.id}",
            cancel_url=f"{settings.DOMAIN_NAME}{reverse('orders:cancel')}"
        )
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
    print(payload)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
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


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        if order.basket_history and order.basket_history.get('purchased_items'):
            items = order.basket_history['purchased_items']
            total = order.basket_history.get('total_sum', 0)
        else:
            # fallback if no basket_history
            baskets = Basket.objects.filter(user=order.initiator)
            items = [basket.de_json() for basket in baskets]
            total = baskets.total_sum()

        context['order_items'] = items
        context['total'] = total
        context['title'] = f'Store - Order №{order.id}'
        return context


class OrdersListView(ListView):
    template_name = 'orders/orders.html'
    queryset = Order.objects.all()
    ordering = '-id'

    def get_queryset(self):
        queryset = super(OrdersListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


    def get_context_data(self, **kwargs):
        context = super(OrdersListView, self).get_context_data()
        context['title'] = 'Store - Orders'
        return context


class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.GET.get('order_id')
        order = None
        if order_id:
            try:
                order = Order.objects.get(pk=order_id)
            except Order.DoesNotExist:
                order = None

        if order and order.basket_history and order.basket_history.get('purchased_items'):
            items = order.basket_history['purchased_items']
            total = order.basket_history.get('total_sum', 0)
        elif order:
            # Show current basket as fallback
            baskets = Basket.objects.filter(user=order.initiator)
            items = [basket.de_json() for basket in baskets]
            total = baskets.total_sum()
        else:
            items = []
            total = 0

        context['order'] = order
        context['order_items'] = items
        context['total'] = total
        context['title'] = 'Store - The successful order'
        return context


class CanceledTemplateView(TemplateView):
    template_name = 'orders/cancel.html'
