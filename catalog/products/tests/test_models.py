import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from catalog.accounts.models import Profile, User
from catalog.products.models import Cart, Product, Category, CartItem
from fixtures import product

@pytest.mark.django_db
def test_product_model():
    category = Category.objects.create(name="test_category")
    product = Product.objects.create(
        name="test_product",
        category=category, 
        nomenclature="test_nomenclature", 
        price=100, 
        discount=10
    )

    assert product.discount_price == 90
    assert product.category.name == "test_category"

@pytest.mark.django_db
def test_cart_model_one_product(user):
    cart_item = CartItem.objects.create(
        cart = user.cart,
        product=product,
        
    )
    assert cart_item.item_total == product.price
    assert user.cart.total == product.price

@pytest.mark.django_db
def test_cart_model_multiple_product(user):
    cart_item = CartItem.objects.create(
        cart=user.cart,
        product=product,
        amount=10
    )
    assert cart_item.item_total == product.price * 10
    assert user.cart.total == product.price * 10