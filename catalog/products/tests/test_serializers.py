import pytest
from decimal import Decimal
from django.contrib.auth.models import User

from products.serializers.product_serializers import ProductSerializer
from products.serializers.order_serializers import OrderSerializer
from products.models import Product

@pytest.mark.django_db
def test_product_serializers_valid(category):
    data = {
        "name": "test_name",
        "description": "test_description",
        "stock": 3,
        "price": 100,
        "available": True,
        "category": category.id,
        "nomenclature": "test_nomenclature",
        "rating": 2,
        "discount": 30,
        "attributes": {}
    }

    serializer = ProductSerializer(data=data)
    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_product_serializer_invalid(category):
    data = {
        "name": "*" * 101,
        "description": 1,
        "stock": -3,
        "price": -100,
        "available": 2,
        "category": "test_category123", 
        "nomenclature": "*" * 101, 
        "rating": "*",
        "discount": -10,
        "attributes": "*"
    }

    serializer = ProductSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors

    assert "Ensure this field has no more than 100 characters." in serializer.errors.get("name", [""])[0]
    assert "Must be a valid boolean." in serializer.errors.get("available", [""])[0]
    assert "Ensure this field has no more than 50 characters." in serializer.errors.get("nomenclature", [""])[0]
    assert "A valid number is required." in serializer.errors.get("rating", [""])[0]

    for field in data.keys():
        assert field in serializer.errors


@pytest.mark.django_db
def test_product_serializer_method_field(product_with_discount):
    serializer = ProductSerializer(product_with_discount)
    
    assert Decimal(serializer.data['discount_price']) == Decimal(str(product_with_discount.discount_price))


@pytest.mark.django_db
def test_order_serializer_read_only(user, order):
    data = {
        "user": user.id,
        "contact_name": "test_name",
        "contact_email": "example.example@gmail.com",
        "contact_phone": "+380663831118",
        "address": "5 Avenue",
    }

    serializer = OrderSerializer(data=data)
    assert serializer.is_valid()
    assert "items" not in serializer.validated_data
    serializer = OrderSerializer(order)
    assert "items" in serializer.data