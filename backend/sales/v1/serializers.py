from rest_framework import serializers
from sales.v1.models import Sales


class SalesFactSerializer(serializers.Serializer):
    """Сериализатор для представления информации о фактических продажах. 
    """
    date = serializers.DateField() 
    sales_type = serializers.IntegerField(source='sales_type_id') 
    sales_units = serializers.IntegerField(source='sales_in_units') 
    sales_units_promo = serializers.IntegerField(source='promo_sales_in_units') 
    sales_rub = serializers.DecimalField(decimal_places=2, source='sales_in_rub') 
    sales_rub_promo = serializers.DecimalField(decimal_places=2, source='promo_sales_in_rub') 


class SalesSerializer(serializers.ModelSerializer):
    """Основной сериализатор для объектов Sales. Включает в себя информацию о магазине, SKU товара и фактические данные о продажах. 
    Использует SalesFactSerializer для сериализации фактических данных о продажах. 
    """
    store = serializers.StringRelatedField(source='store.store_id') 
    sku = serializers.StringRelatedField(source='product.sku_id') 
    fact = SalesFactSerializer(many=True, source='sales_set') 
 
    class Meta: 
        model = Sales 
        fields = ('store', 'sku', 'fact')