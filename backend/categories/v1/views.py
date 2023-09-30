from rest_framework import viewsets
from categories.v1.models import Product
from categories.v1.serializers import ProductSerializer
from categories.v1.filters import ProductFilter
from api.pagination import LimitPageNumberPagination

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление модели товарной иерархии."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitPageNumberPagination
    filterset_class = ProductFilter