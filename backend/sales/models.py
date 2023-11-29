from django.db import models

from categories.models import Product
from lenta_backend.constants import DECIMAL_PLACES, FLAG_CHOICES, MAX_DIGITS
from shops.models import Shop


class Sales(models.Model):
    """Модель для хранения информации о продажах."""

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, 
                             related_name="sales")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                related_name="sales")
    date = models.DateField("дата")
    sales_type = models.PositiveSmallIntegerField(
        "флаг наличия промо", choices=FLAG_CHOICES
    )
    sales_units = models.PositiveSmallIntegerField("продажи без промо в шт")
    sales_units_promo = models.PositiveSmallIntegerField("продажи c промо в шт")
    sales_rub = models.DecimalField(
        "продажи в рублях без промо",
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
    )
    sales_run_promo = models.DecimalField(
        "продажи в рублях промо", max_digits=MAX_DIGITS, 
        decimal_places=DECIMAL_PLACES
    )

    class Meta:
        verbose_name = "Продажи"
        verbose_name_plural = "Продажи"

    def __str__(self):
        return (
            f"Sales: Shop ID - {self.shop.store}, " f"Product SKU - {self.product.sku}"
        )
