from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.product import ProductViewSet
from .views.category import CategoryViewSet

from products.views.views import index, product_details, cart_detail_view, cart_add, cart_delete, checkout

app_name = 'products'
router = DefaultRouter()
router.register(r"products", viewset=ProductViewSet, basename="products")
router.register(r"category", viewset=CategoryViewSet)

urlpatterns = [
    path('', index, name="index"),
    path('pct/<int:product_id>/', product_details, name="product_details"),
    path('cart_roduadd/<int:product_id>/', cart_add, name="cart_add"),
    path('cart_details/', cart_detail_view, name="cart_detail"),
    path('cart_delete/<int:product_id>/', cart_delete, name="cart_delete"),
    path('checkout/', checkout, name="checkout"),
]

urlpatterns += router.urls