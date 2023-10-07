import django_filters

from .models import Shop


class ShopFilter(django_filters.FilterSet):
    store = django_filters.AllValuesMultipleFilter(lookup_expr='icontains')
    city = django_filters.AllValuesMultipleFilter(field_name='city__city_id')
    division = django_filters.AllValuesMultipleFilter(field_name='division__division_code_id')
    type_format = django_filters.AllValuesMultipleFilter(field_name='type_format__type_format_id')
    loc= django_filters.AllValuesMultipleFilter(field_name='loc__type_loc_id')
    size = django_filters.AllValuesMultipleFilter(field_name='size__type_size_id')
    is_active = django_filters.ChoiceFilter(choices=[(0, 'Неактивный'), (1, 'Активный')])

    class Meta:
        model = Shop
        fields = [
            'store',
            'city',
            'division',
            'type_format',
            'loc',
            'size',
            'is_active'
        ]
