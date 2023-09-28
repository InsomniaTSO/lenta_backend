from rest_framework import serializers
from categories.v1.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор товарной иерархии."""
    
    class Meta:
        model = Product
        fields = ('sku', 'group', 'category', 'subcategory', 'uom')