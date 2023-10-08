from django.contrib import admin
from django.contrib.admin import register

from .v1.models import Forecast


@register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    """Админка прогноза."""
    list_display = ('store', 'product', 'forecast_date', 'date', 'target')
    search_fields = ('store', 'product', 'forecast_date')
    empty_value_display = '-пусто-'
