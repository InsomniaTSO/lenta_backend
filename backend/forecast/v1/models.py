from django.db import models

from categories.v1.models import Product
from shops.v1.models import Shop


class Forecast(models.Model):  
    """Модель для хранения информации о прогнозе продаж."""  
    store = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='forecasts')  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='forecasts')  
    forecast_date = models.DateField('Дата составления прогноза') 
    date = models.DateField('Прогноз на дату', default="2022-01-01")
    target = models.IntegerField('Прогноз', default=0)
      
    class Meta:  
        verbose_name = 'Прогноз продаж'  
        verbose_name_plural = 'Прогнозы продаж'  
        constraints = [  
            models.UniqueConstraint(  
                fields=['store', 'forecast_date', 'product', 'date'],  
                name='unique_forecast'  
            ),  
        ]

    def __str__(self): 
        return f'Прогноз для магазина {self.store}, продукта {self.product} на дату {self.forecast_date}'
