from rest_framework import serializers
from datetime import timedelta
from .models import Forecast
from categories.v1.models import Product


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
        # # Проверяем, что прогноз составлен на 14 дней
        # sales_dates = list(forecast['sales_units'].keys())
        # if len(sales_dates) != 14:
        #     raise serializers.ValidationError({
        #         'forecast': 'Данные "sales_units" должны содержать прогноз на 14 дней.'
        #     })
        # # Проверяем, что даты в прогнозе идут по порядку
        # current_date = data['forecast_date']
        # for date_str in sales_dates:
        #     if date_str != str(current_date):
        #         raise serializers.ValidationError({
        #             'forecast': f'Данные "sales_units" содержат неверную дату {date_str}. Ожидалось {current_date}.'
        #         })
        #     current_date += timedelta(days=1)
        return data

class ForecastGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных прогноза. 
    Предоставляет информацию о магазине, продукте и прогнозе продаж.
    """
    store = serializers.CharField(source='store.store')
    sku = serializers.CharField(source='product.sku')
    forecast = serializers.DictField()
    forecast_date = serializers.DateField()
    
    class Meta:
        model = Forecast
        fields = ['store', 'sku', 'forecast_date', 'forecast']
