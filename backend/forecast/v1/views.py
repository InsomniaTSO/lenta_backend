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
    #     store_ids = self.request.query_params.getlist('store')
    #     sku_ids = self.request.query_params.getlist('sku')
    #     if not store_ids or not sku_ids:
    #         return Response(
    #             {'error': 'Не найдены данные с указанными параметрами'},
    #             status=status.HTTP_404_NOT_FOUND
    #         )
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})

    def create(self, request, *args, **kwargs):
        """Метод для создания прогноза и возврата данных в нужном формате.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'data': serializer.data}, status=status.HTTP_201_CREATED, headers=headers
        )

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

    # @action(detail=False, methods=['get'])
    # def comparison(self, request):
    #     """
    #     Возвращает сводные данные по продажам и предсказаниям.
    #     """
    #     store_ids = self.request.query_params.getlist('store')
    #     sku_ids = self.request.query_params.getlist('sku')
    #     queryset_sales = Sales.objects.all()
    #     if not store_ids or not sku_ids:
    #         return Response({'data': []}, status=status.HTTP_404_NOT_FOUND)
    #     queryset_forecast = self.filter_queryset(self.get_queryset())
    #     query = Q()
    #     for store_id in store_ids:
    #         for sku_id in  sku_ids:
    #             query |= Q(shop=store_id, product=sku_id)
    #     queryset_sales =  queryset_sales.filter(query)
    #     serializer_forecast = self.get_serializer(queryset_forecast, many=True).data
    #     serializer_sales = SalesGroupSerializer(queryset_sales, many=True).data[0]
    #     result_list = []
    #     result = {}
    #     for sale in serializer_sales:
    #         for forecast in serializer_sales:
    #             if (sale["store"] == forecast["store"] and
    #                 sale["sku"] == forecast["sku"]):
    #                     result["store"] = sale["store"]
    #                     result["sku"] = sale["sku"]
         
    #     return Response({'data': serializer_sales.data[0]}, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'])    
    def comparison(self, request):    
        store_ids = self.request.query_params.getlist('store')    
        sku_ids = self.request.query_params.getlist('sku')    
    
        if not store_ids or not sku_ids:    
            return Response({'data': []}, status=status.HTTP_404_NOT_FOUND)    
    
        end_date = datetime.now().date()   
        start_date = end_date - timedelta(days=14)  
    
        sales = Sales.objects.filter(shop__in=store_ids, product__in=sku_ids, date__gte=start_date)    
        forecasts = Forecast.objects.filter(store__in=store_ids, product__in=sku_ids, forecast_date=start_date)
    
        result_list = []    
    
        for store_id in store_ids:    
            for sku_id in sku_ids:    
                sales_for_combo = sales.filter(shop=store_id, product=sku_id)    
                sales_map = {   
                    sale.date: sale.sales_units for sale in sales_for_combo    
                }   
    
                forecast_for_combo = forecasts.filter(store=store_id, product=sku_id).first()    
                if forecast_for_combo:   
                    detailed_entries = []
                    first_week_forecast = 0
                    first_week_sales = 0
                    second_week_forecast = 0
                    second_week_sales = 0
    
                    for date_str, forecast_value in forecast_for_combo.forecast['sales_units'].items():    
                        date = datetime.strptime(date_str, '%Y-%m-%d').date()    
                        sales_units = sales_map.get(date, 0)
                        
                        entry = {  
                            'date': date_str,    
                            'forecast': forecast_value,    
                            'sales_units': sales_units    
                        }
                        
                        detailed_entries.append(entry)
    
                        if (date - start_date).days < 7:  
                            first_week_forecast += forecast_value
                            first_week_sales += sales_units
                        else:  
                            second_week_forecast += forecast_value
                            second_week_sales += sales_units
                            
                    comparison_data = { 
                        'first_week': [{
                            'forecast': first_week_forecast,
                            'sales_units': first_week_sales
                        }],
                        'second_week': [{
                            'forecast': second_week_forecast,
                            'sales_units': second_week_sales
                        }],
                        'details': detailed_entries
                    }
    
                    result_list.append({    
                        'store': store_id,    
                        'sku': sku_id,    
                        'comparison': comparison_data  
                    })   
    
        return Response({'data': result_list}, status=status.HTTP_200_OK)