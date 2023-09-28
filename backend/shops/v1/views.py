from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from shops.v1.serializers import ShopsSerializer
from shops.v1.models import Shop
from shops.v1.filters import ShopFilter
from api.pagination import LimitPageNumberPagination


class ShopViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление модели магазинов."""

    queryset = Shop.objects.all()
    serializer_class = ShopsSerializer
    pagination_class = None
    filterset_class = ShopFilter
    pagination_class = LimitPageNumberPagination
