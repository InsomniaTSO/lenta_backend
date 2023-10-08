from django.contrib import admin
from django.contrib.admin import register

from sales.v1.models import Sales


@register(Sales)
class SalesAdmin(admin.ModelAdmin):
    """Админка продаж."""
    list_display = ('shop', 'product', 'date', 'sales_type', 'sales_units',
                    'sales_units_promo', 'sales_rub', 'sales_run_promo')
    search_fields = ('shop', 'product', 'date', 'sales_type')
    empty_value_display = '-пусто-'
