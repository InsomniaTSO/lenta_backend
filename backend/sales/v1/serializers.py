from rest_framework import serializers
from sales.v1.models import Sales
from lenta_backend.consatants import DECIMAL_PLACES, MAX_DIGITS


class SalesSerializer(serializers.ModelSerializer):
    """Основной сериализатор для объектов Sales. Включает в себя информацию фактических данных о продажах. 
    """
    
    class Meta: 
        model = Sales 
        fields = ('date', 'sales_type', 'sales_units',
                  'sales_units_promo', 'sales_rub', 
                  'sales_run_promo')


class SalesGroupSerializer(serializers.ModelSerializer):
    """Сериализатор группировки данных по магазину и товару. 
    """
    store = serializers.StringRelatedField(source='shop.store')
    sku = serializers.StringRelatedField(source='product.sku')
    fact = serializers.SerializerMethodField(method_name='get_fact')

    class Meta: 
        model = Sales 
        fields = ('store', 'sku', 'fact')

    def get_fact(self, obj):
        shop = obj.shop
        product = obj.product
        sales = Sales.objects.filter(shop=shop, product=product)
        sales_serializer = SalesSerializer(sales, many=True)
        return sales_serializer.data


class FactSerializer(serializers.ModelSerializer):
    """Сериализатор для представления информации о фактических продажах. 
    """
    date = serializers.DateField() 
    sales_type = serializers.IntegerField() 
    sales_units = serializers.IntegerField() 
    sales_units_promo = serializers.IntegerField() 
    sales_rub = serializers.DecimalField(MAX_DIGITS, DECIMAL_PLACES) 
    sales_rub_promo = serializers.DecimalField(MAX_DIGITS, DECIMAL_PLACES) 

    class Meta:
        model = Sales
        fields = ('date', 'sales_type', 'sales_units',
                  'sales_units_promo', 'sales_rub', 
                  'sales_run_promo')


class SalesFactSerializer(serializers.Serializer):
    store = serializers.StringRelatedField(source='shop.store')
    sku = serializers.StringRelatedField(source='product.sku')
    fact = serializers.ListField(child=SalesSerializer())

    class Meta:
        model = Sales
        fields = ('store', 'sku', 'date', 'sales_type', 'sales_units',
                  'sales_units_promo', 'sales_rub', 
                  'sales_run_promo'
                  )
        
    def create(self, validated_data):
        store = validated_data.get('store')
        sku = validated_data.get('sku')
        fact = validated_data.get('fact')
        for f in fact:
            sale = Sales.objects.create(shop=store, 
                                        product=sku, 
                                        date=f['date'],
                                        sales_type=f['sales_type'],
                                        sales_units=f['sales_units'],
                                        sales_units_promo=f['sales_units_promo'],
                                        sales_rub=f['sales_rub'],
                                        sales_run_promo=f['sales_run_promo'])
            return validated_data