from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import action
from rest_framework import status
from lenta_backend.consatants import ONLY_LIST_MSG
from .models import Forecast
from .serializers import ForecastPostSerializer, ForecastGetSerializer
from .filters import ForecastFilter
from api.pagination import LimitPageNumberPagination


class ForecastViewSet(viewsets.ModelViewSet): 
    """Представление для работы с моделью прогноза.""" 
    queryset = Forecast.objects.all()
    serializer_class = ForecastGetSerializer
    http_method_names = ['get', 'post']
    filterset_class = ForecastFilter

    def retrieve(self, request): 
        """Ограничение метода retrieve.""" 
        raise MethodNotAllowed('GET', detail=ONLY_LIST_MSG)  
   
    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от
        используемого метода.
        """
        if self.action == 'create':
            return ForecastPostSerializer
        return self.serializer_class

    def list(self, request):
        """Метод для получения списка прогнозов."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Метод для создания прогноза и возврата данных в нужном формате.
        """
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'data': [serializer.data]}, status=status.HTTP_201_CREATED, headers=headers)

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
        return Response({'data': self.get_serializer(forecasts, many=True).data}, status=status.HTTP_201_CREATED)
