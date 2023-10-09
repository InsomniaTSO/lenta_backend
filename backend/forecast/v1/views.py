import pandas as pd
import json
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from lenta_backend.constants import ONLY_LIST_MSG
from forecast.v1.filters import ForecastFilter
from forecast.v1.get_xls import get_xls, get_quality_xls
from forecast.v1.models import Forecast
from forecast.v1.serializers import (
    ForecastGetSerializer, ForecastPostSerializer
)
from sales.v1.models import Sales
from categories.v1.models import Product
from forecast.v1.aggregation import aggregation, aggregation_by_store


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
        serializer.create(data=request.data['data'])
        headers = self.get_success_headers(serializer.data)
        return Response(
            request.data['data'],
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=False, methods=['get'])
    def download_file(self, request):
        """Возвращает xlsx-файл с предсказаниями.
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
        date_range = ["2023-07-05", "2023-07-18"]
        store_ids = self.request.query_params.getlist('store')
        sku_ids = self.request.query_params.getlist('sku')
        group = self.request.query_params.get('group')
        if not store_ids or not sku_ids:
            return Response({"data": []}, status=status.HTTP_404_NOT_FOUND)
        query_sales = Sales.objects.filter(date__range=date_range)
        query_forecast = Forecast.objects.filter(date__range=date_range)
        query_f = Q()
        for store_id in store_ids:
            for sku_id in sku_ids:
                query_f |= Q(store=store_id, product=sku_id)
        query_s = Q()
        for store_id in store_ids:
            for sku_id in sku_ids:
                query_s |= Q(shop=store_id, product=sku_id)
        if (not query_sales.filter(query_s)
                or not query_forecast.filter(query_f)):
            return Response({"data": []}, status=status.HTTP_404_NOT_FOUND)
        cat = Product.objects.all().values()
        pd_cat = pd.DataFrame(cat).rename(columns={'sku': 'product_id'})
        pd_sales = pd.DataFrame(query_sales.filter(query_s).values())
        pd_forecast = pd.DataFrame(query_forecast.filter(query_f).values())
        pd_all = aggregation(pd_cat, pd_sales, pd_forecast)
        if group == "1":
            result = aggregation_by_store(pd_all)
            return Response({"data":
                             json.loads(result.to_json(orient="records"))},
                            status=status.HTTP_200_OK)
        else:
            return Response({"data":
                             json.loads(pd_all.to_json(orient="records"))},
                            status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def download_forecast_quality(self, request):
        """
        Возвращает xlsx-файл с качеством прогноза.
        """
        today = datetime.today().strftime('%d-%m-%Y')
        filename = f'{today}_forecast_quality.xlsx'
        date_range = ["2023-07-05", "2023-07-18"]
        store_ids = self.request.query_params.getlist('store')
        sku_ids = self.request.query_params.getlist('sku')
        if not store_ids or not sku_ids:
            return Response({"data": []}, status=status.HTTP_404_NOT_FOUND)
        query_sales = Sales.objects.filter(date__range=date_range)
        query_forecast = Forecast.objects.filter(date__range=date_range)
        query_f = Q()
        for store_id in store_ids:
            for sku_id in sku_ids:
                query_f |= Q(store=store_id, product=sku_id)
        query_s = Q()
        for store_id in store_ids:
            for sku_id in sku_ids:
                query_s |= Q(shop=store_id, product=sku_id)
        if (not query_sales.filter(query_s)
                or not query_forecast.filter(query_f)):
            return Response({"data": []}, status=status.HTTP_404_NOT_FOUND)
        cat = Product.objects.all().values()
        pd_cat = pd.DataFrame(cat).rename(columns={'sku': 'product_id'})
        pd_sales = pd.DataFrame(query_sales.filter(query_s).values())
        pd_forecast = pd.DataFrame(query_forecast.filter(query_f).values())
        pd_all = aggregation(pd_cat, pd_sales, pd_forecast)
        forecast = get_quality_xls(pd_all).getvalue()
        response = HttpResponse(
            forecast, content_type='application/vnd.ms-excel'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
