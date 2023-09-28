from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from shops.v1.serializers import ShopsSerializer
from shops.v1.models import Shop
from .filters import ShopFilter


class ShopViewSet(viewsets.ModelViewSet):
    """Представление модели магазинов."""

    queryset = Shop.objects.all()
    serializer_class = ShopsSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filterset_class = ShopFilter
