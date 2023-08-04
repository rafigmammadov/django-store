import stripe

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy

from http import HTTPStatus

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
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1NbM0NHq11uemsKDDxnJIggJ',
                    'quantity': 1,
                },
            ],
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
