from django.urls import path

from orders.views import (CanceledTemplateView, CreateOrderTemplateView,
                          OrderDetailView, OrdersListView, SuccessTemplateView)

app_name = 'orders'

urlpatterns = [
    path('order_create', CreateOrderTemplateView.as_view(), name='order_create'),
    path('orders_list', OrdersListView.as_view(), name='orders_list'),
    path('order_detail/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('success', SuccessTemplateView.as_view(), name='success'),
    path('cancel', CanceledTemplateView.as_view(), name='cancel')
]
