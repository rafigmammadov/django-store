from django.shortcuts import render
from django.views.generic.base import TemplateView

class CreateOrderTemplateView(TemplateView):
    template_name = 'orders/order-create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateOrderTemplateView, self).get_context_data()
        context['title'] = 'Store - Creating Order'

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
