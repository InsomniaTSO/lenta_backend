from django.db import models
from shops.models import Shop
from categories.models import Product
from api.consatants import DECIMAL_PLACES, FLAG_CHOICES, MAX_DIGITS


class Sales(models.Model):
    """Модель для хранения информации о продажах.
    """
    
    store = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField('дата')
    sales_type_id = models.PositiveSmallIntegerField('флаг наличия промо', choices=FLAG_CHOICES)
    sales_in_units = models.PositiveSmallIntegerField('продажи без промо в шт')
    promo_sales_in_units = models.PositiveSmallIntegerField('продажи c промо в шт')
    sales_in_rub = models.DecimalField('продажи в рублях без промо', max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    promo_sales_in_rub = models.DecimalField('продажи в рублях промо', max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
