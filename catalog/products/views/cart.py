from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.shortcuts import get_object_or_404
from django.conf import settings
from catalog.products.forms import OrderCreateForm
from catalog.products.models import OrderItem

from models import Cart, CartItem, Product, Payment, Order
from serializers.cart_serializers import CartItemSerializer, CartSerializer
from serializers.product_serializers import ProductSerializer
from utils.email.email import send_order_confirmation_email


@extend_schema_view(
    add=extend_schema(
        summary="Add product to cart",
        description="Adds a product to the user's cart or session cart."
    ),
    checkout=extend_schema(
        summary="Checkout current cart",
        description="Creates an order from the cart and processes the payment."
    )
)

class CartViewSet(ViewSet):
    queryset = CartItem.objects.all()

    @action(detail=False, methods=['post'], url_path='cart-add/<int:product_id>')
    def add(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            cart = request.user.cart
            cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
            if _:
                cart_item.amount = 1
            else:
                cart_item.amount += 1
            cart_item.save()
        else:
            cart = request.session.get(settings.CART_SESSION_ID, default = {})
            cart[str(product_id)] = cart.get(str(product_id), default=0) + 1
        return Response({'message':f'Product with id {product_id} has been added'}, status=200)

    @action(detail=False, methods=['post'], url_path='cart-checkout')
    def checkout(self, request):
        if request.user.is_authenticated:
            cart = request.session.get()
            if not cart or cart.items.count() == 0:
                return Response({"error":"Cart is empty"}, status=400)

        else:
            if not request.session.get(settings.CART_SESSION_ID, default={}):
                return Response({"error":"Cart is empty"}, status=400)

        form = OrderCreateForm(request.data)

        if not form.is_valid():
            return Response ({"error": "Cart is empty"}, status=400)

        order = form.save(commit=False)

        if request.user.is_authenticated:
            order.user = request.user

        order.save()

        if request.user.is_authenticated:
            cart_items = order.user.cart_items.select_related("product").all()
            items = OrderItem.objects.bulk_create([OrderItem(order=order, product=item["product"], amount=item["amount"], 
            price=item["product"].discount_price or item["product"].price) for item in cart_items])

        else:
            cart_items = [{"product":Product.objects.get(id=int(p_id)), "amount":a} for p_id, a in cart.items()]
            items = OrderItem.objects.bulk_create([OrderItem(order=order, product=item["product"], amount=item["amount"], 
            price=item["product"].discount_price or item["product"].price) for item in cart_items])

            method = form.cleaned_data["payment_method"]
            total = sum(item.item_total for item in items)
            if method != "cash":
                Payment.objects.create(order=order, provider=method, amount=total, status=Payment.Status)
            else:
                order.status = Order.Status.PROCESSING
                order.save()

        if request.user.is_authenticated:
            request.user.cart.items.all().delete()
        else:
            cart.clear()

        if request.user.is_authenticated:

        send_order_confirmation_email(order=order)

        return Response({"message":"Order {order.id} is created"}, status=200)

        
