from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from products.models import Product
from ..serializers.product_serializers import ProductSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List all products",
        description="Returns a filtered and ordered list of products.",
        tags=["Products"],
    ),
    retrieve=extend_schema(
        summary="Retrieve product by ID",
        description="Returns product details by ID.",
        tags=["Products"],
    ),
    create=extend_schema(
        summary="Create a new product",
        description="Creates a new product in the catalog.",
        tags=["Products"],
    ),
    update=extend_schema(
        summary="Update a product",
        description="Replaces a product entirely.",
        tags=["Products"],
    ),
    partial_update=extend_schema(
        summary="Partially update a product",
        description="Updates specific fields of a product.",
        tags=["Products"],
    ),
    destroy=extend_schema(
        summary="Delete a product",
        description="Deletes a product from the catalog.",
        tags=["Products"],
    ),
)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]
    ordering_fields = ["price", "rating"]