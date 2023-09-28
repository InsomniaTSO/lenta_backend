from rest_framework import serializers 
from .models import Forecast
from categories.v1.models import Product
from shops.v1.models import Shop


class ForecastPostSerializer(serializers.Serializer): 
    store = serializers.CharField(write_only=True) 
    forecast_date = serializers.DateField(write_only=True) 
    forecast = serializers.DictField( 
        child=serializers.DictField( 
            child=serializers.IntegerField(), 
        ) 
    ) 
 
    def create(self, validated_data): 
        store_id = validated_data['store'] 
        # forecast_date = validated_data['forecast_date'] 
        forecast_data = validated_data['forecast']
        for sku, sales_units in forecast_data.items(): 
            product = Product.objects.get(sku=sku) 
            store = Shop.objects.get(store=store_id)
            for date, units in sales_units.items(): 
                Forecast.objects.create( 
                    store=store, 
                    product=product, 
                    date=date, 
                    target=units 
                )
        return validated_data 
 
class ForecastGetSerializer(serializers.ModelSerializer):    
    
    class Meta: 
        model = Forecast        
        fields = ('store', 'product', 'date', 'target')
