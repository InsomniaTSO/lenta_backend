from django_filters import AllValuesMultipleFilter, NumberFilter, FilterSet

from categories.models import Product


class ProductFilter(FilterSet):
    sku = AllValuesMultipleFilter(lookup_expr="icontains")
    group = AllValuesMultipleFilter(field_name="group__group_id")
    category = AllValuesMultipleFilter(field_name="category__cat_id")
    subcategory = AllValuesMultipleFilter(
        field_name="subcategory__subcat_id"
    )
    uom = NumberFilter(lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["sku", "group", "category", "subcategory", "uom"]
