from django.urls import path

from .views import index, about_us, product_details

urlpatterns = [
    path('',index, name="index"),
    path('',about_us, name="about"),
    path('product/<int:product_id>/',product_details, name="product_details")
]