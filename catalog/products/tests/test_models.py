import pytest
from decimal import Decimal

from products.models import Cart, Product, Category, CartItem, Order, OrderItem
from .fixtures import product, product_with_discount, order, category


AMOUNT = 10

@pytest.mark.django_db
def test_product_model():
    category = Category.objects.create(
        name="test_category"
    )
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
def test_cart_model_one_product(user, product):
    cart, _ = Cart.objects.get_or_create(user=user)
    CartItem.objects.filter(cart=cart).delete()

    cart_item = CartItem.objects.create(
        cart=cart,
        product=product,
        amount=1,
    )
    
    assert cart.total_price == product.price
    assert cart_item.total_price == product.price
        
@pytest.mark.django_db
def test_cart_model_multiple_products(user, product):
    cart, _ = Cart.objects.get_or_create(user=user)
    CartItem.objects.filter(cart=cart).delete()

    cart_item = CartItem.objects.create(
        cart=cart,
        product=product,
        amount=AMOUNT,
    )
    
    assert cart.total_price == product.price * AMOUNT
    assert cart_item.total_price == product.price * AMOUNT
    
@pytest.mark.django_db
def test_cart_model_discount_product(user, product_with_discount):
    cart, _ = Cart.objects.get_or_create(user=user)
    CartItem.objects.filter(cart=cart).delete()

    cart_item = CartItem.objects.create(
        cart=cart,
        product=product_with_discount,
        amount=1,
    )

    expected_price = Decimal(str(product_with_discount.discount_price))

    assert cart.total_price == expected_price
    assert cart_item.total_price == expected_price
    
@pytest.mark.django_db
def test_cart_model_discount_multiple_products(user, product_with_discount):
    cart, _ = Cart.objects.get_or_create(user=user)
    CartItem.objects.filter(cart=cart).delete()

    cart_item = CartItem.objects.create(
        cart=cart,
        product=product_with_discount,
        amount=AMOUNT,
    )

    expected_price = Decimal(str(product_with_discount.discount_price)) * AMOUNT

    assert cart.total_price == expected_price
    assert cart_item.total_price == expected_price


@pytest.mark.django_db
def test_cart_model_different_products(user, product_discount, product):

    cart_item = CartItem.objects.create(
        cart=user.cart,
        product=product_discount,
    )

    cart_item_2 = CartItem.objects.create(
        cart=user.cart,
        product=product,
    )

    assert user.cart.total == 190

@pytest.mark.django_db
def test_order_creation(user):
    order = Order.objects.create(
        user=user,
        contact_name="John Doe",
        contact_email="john@example.com",
        contact_phone="+380123456789",
        address="Kyiv, Ukraine"
    )
    assert order.status == Order.Status.NEW
    assert order.is_paid is False
    assert str(order).startswith("Order №:")

@pytest.mark.django_db
def test_order_total_price(user, product):
    order = Order.objects.create(
        user=user,
        contact_name="Jane Doe",
        contact_email="jane@example.com",
        contact_phone="+380987654321",
        address="Lviv, Ukraine"
    )

    assert order.total_price == 0

    item = OrderItem.objects.create(
        order=order,
        product=product,
        amount=2,
        price=product.price
    )

    expected_total = item.amount * item.price
    assert order.total_price == expected_total

@pytest.mark.django_db
def test_order_multiple_items_total(user, product, product_with_discount):
    order = Order.objects.create(
        user=user,
        contact_name="Test User",
        contact_email="testuser@example.com",
        contact_phone="+380111222333",
        address="Odesa, Ukraine"
    )

    item1 = OrderItem.objects.create(
        order=order,
        product=product,
        amount=1,
        price=product.price
    )
    item2 = OrderItem.objects.create(
        order=order,
        product=product_with_discount,
        amount=3,
        price=product_with_discount.discount_price
    )

    expected_total = (item1.amount * item1.price) + (item2.amount * item2.price)
    assert order.total_price == expected_total

@pytest.mark.django_db
def test_order_status_choices(user):
    order = Order.objects.create(
        user=user,
        contact_name="Status Test",
        contact_email="status@example.com",
        contact_phone="+380000000000",
        address="Kharkiv, Ukraine",
        status=Order.Status.PROCESSING,
        is_paid=True
    )
    assert order.status == Order.Status.PROCESSING
    assert order.is_paid is True