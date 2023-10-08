from datetime import datetime
from django.db.models import Q

from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from datetime import datetime, timedelta

from lenta_backend.constants import ONLY_LIST_MSG

from forecast.v1.filters import ForecastFilter
from forecast.v1.get_xls import get_xls
from forecast.v1.models import Forecast
from forecast.v1.serializers import ForecastGetSerializer, ForecastPostSerializer, ForecastSerializer
from sales.v1.models import Sales
from shops.v1.models import Shop



class ForecastViewSet(viewsets.ModelViewSet):
    """Представление для работы с моделью прогноза.""" 
    queryset = Forecast.objects.all()
    serializer_class = ForecastGetSerializer
    http_method_names = ['get', 'post']
    filterset_class = ForecastFilter

    def retrieve(self, request, pk=None):
        """Ограничение метода retrieve."""
        raise MethodNotAllowed('GET', detail=ONLY_LIST_MSG)

    def get_serializer(self, *args, **kwargs):
        """Задает значение many=true если передан список.
        """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(ForecastViewSet, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от
        используемого метода.
        """
        if self.action == 'create':
            return ForecastPostSerializer
        elif self.action == 'comparison':
            return ForecastSerializer
        return self.serializer_class

    def list(self, request):
        """Метод для получения списка прогнозов."""
        store_ids = self.request.query_params.getlist('store')
        sku_ids = self.request.query_params.getlist('sku')
        if not store_ids or not sku_ids:
            return Response(
                {'error': 'Не найдены данные с указанными параметрами'},
                status=status.HTTP_404_NOT_FOUND
            )
        queryset = self.filter_queryset(self.get_queryset())
        data_list = []
        for obj in queryset:
            serializer = self.get_serializer(obj) 
            if serializer.data not in data_list:
                data_list.append(serializer.data)
        return Response({'data': data_list})
    
    def create(self, request, *args, **kwargs):
        """Метод для создания прогноза и возврата данных в нужном формате.
        """
        serializer = self.get_serializer(data=request.data['data'])
        serializer.is_valid(raise_exception=True)
        serializer.create(validated_data=request.data['data'])
        headers = self.get_success_headers(serializer.data)
        return Response(request.data['data'], status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def download_file(self, request):
        """
        Возвращает xlsx-файл с предсказаниями.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = JSONRenderer().render(serializer.data)
        today = datetime.today().strftime('%d-%m-%Y')
        filename = f'{today}_forecast.xlsx'
        forecast = get_xls(data).getvalue()
        response = HttpResponse(
            forecast, content_type='application/vnd.ms-excel'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    
    @action(detail=False, methods=['get'])
    def forecast_quality(self, request):
        """
        Возвращает сводные данные по продажам и предсказаниям.
        """
        store_ids = self.request.query_params.getlist('store')
        sku_ids = self.request.query_params.getlist('sku')
        date = self.request.query_params.get('date')
        group = self.request.query_params.get('group')
        
        # for store in store_ids:
        #     for sku in sku_ids:
        #         forecasts = Forecast.objects.filter(store=store, product=sku)
        #         sales = Sales.objects.filter(store=store, product=sku, date__range=["2011-01-01", "2011-01-31"])

        # for store in store_ids:
        #     serializer = self.get_serializer(data=Shop.objects.get(store=store).forecasts)
        #     serializer.is_valid(raise_exception=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
