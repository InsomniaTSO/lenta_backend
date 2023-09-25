from django.db import models
from hashids import HashidField


UOM_CHOICES = (
    (1, 'Шт'),
    (2, 'Руб'),
)


class Product(models.Model):
    """Модель для хранения информации о товарах.
    """
    sku_id = HashidAutoField(salt='sku_salt', allow_int_lookup=True, primary_key=True)
    group_id = HashidField(salt='group_salt')
    cat_id = HashidField(salt='cat_salt', allow_int_lookup=True)
    subcat_id = HashidField(salt='subcat_salt', allow_int_lookup=True)
    uom_id = models.PositiveSmallIntegerField(choices=UOM_CHOICES)


class Store(models.Model):
    """Модель для хранения информации о магазинах.
    """

    store_id = HashidAutoField(salt='store_salt', allow_int_lookup=True, primary_key=True)
    city_id = HashidField(salt='city_salt', allow_int_lookup=True)
    division_code = HashidField(salt='dc_salt', allow_int_lookup=True)
    type_format_id = models.PositiveSmallIntegerField()
    type_loc_id = models.PositiveSmallIntegerField()
    type_size_id = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)


class Sales(models.Model):
    """Модель для хранения информации о продажах.
    """

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    sales_type_id = models.BooleanField(default=False)
    sales_in_units = models.IntegerField()
    promo_sales_in_units = models.IntegerField()
    sales_in_rub = models.DecimalField(max_digits=15, decimal_places=2)
    promo_sales_in_rub = models.DecimalField(max_digits=15, decimal_places=2)


class ForPrediction(models.Model):
    """Модель для хранения данных, необходимых для создания прогноза.
    """

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()


class Forecast(models.Model):
    """Модель для хранения результатов прогноза.
    """

    for_prediction = models.ForeignKey(ForPrediction, on_delete=models.CASCADE)
    target = models.IntegerField()
