from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.product import ProductViewSet
from .views.category import CategoryViewSet

from .views import index, about_us, product_details, cart_detail_view, cart_add, update_cart_item_quantity, remove_from_cart

app_name = 'products'
router = DefaultRouter()
router.register(r"products", viewset=ProductViewSet)
router.register(r"category", viewset=CategoryViewSet)

urlpatterns = [
    path('',index, name="index"),
    path('about/',about_us, name="about"),
    path('product/<int:product_id>/',product_details, name="product_details"),
    path('cart_add/<int:product_id>/',cart_add, name="cart_add"),
    path('cart_details/',cart_detail_view, name="cart_detail"),
    path('update_cart_item/', update_cart_item_quantity, name="update_cart_item"), 
    path('remove_from_cart/', remove_from_cart, name="remove_from_cart")
]

urlpatterns += router.urls