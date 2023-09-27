from rest_framework import viewsets
from shops.v1.serializers import ShopsSerializer
from shops.v1.models import Shop
from rest_framework.permissions import AllowAny


class ShopViewSet(viewsets.ModelViewSet):
    """Представление модели магазинов."""

    queryset = Shop.objects.all()
    serializer_class = ShopsSerializer
    permission_classes = (AllowAny,)
    pagination_class = None