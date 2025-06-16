import pytest

from accounts.models import Profile
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
    
    assert cart.total == product.price
    assert cart_item.item_total == product.price
        
@pytest.mark.django_db
def test_cart_model_multiple_products(user, product):
    cart, _ = Cart.objects.get_or_create(user=user)
    CartItem.objects.filter(cart=cart).delete()

    cart_item = CartItem.objects.create(
        cart=cart,
        product=product,
        amount=AMOUNT,
    )
    
    assert cart.total == product.price * AMOUNT
    assert cart_item.item_total == product.price * AMOUNT
    
@pytest.mark.django_db
def test_cart_model_discount_product(user, product_with_discount):
    cart, _ = Cart.objects.get_or_create(user=user)
    CartItem.objects.filter(cart=cart).delete()

    cart_item = CartItem.objects.create(
        cart=cart,
        product=product_with_discount,
        amount=1,
    )
    
    assert cart.total == product_with_discount.discount_price
    assert cart_item.item_total == product_with_discount.discount_price
    
@pytest.mark.django_db
def test_cart_model_discount_multiple_products(user, product_with_discount):
    cart, _ = Cart.objects.get_or_create(user=user)
    CartItem.objects.filter(cart=cart).delete()

    cart_item = CartItem.objects.create(
        cart=cart,
        product=product_with_discount,
        amount=AMOUNT,
    )
    
    assert cart.total == product_with_discount.discount_price * AMOUNT
    assert cart_item.item_total == product_with_discount.discount_price * AMOUNT
    
@pytest.mark.django_db
def test_cart_model_diffrent_products(user, product_with_discount, product):
    cart, _ = Cart.objects.get_or_create(user=user)
    CartItem.objects.filter(cart=cart).delete()

    CartItem.objects.create(
        cart=cart,
        product=product_with_discount,
        amount=1,
    )
    
    CartItem.objects.create(
        cart=cart,
        product=product,
        amount=1,
    )
    
    expected_total = product_with_discount.discount_price + product.price
    assert cart.total == expected_total

@pytest.mark.django_db
def test_order_model_one_item(order, product):
    OrderItem.objects.filter(order=order).delete()
    order_item = OrderItem.objects.create(
        order=order, product=product, price=product.price, amount=1
    )

    assert order_item.amount == 1
    assert order_item.item_total == product.price


@pytest.mark.django_db
def test_order_model_multiple_items(order, product):
    OrderItem.objects.filter(order=order).delete()
    order_item = OrderItem.objects.create(
        order=order, product=product, amount=AMOUNT, price=product.price
    )

    assert order_item.amount == AMOUNT
    assert order_item.item_total == product.price * AMOUNT


@pytest.mark.django_db
def test_order_model_discount_item(order, product_with_discount):
    OrderItem.objects.filter(order=order).delete()
    order_item = OrderItem.objects.create(
        order=order, product=product_with_discount, price=product_with_discount.price, amount=1
    )

    assert order_item.item_total == product_with_discount.discount_price


@pytest.mark.django_db
def test_order_model_different_items(order, product_with_discount, product):
    OrderItem.objects.filter(order=order).delete()

    order_item_1 = OrderItem.objects.create(
        order=order, product=product, price=product.price, amount=1
    )

    order_item_2 = OrderItem.objects.create(
        order=order, product=product_with_discount, price=product_with_discount.price, amount=1
    )

    expected_total = order_item_1.item_total + order_item_2.item_total
    assert expected_total == product.price + product_with_discount.discount_price
