from django_filters import AllValuesMultipleFilter, ChoiceFilter, FilterSet

from .models import Shop


class ShopFilter(FilterSet):
    """Фильтр для магазинов. Позволяет фильтровать магазины по id,
    городам, подразделением, типу, локации, размеру, флага 'is_active'.
    """

    store = AllValuesMultipleFilter(lookup_expr="icontains")
    city = AllValuesMultipleFilter(field_name="city__city_id")
    division = AllValuesMultipleFilter(field_name="division__division_code_id")
    type_format = AllValuesMultipleFilter(field_name="type_format__type_format_id")
    loc = AllValuesMultipleFilter(field_name="loc__type_loc_id")
    size = AllValuesMultipleFilter(field_name="size__type_size_id")
    is_active = ChoiceFilter(choices=[(0, "Неактивный"), (1, "Активный")])

    class Meta:
        model = Shop
        fields = [
            "store",
            "city",
            "division",
            "type_format",
            "loc",
            "size",
            "is_active",
        ]
