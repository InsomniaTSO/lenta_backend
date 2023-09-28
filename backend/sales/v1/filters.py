import django_filters
from sales.v1.models import Sales

class SalesFilter(django_filters.FilterSet):
    
    class Meta:
        model = Sales
        fields = ['shop', 'product']
