from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from categories.models import Category
from sales.models import Sales
from shops.models import Shop
from .serializers import CategoriesViewSerializer, SalesSerializer, ShopsSerializer



class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление модели иерархии."""
    queryset = Category.objects.all()
    serializer_class = CategoriesViewSerializer
    permission_classes = (AllowAny,)
    pagination_class = None



class SalesViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для обработки запросов к объектам Sales. Предоставляет только возможность чтения данных. 
    Переопределен метод list для фильтрации queryset по параметрам store_id и sku_id, переданным в запросе. 
    В случае отсутствия требуемых параметров возвращает ошибку 400, а при отсутствии результатов по запросу - ошибку 404. 
    """
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    permission_classes = (AllowAny,) 
    pagination_class = None
    
    def list(self, request, *args, **kwargs):
        store_id = request.query_params.get('store_id')
        sku_id = request.query_params.get('sku_id')
        
        if not store_id or not sku_id:
            return Response({"error": "store_id and sku_id are required"}, status=400)
            
        queryset = Sales.objects.filter(storestore_id=store_id, productsku_id=sku_id)
        
        if not queryset.exists():
            return Response({"error": "No sales found for the given store_id and sku_id"}, status=404)
            
        serializer = SalesSerializer(queryset, many=True)
        
        return Response(serializer.data)



class ShopsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для обработки запросов к объектам Shops. Предоставляет только возможность чтения данных.  
    """

    queryset = Shop.objects.all()
    serializer_class = ShopsSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
