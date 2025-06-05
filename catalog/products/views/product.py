from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from models import Product
from ..serializers.product_serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.object.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]
    ordering_fields = ["price", "rating"]