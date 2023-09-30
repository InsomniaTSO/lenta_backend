from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import action
from rest_framework import status
from lenta_backend.consatants import ONLY_LIST_MSG
from .models import Forecast
from .serializers import ForecastPostSerializer, ForecastGetSerializer
from shops.v1.models import Shop

class ForecastViewSet(viewsets.ModelViewSet): 
    """Представление для работы с моделью прогноза.""" 
    queryset = Forecast.objects.all() 
    http_method_names = ['get', 'post'] 

    def retrieve(self, request): 
        """Ограничение метода retrieve.""" 
        raise MethodNotAllowed('GET', detail=ONLY_LIST_MSG)  
   
    def get_serializer_class(self):  
        """Метод для выбора сериализатора.  
        В зависимости от действия выбирает соответствующий сериализатор.
        """  
        if self.action == 'create':  
            return ForecastPostSerializer  
        return ForecastGetSerializer  

    def list(self, request):
        """Метод для получения списка прогнозов."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})

    @action(detail=False, methods=['POST']) 
    def bulk_create(self, request): 
        """Метод для массового создания прогнозов.
        Принимает список прогнозов и сохраняет их все в базе данных."""
        data = request.data.get('data', []) 
        forecasts = [] 
        for forecast in data: 
            store_id = forecast.get('store') 
            if not Shop.objects.filter(pk=store_id).exists(): 
                return Response({'store': f'Магазина с ID {store_id} не существует.'}, status=status.HTTP_400_BAD_REQUEST) 
            forecast['store'] = Shop.objects.get(pk=store_id) 
            serializer = self.get_serializer(data=forecast) 
            serializer.is_valid(raise_exception=True) 
            forecasts.append(serializer.save()) 
        return Response(self.get_serializer(forecasts, many=True).data, status=status.HTTP_201_CREATED)
