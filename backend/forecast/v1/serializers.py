from rest_framework import serializers 
from .models import Forecast
from categories.v1.models import Product
from shops.v1.models import Shop


class ForecastPostSerializer(serializers.Serializer): 
    pass
 

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
