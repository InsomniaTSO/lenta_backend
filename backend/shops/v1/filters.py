import django_filters
from .models import Shop

class ShopFilter(django_filters.FilterSet):
    store = django_filters.CharFilter(lookup_expr='icontains')
    city__city_id = django_filters.CharFilter(lookup_expr='icontains')
    division__division_code_id = django_filters.CharFilter(lookup_expr='icontains')
    type_format__type_format_id = django_filters.NumberFilter()
    loc__type_loc_id = django_filters.NumberFilter()
    size__type_size_id = django_filters.NumberFilter()
    is_active = django_filters.NumberFilter()

    class Meta:
        model = Shop
        fields = [
            'store',
            'city__city_id',
            'division__division_code_id',
            'type_format__type_format_id',
            'loc__type_loc_id',
            'size__type_size_id',
            'is_active'
        ]
