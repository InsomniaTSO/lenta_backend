import collections
from rest_framework import serializers
from categories.v1.models import Product
from shops.v1.models import Shop

from .models import Forecast


class ForecastPostSerializer(serializers.ModelSerializer):
    """Сериализатор для отправки данных прогноза.
    Позволяет отправить информацию о магазине, дате прогноза и прогнозе продаж.
    """
    sku = serializers.StringRelatedField(source='product.sku')

    class Meta:
        model = Forecast
        fields = ('store', 'sku', 'forecast_date')

    def create(self, data):
        print(data)
        forecast_data = data.get('forecast')
        store = Shop.objects.get(store=data.get('store'))
        sku = Product.objects.get(sku=forecast_data['sku'])
        forecast_date = data.get('forecast_date')
        forecast = forecast_data['sales_units']
        for key, value in forecast.items():
            obj = Forecast.objects.filter(store=store, product=sku,
                                          forecast_date=forecast_date,
                                          date=key)
            if obj.exists():
                obj.update(target=value)
            else:
                Forecast.objects.create(store=store,
                                        product=sku,
                                        forecast_date=forecast_date,
                                        date=key,
                                        target=value)
        return data


class ForecastGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных прогноза.
    Предоставляет информацию о магазине, продукте и прогнозе продаж.
    """
    store = serializers.StringRelatedField(source='store.store')
    sku = serializers.StringRelatedField(source='product.sku')
    forecast = serializers.SerializerMethodField(method_name='get_forecast')
    group = serializers.CharField(source='product.group')
    category = serializers.CharField(source='product.category')
    subcategory = serializers.CharField(source='product.subcategory')
    uom = serializers.CharField(source='product.uom')

    class Meta:
        model = Forecast
        fields = [
            'store',
            'sku',
            'group',
            'category',
            'subcategory',
            'uom',
            'forecast_date',
            'forecast'
        ]

    def get_forecast(self, obj):
        store = obj.store
        product = obj.product
        forecast_date = obj.forecast_date
        forecasts = Forecast.objects.filter(store=store, product=product,
                                            forecast_date=forecast_date)
        forecast = collections.OrderedDict()
        for f in forecasts:
            forecast[str(f.date)] = f.target
        return dict(forecast)
