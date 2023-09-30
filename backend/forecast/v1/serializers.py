from rest_framework import serializers 
from .models import Forecast
from categories.v1.models import Product
from shops.v1.models import Shop


class ForecastPostSerializer(serializers.Serializer):  
    store = serializers.CharField(help_text='Укажите уникальный идентификатор магазина')  
    forecast_date = serializers.DateField(help_text='Укажите дату прогноза в формате YYYY-MM-DD')  
    forecast = serializers.DictField(  
        help_text='Укажите прогноз в формате {"SKU": {"Дата": Количество проданных единиц}}',
        child=serializers.DictField(  
            help_text='Укажите SKU и соответствующий ему прогноз',
            child=serializers.IntegerField(help_text='Укажите дату и ожидаемое количество проданных единиц'),
        ) 
    ) 
     
    def create(self, validated_data): 
        store_id = validated_data.get('store') 
        # forecast_date = validated_data.get('forecast_date') 
        forecast_data = validated_data.get('forecast') 
         
        store = Shop.objects.get(store=store_id) 
         
        for sku, sales_units in forecast_data.items(): 
            product = Product.objects.get(sku=sku) 
            for date, target in sales_units.items(): 
                Forecast.objects.create( 
                    store=store, 
                    product=product, 
                    date=date, 
                    target=target 
                ) 
        return validated_data


class ForecastGetSerializer(serializers.Serializer): 
    store = serializers.CharField()
    sku = serializers.CharField()  
    forecast_date = serializers.DateField() 
    forecast = serializers.DictField(child=serializers.IntegerField())

    def get_forecast(self, obj_list):
        forecast_dict = {}
        for obj in obj_list:
            date_str = obj.date.strftime('%Y-%m-%d')
            forecast_dict[date_str] = obj.target
        return forecast_dict
