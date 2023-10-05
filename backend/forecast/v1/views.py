from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import action
from rest_framework import status
from lenta_backend.constants import ONLY_LIST_MSG
from .models import Forecast
from .serializers import ForecastPostSerializer, ForecastGetSerializer
from datetime import datetime
from django.http import HttpResponse
from .filters import ForecastFilter
from .get_xls import get_xls
from rest_framework.renderers import JSONRenderer


class ForecastViewSet(viewsets.ModelViewSet): 
    """Представление для работы с моделью прогноза.""" 
    queryset = Forecast.objects.all()
    serializer_class = ForecastGetSerializer
    http_method_names = ['get', 'post']
    filterset_class = ForecastFilter

    def retrieve(self, request): 
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

    # def list(self, request):
    #     """Метод для получения списка прогнозов."""
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response({'data': serializer.data})
    
    def create(self, request, *args, **kwargs):
        """Метод для создания прогноза и возврата данных в нужном формате.
        """
        serializer=self.get_serializer(data=request.data['data'])
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

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
