from datetime import timedelta

from rest_framework import serializers

from categories.v1.models import Product
from shops.v1.models import Shop

from .models import Forecast


class ForecastPostSerializer(serializers.ModelSerializer):
    """Сериализатор для отправки данных прогноза. 
    Позволяет отправить информацию о магазине, дате прогноза и прогнозе продаж.
    """

    class Meta:
        model = Forecast
        fields = ['store', 'forecast_date', 'forecast']

    def validate(self, data): 
        forecast_data = data.get('forecast') 
        # Проверяем наличие 'sku' в данных
        if 'sku' not in forecast_data: 
            raise serializers.ValidationError({'forecast': 'Поле "sku" отсутствует.'})
        product_sku = forecast_data.get('sku') 
        # Проверяем, что продукт с таким SKU существует
        if not Product.objects.filter(sku=product_sku).exists(): 
            raise serializers.ValidationError({'sku': 'Неверный SKU.'}) 
        data['product'] = Product.objects.get(sku=product_sku)
        # Проверяем наличие 'sales_units' в данных
        if 'sales_units' not in forecast_data: 
            raise serializers.ValidationError({'forecast': 'Поле "sales_units" отсутствует.'})
        # Проверяем, что первая дата в 'sales_units' соответствует 'forecast_date'
        first_sales_date = next(iter(forecast_data['sales_units']))
        if first_sales_date != str(data['forecast_date']):
            raise serializers.ValidationError({
                'forecast_date': f'Первая дата в "sales_units" ({first_sales_date}) не совпадает с "forecast_date" ({data["forecast_date"]}).'
            })
        return data
    
    def create(self, validated_data):
        forecast_data = validated_data.get('forecast')
        store = Shop.objects.get(store=validated_data.get('store'))
        sku = Product.objects.get(sku=forecast_data['sku'])
        forecast_date = validated_data.get('forecast_date')
        forecast = forecast_data['sales_units']
        if Forecast.objects.filter(store=store, 
                                   product=sku, 
                                   forecast_date=forecast_date).exists():
            Forecast.objects.filter(store=store, 
                                    product=sku, 
                                    forecast_date=forecast_date).update(forecast=forecast)
        else:
            Forecast.objects.create(store=store, 
                                    product=sku, 
                                    forecast_date=forecast_date,
                                    forecast=forecast)
        return validated_data


class ForecastGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных прогноза. 
    Предоставляет информацию о магазине, продукте и прогнозе продаж.
    """
    #store = serializers.CharField(source='store.store')
    sku = serializers.CharField(source='product.sku')
    group = serializers.CharField(source='product.group')
    forecast = serializers.DictField()
    forecast_date = serializers.DateField()
    category = serializers.CharField(source='product.category')
    subcategory = serializers.CharField(source='product.subcategory')
    uom = serializers.CharField(source='product.uom')

    class Meta:
        model = Forecast
        fields = ['store', 'sku', 'group', 'category', 'subcategory', 'uom', 'forecast_date', 'forecast']
