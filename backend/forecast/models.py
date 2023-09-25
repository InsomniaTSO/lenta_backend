from django.db import models
from shops.models import Shop
from categories.models import Product


class Forecast(models.Model):
    """Модель для хранения результатов прогноза.
    """

    store = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField('дата')
    target = models.PositiveSmallIntegerField('спрос в шт')


class ForPrediction(models.Model):
    """Модель для хранения данных, необходимых для создания прогноза.
    """

    store = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)



