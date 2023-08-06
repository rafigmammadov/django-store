from django.urls import path

from orders.views import (CanceledTemplateView, CreateOrderTemplateView,
                          OrdersTemplateView, OrderTemplateView,
                          SuccessTemplateView)

app_name = 'orders'

urlpatterns = [
    path('order_create', CreateOrderTemplateView.as_view(), name='order_create'),
    path('orders', OrdersTemplateView.as_view(), name='orders'),
    path('order', OrderTemplateView.as_view(), name='order'),
    path('success', SuccessTemplateView.as_view(), name='success'),
    path('cancel', CanceledTemplateView.as_view(), name='cancel')
]
