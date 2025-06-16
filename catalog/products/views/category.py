from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ReadOnlyModelViewSet
from products.models import Category
from ..serializers.category_serializers import CategorySerializer

@extend_schema_view(
    list=extend_schema(
        summary="List all categories",
        description="Returns a list of all product categories.",
        tags=["Categories"],
    ),
    retrieve=extend_schema(
        summary="Retrieve category by ID",
        description="Returns a single category with its details.",
        tags=["Categories"],
    ),
)

class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer