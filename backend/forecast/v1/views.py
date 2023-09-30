from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from collections import defaultdict
from lenta_backend.consatants import ONLY_LIST_MSG
from .models import Forecast
from .serializers import ForecastPostSerializer, ForecastGetSerializer
from shops.v1.models import Shop

class ForecastViewSet(viewsets.ModelViewSet):
    """Представление модели прогноза.
    """
    queryset = Forecast.objects.all()
    http_method_names = ['get', 'post']

    def retrieve(self, request):
        raise MethodNotAllowed('GET', detail=ONLY_LIST_MSG)
    
    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от
        используемого метода.
        """
        if self.action == 'create':
            return ForecastPostSerializer
        return ForecastGetSerializer
    
    def create(self, request, *args, **kwargs):  
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        if serializer.is_valid():  
            serializer.save()  
            return Response({"success": "Прогноз успешно сохранен"}, status=status.HTTP_201_CREATED)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    def list(self, request, *args, **kwargs):
        store_id = self.request.query_params.get('store')
        sku_id = self.request.query_params.get('sku') 
        if store_id and sku_id:
            queryset = Forecast.objects.filter(store=store_id, product=sku_id)
        else:
            queryset = Forecast.objects.all()
        if not queryset.exists():
            return Response({'error': 'Не найдены данные с указанными параметрами'}, status=status.HTTP_404_NOT_FOUND)
        grouped_data = defaultdict(lambda: defaultdict(int))
        for forecast in queryset:
            key = (forecast.store, forecast.product.sku)
            date_str = forecast.date.strftime('%Y-%m-%d')
            grouped_data[key][date_str] = forecast.target
        serialized_data = []
        for (store_id, sku), forecast_dict in grouped_data.items():
            store = Shop.objects.get(store=store_id)
            serializer = self.get_serializer({'store': store, 'sku': sku, 'forecast_date': min(forecast_dict.keys()), 'forecast': forecast_dict})
            serialized_data.append(serializer.data)
        return Response({'data': serialized_data})
