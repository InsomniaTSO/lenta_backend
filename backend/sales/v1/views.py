from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import MethodNotAllowed
from lenta_backend.consatants import ONLY_LIST_MSG
from sales.v1.models import Sales
from sales.v1.serializers import SalesGroupSerializer, SalesFactSerializer
from api.pagination import LimitPageNumberPagination


class SalesViewSet(viewsets.ModelViewSet):
    """Представление модели продаж.
    """
    queryset = Sales.objects.all()
    serializer_class = SalesGroupSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']
    pagination_class = LimitPageNumberPagination


    def retrieve(self, request):
        raise MethodNotAllowed('GET', detail=ONLY_LIST_MSG)
    
    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости от
        используемого метода.
        """
        if self.action == "create":
            return SalesFactSerializer
        return self.serializer_class
    
    def get_serializer_context(self):
        context = {'request': self.request}
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        if date_start and date_end:
            context['date_start'] = date_start
            context['date_end'] = date_end
        return context
    
    def get_instance(self):
        store_id = self.request.query_params.get('store')
        sku_id = self.request.query_params.get('sku')
        if not store_id or not sku_id:
            return Sales.objects.none()
        insanse = Sales.objects.filter(shop=store_id, product=sku_id).first()
        return insanse

    def list(self, request, *args, **kwargs):
        instance = self.get_instance()
        if not instance:
            return Response(
                {"error": "Не найдены данные с указанными параметрами"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance) 
        return Response({"data": serializer.data})

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


