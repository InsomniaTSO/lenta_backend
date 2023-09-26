from rest_framework import serializers
from categories.models import Category


class CategoriesViewSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""
    
    class Meta:
        model = Category
        fields = ('sku_id', 'group', 'cat_id', 'subcat_id', 'subcat_id', 'uom_id')
