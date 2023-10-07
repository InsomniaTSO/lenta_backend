from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.pagination import LimitPageNumberPagination
from shops.v1.filters import ShopFilter
from shops.v1.models import Shop
from shops.v1.serializers import ShopsSerializer


class ShopViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление модели магазинов."""

    queryset = Shop.objects.all()
    serializer_class = ShopsSerializer
    permission_classes = (AllowAny,)
    filterset_class = ShopFilter
    pagination_class = LimitPageNumberPagination

    def list(self, request):
        """Метод для получения списка магазинов."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})
