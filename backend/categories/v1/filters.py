import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    sku = django_filters.AllValuesMultipleFilter(
        lookup_expr='icontains'
    )
    group = django_filters.AllValuesMultipleFilter(
        field_name='group__group_id'
    )
    category = django_filters.AllValuesMultipleFilter(
        field_name='category__cat_id'
    )
    subcategory = django_filters.AllValuesMultipleFilter(
        field_name='subcategory__subcat_id'
    )
    uom = django_filters.NumberFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = [
            'sku', 'group',
            'category', 'subcategory',
            'uom'
        ]
