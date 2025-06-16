from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from rest_framework.fields import DecimalField

from models import Cart, CartItem
from serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    @extend_schema_field(DecimalField(max_digits=10, decimal_places=2))
    def get_item_total(self, obj):
        return obj.item_total

    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'item_total', 'amount']
    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError("The quantity must be at least 1.")
        return value

    def validate(self, data):
        product = self.instance.product if self.instance else self.initial_data.get("product")
        if product and hasattr(product, "price"):
            if product.price < 10:
                raise serializers.ValidationError("The product price must be at least 10 UAH.")
        return data
    

class CartSerializer(serializers.ModelSerializer):
    @extend_schema_field(DecimalField(max_digits=10, decimal_places=2))
    def get_total(self, obj):
        return sum(item.item_total for item in obj.items.all())

    total = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['user', 'created_at', 'items', 'total']

    def validate_items(self, value):
        total_amount = sum(item.get('amount', 0) for item in value)
        if total_amount < 1:
            raise serializers.ValidationError("Cart must contain at least one item.")
        return value