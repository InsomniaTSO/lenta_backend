from django.db import models

from lenta_backend.constants import MAX_ID_FIELD_LENGTH, UOM_CHOICES


class Group(models.Model):
    """Группа товара.
    """
    group_id = models.CharField(
        'id группы',
        max_length=MAX_ID_FIELD_LENGTH,
        primary_key=True
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return str(self.group_id)


class Category(models.Model):
    """Категория товара.
    """
    cat_id = models.CharField(
        'id категории товара',
        max_length=MAX_ID_FIELD_LENGTH,
        primary_key=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.cat_id)


class Subcategory(models.Model):
    """Подкатегория товара.
    """
    subcat_id = models.CharField(
        'id подкатегории товара',
        max_length=MAX_ID_FIELD_LENGTH,
        primary_key=True
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return str(self.subcat_id)


class Product(models.Model):
    """Иерархия для товара.
    """

    sku = models.CharField(
        'id товара', max_length=MAX_ID_FIELD_LENGTH, primary_key=True
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='products', null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='products', null=True
    )
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.SET_NULL,
        related_name='products', null=True
    )
    uom = models.PositiveSmallIntegerField(
        'маркер продажи на вес', choices=UOM_CHOICES
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return str(self.sku)
