from django.urls import path

from .views import index, about_us, product_details, cart_detail_view, cart_add, update_cart_item_quantity, remove_from_cart


urlpatterns = [
    path('',index, name="index"),
    path('about/',about_us, name="about"),
    path('product/<int:product_id>/',product_details, name="product_details"),
    path('cart_add/<int:product_id>/',cart_add, name="cart_add"),
    path('cart_details/',cart_detail_view, name="cart_detail"),
    path('update_cart_item/', update_cart_item_quantity, name="update_cart_item"), 
    path('remove_from_cart/', remove_from_cart, name="remove_from_cart")
]