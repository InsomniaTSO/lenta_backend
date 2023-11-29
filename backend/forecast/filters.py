from django_filters import AllValuesMultipleFilter, DateFilter, FilterSet

from .models import Forecast


class ForecastFilter(FilterSet):
    """Фильтр для прогнозов. Позволяет фильтровать прогнозы по дате прогноза,
    магазину, продукту и по связанным с ними полям.
    """

    store = AllValuesMultipleFilter(
        field_name="store__store",
    )
    sku = AllValuesMultipleFilter(field_name="product__sku")
    forecast_date = DateFilter(field_name="forecast_date")
    city = AllValuesMultipleFilter(field_name="store__city__city_id")
    division = AllValuesMultipleFilter(
        field_name="store__division__division_code_id"
    )
    type_format = AllValuesMultipleFilter(
        field_name="store__type_format__type_format_id"
    )
    location = AllValuesMultipleFilter(
        field_name="store__loc__type_loc_id"
    )
    size = AllValuesMultipleFilter(
        field_name="store__size__type_size_id"
    )
    is_active = AllValuesMultipleFilter(field_name="store__is_active")
    group = AllValuesMultipleFilter(
        field_name="product__group__group_id"
    )
    category = AllValuesMultipleFilter(
        field_name="product__category__cat_id"
    )
    subcategory = AllValuesMultipleFilter(
        field_name="product__subcategory__subcat_id"
    )
    uom = AllValuesMultipleFilter(field_name="product__uom")

    class Meta:
        model = Forecast
        fields = [
            "store",
            "sku",
            "forecast_date",
            "city",
            "division",
            "type_format",
            "location",
            "size",
            "is_active",
            "group",
            "category",
            "subcategory",
            "uom",
        ]
