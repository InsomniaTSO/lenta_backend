from rest_framework import viewsets
from categories.v1.models import Product
from categories.v1.serializers import ProductSerializer
from categories.v1.filters import ProductFilter
from api.pagination import LimitPageNumberPagination
from rest_framework.response import Response

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление модели товарной иерархии."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # pagination_class = LimitPageNumberPagination
    filterset_class = ProductFilter

    def list(self, request):
        """Метод для получения списка товарной иерархии."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})