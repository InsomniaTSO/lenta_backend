from django.db import models
from shops.v1.models import Shop
from categories.v1.models import Product


class Forecast(models.Model):
    """Модель для хранения результатов прогноза.
    """

    store = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='forecast')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='forecast')
    date = models.DateField('дата')
    target = models.PositiveSmallIntegerField('спрос в шт')

    def __str__(self):
        return f'Прогноз для магазина {self.store} по продукту {self.product}'
  

class ForPrediction(models.Model):
    """Модель для хранения данных, необходимых для создания прогноза.
    """

    store = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='for_prediction')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='for_prediction')

    def __str__(self):
        return f'Данные для прогноза для магазина {self.store} по продукту {self.product}'
