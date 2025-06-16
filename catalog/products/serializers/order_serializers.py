from rest_framework import serializers
from rest_framework.fields import DecimalField
from drf_spectacular.utils import extend_schema_field

from models import Order, OrderItem
from serializers.product_serializers import ProductSerializer



class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'

    @extend_schema_field(DecimalField(max_digits=10, decimal_places=2))
    def get_total_price(self, obj):
        return obj.total_price

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError("The quantity must be at least 1.")
        return value

    def validate(self, data):
        product = self.instance.product if self.instance else data.get("product")
        amount = data.get("amount")
        price = data.get("price")

        if product:
            if not product.available:
                raise serializers.ValidationError("This product is not available for ordering.")
            if amount and product.stock < amount:
                raise serializers.ValidationError("Not enough items in stock.")
            if price and price < product.discount_price:
                raise serializers.ValidationError("Price must not be lower than the product's discounted price.")

        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    @extend_schema_field(DecimalField(max_digits=10, decimal_places=2))
    def get_total_price(self, obj):
        return obj.total_price

    def validate_contact_email(self, value):
        if not value or '@' not in value:
            raise serializers.ValidationError("Please enter a valid email address.")
        return value

    def validate_contact_phone(self, value):
        if not value or not value.startswith('+'):
            raise serializers.ValidationError("Phone number must start with '+'.")
        if len(value) < 10:
            raise serializers.ValidationError("Phone number is too short.")
        return value

    def validate_address(self, value):
        if not value.strip():
            raise serializers.ValidationError("Address cannot be empty.")
        return value

    def validate(self, data):
        instance = self.instance
        items = instance.items.all() if instance else []

        if not items:
            raise serializers.ValidationError("The order must contain at least one item.")

        total = sum(item.total_price for item in items)
        if total <= 0:
            raise serializers.ValidationError("The total order price must be greater than zero.")

        return data