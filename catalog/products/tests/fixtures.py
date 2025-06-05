import pytest

from products.models import Category, Product, Order


@pytest.fixture
def category():
    return Category.objects.create(name="category")


@pytest.fixture
def product(category):
    return Product.objects.create(
        name="test_product",
        category=category.id,
        nomenclature="test_nomenclature",
        price=100
    )


@pytest.fixture
def product_discount(category):
    return Product.objects.create(
        name="test_product_2",
        category=category.id,
        nomenclature="test_nomenclature_2",
        price=100,
        discount=20
    )


@pytest.fixture
def order():
    return Order.objects.create(
        contact_name="test_contact_name",
        contact_email="test_contact_email",
        contact_phone="test_contact_phone",
        address="test_address"
    )
