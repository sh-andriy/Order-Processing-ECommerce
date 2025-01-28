from django.urls import path
from .views import checkout_order, process_payment, confirm_delivery, sync_orders_from_external

urlpatterns = [
    path('order/checkout/', checkout_order, name='checkout_order'),
    path('order/payment/', process_payment, name='process_payment'),
    path('order/confirm-delivery/', confirm_delivery, name='confirm_delivery'),
    path('order/sync-external/', sync_orders_from_external, name='sync_orders_from_external'),
]
