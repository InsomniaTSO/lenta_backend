from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from categories.v1.models import Product
from categories.v1.serializers import ProductSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление модели товарной иерархии."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None