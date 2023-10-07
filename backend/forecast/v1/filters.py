import django_filters

from .models import Forecast


class ForecastFilter(django_filters.FilterSet):
    """Фильтр для прогнозов. Позволяет фильтровать прогнозы по дате прогноза,
    магазину, продукту и по связанным с ними полям.
    """
    store = django_filters.AllValuesMultipleFilter(field_name='store__store', )
    product = django_filters.AllValuesMultipleFilter(field_name='product__sku')
    forecast_date = django_filters.DateFilter(field_name='forecast_date')
    city = django_filters.AllValuesMultipleFilter(field_name='store__city__city_id')
    division = django_filters.AllValuesMultipleFilter(field_name='store__division__division_code_id')
    type_format = django_filters.AllValuesMultipleFilter(field_name='store__type_format__type_format_id')
    location = django_filters.AllValuesMultipleFilter(field_name='store__loc__type_loc_id')
    size = django_filters.AllValuesMultipleFilter(field_name='store__size__type_size_id')
    is_active = django_filters.AllValuesMultipleFilter(field_name='store__is_active')
    group = django_filters.AllValuesMultipleFilter(field_name='product__group__group_id')
    category = django_filters.AllValuesMultipleFilter(field_name='product__category__cat_id')
    subcategory = django_filters.AllValuesMultipleFilter(field_name='product__subcategory__subcat_id')
    uom = django_filters.AllValuesMultipleFilter(field_name='product__uom')


    class Meta:
        model = Forecast
        fields = [
            'store',
            'product',
            'forecast_date',
            'city',
            'division',
            'type_format',
            'location',
            'size',
            'is_active',
            'group',
            'category',
            'subcategory',
            'uom'
        ]
