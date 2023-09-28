from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Forecast
from .serializers import ForecastPostSerializer, ForecastGetSerializer

class ForecastViewSet(viewsets.ModelViewSet):
    queryset = Forecast.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ForecastPostSerializer
        return ForecastGetSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Прогноз успешно сохранен"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())    
        store_id = self.request.query_params.get('store')
        sku_id = self.request.query_params.get('sku')
        if store_id and sku_id:
            queryset = queryset.filter(storestore=store_id, productsku=sku_id)        
        if not queryset.exists():
            return Response({"error": "Не найдены данные с указанными параметрами"}, status=status.HTTP_404_NOT_FOUND)  
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
