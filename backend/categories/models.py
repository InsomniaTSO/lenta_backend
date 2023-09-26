from django.db import models
from api.consatants import MAX_ID_FIELD_LENGTH, UOM_CHOICES


class Group(models.Model):
    """Группа товара.
    """  
    group_id = models.CharField('id группы', max_length=MAX_ID_FIELD_LENGTH, primary_key=True)


class Category(models.Model):
    """Категория товара.
    """  
    cat_id = models.CharField('id категории товара', max_length=MAX_ID_FIELD_LENGTH, primary_key=True)


class Subcategory(models.Model):
    """Подкатегория товара.
    """  
    subcat_id = models.CharField('id подкатегории товара', max_length=MAX_ID_FIELD_LENGTH, primary_key=True)


class Product(models.Model):
    """Иерархия для товара.
    """

    sku_id = models.CharField('id товара', max_length=MAX_ID_FIELD_LENGTH, primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    cat_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcat_id = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    uom_id = models.PositiveSmallIntegerField('маркер продажи на вес', choices=UOM_CHOICES)
