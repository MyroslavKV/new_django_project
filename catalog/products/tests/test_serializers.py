import pytest
import pytest_check as check

from products.serializers.product_serializers import ProductSerializer
from products.serializers.order_serializers import OrderSerializer

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
        "name": "*"*101,
        "description": 1,
        "stock": -3,
        "price": -100,
        "available": 2,
        "category": "test_category123",
        "nomenclature": "*"*101,
        "rating": "*",
        "discount": -10,
        "attributes": "*"
    }

    serializer = ProductSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors

    check.is_in('Ensure this field has no more than 100 characters.', serializer.errors.get("name", [""])[0])
    check.is_in('Must be a valid boolean.', serializer.errors.get("available", [""])[0])
    check.is_in('Ensure this field has no more than 50 characters.', serializer.errors.get("nomenclature", [""])[0])
    check.is_in('A valid number is required.', serializer.errors.get("rating", [""])[0])
    
    for field in data.keys():
        assert field in serializer.errors


@pytest.mark.django_db
def test_product_serializer_read_only(category):
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
    product_instance = serializer.save()
    read_only_serializer = ProductSerializer(product_instance)
    

    assert "category" in read_only_serializer.data


@pytest.mark.django_db
def test_product_serializer_method_field(product_discount):
    serializer = ProductSerializer(product_discount)

    assert serializer.data['discount_price'] == product_discount.discount_price
    assert serializer.data['discount_price'] == 80


@pytest.mark.django_db
def test_order_serializer_read_only():
    data = {
        'user': 'test-user',
        'contact_name': 'test-name',
        'contact_email': 'testemail@email.com',
        'contact-phone': '3800999999',
        'address': 'test-address'
    }

    serializer = OrderSerializer(data=data)

    assert serializer.is_valid()
    assert "product" not in serializer.validated_data

    order = serializer.save()

    serializer = OrderSerializer(order)

    assert1 = serializer.is_valid()
    print(serializer.errors)
    assert assert1