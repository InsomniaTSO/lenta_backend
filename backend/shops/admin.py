from django.contrib import admin
from django.contrib.admin import register
from shops.v1.models import City, Division, Format, Location, Size, Shop


@register(City)
class CityAdmin(admin.ModelAdmin):
    """Админка городов."""
    list_display = ('city_id',)
    search_fields = ('city_id',)
    empty_value_display = '-пусто-'


@register(Division)
class DivisionAdmin(admin.ModelAdmin):
    """Админка дивизионов."""
    list_display = ('division_code_id',)
    search_fields = ('division_code_id',)
    empty_value_display = '-пусто-'


@register(Format)
class FormatAdmin(admin.ModelAdmin):
    """Админка форматов."""
    list_display = ('type_format_id',)
    search_fields = ('type_format_id',)
    empty_value_display = '-пусто-'


@register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Админка типов локаций."""
    list_display = ('type_loc_id',)
    search_fields = ('type_loc_id',)
    empty_value_display = '-пусто-'


@register(Size)
class SizeAdmin(admin.ModelAdmin):
    """Админка типов размеров магазинов."""
    list_display = ('type_size_id',)
    search_fields = ('type_size_id',)
    empty_value_display = '-пусто-'


@register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """Админка магазинов."""
    list_display = ('store', 'city', 'type_format', 'loc', 'size', 'is_active')
    search_fields = ('store', 'city', 'type_format', 'loc', 'size', 'is_active')
    empty_value_display = '-пусто-'