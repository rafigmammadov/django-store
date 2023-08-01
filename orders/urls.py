from django.urls import path
from orders.views import CreateOrderTemplateView, OrderTemplateView, OrdersTemplateView, SuccessTemplateView

app_name = 'orders'


urlpatterns = [
    path ('order_create', CreateOrderTemplateView.as_view(), name='order_create' ),
    path ('orders', OrdersTemplateView.as_view(), name='orders' ),
    path ('order', OrderTemplateView.as_view(), name='order' ),
    path ('success',SuccessTemplateView.as_view(), name='success' ),
]