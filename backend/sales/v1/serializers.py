from categories.v1.models import Product
from lenta_backend.constants import DECIMAL_PLACES, MAX_DIGITS
from rest_framework import serializers
from sales.v1.models import Sales
from shops.v1.models import Shop


class SalesSerializer(serializers.ModelSerializer):
    """Основной сериализатор для объектов Sales. 
       Включает в себя информацию фактических данных о продажах. 
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
        date_start = self.context.get('date_start')
        date_end = self.context.get('date_end')
        shop = obj.shop
        product = obj.product
        sales = Sales.objects.filter(shop=shop, product=product)
        if date_start and date_end:
            sales = sales.filter(date__range=(date_start, date_end))
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
    sales_run_promo = serializers.DecimalField(MAX_DIGITS, DECIMAL_PLACES) 

    class Meta:
        model = Sales
        fields = ('date', 'sales_type', 'sales_units',
                  'sales_units_promo', 'sales_rub', 
                  'sales_run_promo')


class SalesFactSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки информации о продажах. 
    """

    store = serializers.CharField()
    sku = serializers.CharField()
    fact = serializers.ListField(child=FactSerializer())

    class Meta:
        model = Sales
        fields = ('store', 'sku', 'fact')

    def create(self, validated_data):
        store = Shop.objects.get(store=validated_data.get('store'))
        sku = Product.objects.get(sku=validated_data.get('sku'))
        fact = validated_data.get('fact')
        for f in fact:
            if Sales.objects.filter(shop=store, product=sku, date=f['date']).exists():
                Sales.objects.filter(shop=store, product=sku, 
                                    date=f['date']).update(sales_type=f['sales_type'],
                                    sales_units=f['sales_units'],
                                    sales_units_promo=f['sales_units_promo'],
                                    sales_rub=f['sales_rub'],
                                    sales_run_promo=f['sales_run_promo'])
            else:
                Sales.objects.create(shop=store, product=sku, 
                                    date=f['date'], sales_type=f['sales_type'],
                                    sales_units=f['sales_units'],
                                    sales_units_promo=f['sales_units_promo'],
                                    sales_rub=f['sales_rub'],
                                    sales_run_promo=f['sales_run_promo'])
            
        return validated_data