from django.db import models
from django.db.models import JSONField

from categories.v1.models import Product
from shops.v1.models import Shop


class Forecast(models.Model):  
    """Модель для хранения информации о прогнозе продаж."""  
    store = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='forecasts')  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='forecasts')  
    forecast_date = models.DateField('Дата начала прогноза') 
    forecast = JSONField('Прогноз на 14 дней', default=dict)
      
    class Meta:  
        verbose_name = 'Прогноз продаж'  
        verbose_name_plural = 'Прогнозы продаж'  
        constraints = [  
            models.UniqueConstraint(  
                fields=['store', 'forecast_date', 'product'],  
                name='unique_forecast'  
            ),  
        ] 

    def __str__(self): 
        return f'Прогноз для магазина {self.store}, продукта {self.product} начиная с {self.forecast_date}'
