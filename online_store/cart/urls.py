from django.urls import path
from .views import create_cart, add_item_to_cart, apply_promotion_to_cart, get_cart_total

urlpatterns = [
    path('cart/create/', create_cart, name='create_cart'),
    path('cart/add-item/', add_item_to_cart, name='add_item'),
    path('cart/apply-promotion/', apply_promotion_to_cart, name='apply_promotion'),
    path('cart/get-total/', get_cart_total, name='get_total'),
]
