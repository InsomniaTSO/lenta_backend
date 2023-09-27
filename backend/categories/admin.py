from django.contrib import admin
from django.contrib.admin import register

from categories.v1.models import Group, Category, Subcategory, Product

@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка категорий товара."""
    list_display = ('cat_id',)
    search_fields = ('cat_id',)
    empty_value_display = '-пусто-'


@register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Админка групп товара."""
    list_display = ('group_id',)
    search_fields = ('group_id',)
    empty_value_display = '-пусто-'


@register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """Админка подкатегорий товара."""
    list_display = ('subcat_id',)
    search_fields = ('subcat_id',)
    empty_value_display = '-пусто-'


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка товара."""
    list_display = ('sku_id', 'group', 'category', 'subcategory', 'uom_id')
    search_fields = ('sku_id', 'group', 'category', 'subcategory', 'uom_id')
    empty_value_display = '-пусто-'
