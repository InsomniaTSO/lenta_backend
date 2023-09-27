from django.contrib.admin import register
from django.contrib import admin
from sales.v1.models import Sales


@register(Sales)
class SalesAdmin(admin.ModelAdmin):
    """Админка продаж."""
    list_display = ('shop',  'product', 'date', 'sales_type_id', 'sales_in_units', 
                    'promo_sales_in_units', 'sales_in_rub', 'promo_sales_in_rub')
    search_fields = ('shop',  'product', 'date', 'sales_type_id')
    empty_value_display = '-пусто-'