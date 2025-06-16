import json
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes

from products.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
        "id",
        "name",
        "description",
        "stock", 
        "price",
        "available",
        "category",
        "nomenclature",
        "created_at",
        "rating",
        "discount",
        "attributes",
        "discount_price",
        ]


    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_discount_price(self, obj):
        if obj.get("discount"):
            return obj.get("discount_price")
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('The price should be higher than 0')
        return value
        
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('The stock should be higher than 0')
        return value
    
    def validate_description(self, value):
        if isinstance(value,str):
            return value
        raise serializers.ValidationError('Description must be text')
    
    def validate_category(self, value):
        print(isinstance(value, int))
        if not (isinstance(value, int)) or not (isinstance(value, Category)):
            raise serializers.ValidationError("Category must be int or Category instance")
        return value

    def validate_discount(self, value):
        if value < 0:
            raise serializers.ValidationError('The discount should be higher than 0')
        return value

    def validate_attributes(self, value):
        if not value:
            return value
        try:
            return json.loads(value)
        except Exception:
            raise serializers.ValidationError('Attributes must be a valid JSON')
        
