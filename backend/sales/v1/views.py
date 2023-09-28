from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Sales
from .serializers import SalesSerializer


class SalesViewSet(viewsets.ModelViewSet):
    """Представление модели продаж.
    """
    serializer_class = SalesSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    
    def get_queryset(self):
        print(self.request.query_params)
        store_id = self.request.query_params.get('store')
        sku_id = self.request.query_params.get('sku')
        if not store_id or not sku_id:
            print('Ой')
            return Sales.objects.none()
        queryset = Sales.objects.filter(shop__store=store_id, product__sku=sku_id)
        print(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response(
                {"error": "Не найдены данные с указанными параметрами"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
