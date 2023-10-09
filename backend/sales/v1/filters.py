import django_filters

from .models import Sales


class SalesFilter(django_filters.FilterSet):
    """Фильтр для прогнозов. Позволяет фильтровать прогнозы по дате прогноза,
    магазину, продукту и по связанным с ними полям.
    """
    store = django_filters.AllValuesMultipleFilter(field_name='shop__store')
    sku = django_filters.AllValuesMultipleFilter(field_name='product__sku')

    class Meta:
        model = Sales
        fields = [
            'store',
            'sku'
        ]
