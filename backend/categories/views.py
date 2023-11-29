from rest_framework import viewsets
from rest_framework.response import Response

from categories.filters import ProductFilter
from categories.models import Product
from categories.serializers import ProductSerializer
from api.pagination import LimitPageNumberPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление модели товарной иерархии."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitPageNumberPagination
    filterset_class = ProductFilter

    def list(self, request):
        """Метод для получения списка товарной иерархии."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
