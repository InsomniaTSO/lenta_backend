from django_filters import AllValuesMultipleFilter, FilterSet

from .models import Sales


class SalesFilter(FilterSet):
    """Фильтр для прогнозов. Позволяет фильтровать прогнозы по дате прогноза,
    магазину, продукту и по связанным с ними полям.
    """

    store = AllValuesMultipleFilter(field_name="shop__store")
    sku = AllValuesMultipleFilter(field_name="product__sku")

    class Meta:
        model = Sales
        fields = ["store", "sku"]
