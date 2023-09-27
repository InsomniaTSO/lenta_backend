from django.contrib import admin
from django.contrib.admin import register
from .v1.models import Forecast, ForPrediction


@register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    """Админка прогноза."""
    list_display = ('store', 'product', 'date', 'target')
    search_fields = ('store', 'product', 'date', 'target')
    empty_value_display = '-пусто-'


@register(ForPrediction)
class ForPredictionAdmin(admin.ModelAdmin):
    """Админка запроса на прогноз."""
    list_display = ('store', 'product',)
    search_fields = ('store', 'product',)
    empty_value_display = '-пусто-'
