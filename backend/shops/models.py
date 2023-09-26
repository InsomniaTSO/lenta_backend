from django.db import models
from api.consatants import MAX_ID_FIELD_LENGTH, FLAG_CHOICES


class City(models.Model):
    """Модель для хранения информации о городах.
    """
    
    city_id = models.CharField('id города', max_length=MAX_ID_FIELD_LENGTH)


class Division(models.Model):
    """Модель для хранения информации о дивизионах.
    """

    division_code_id = models.CharField('id дивизиона', max_length=MAX_ID_FIELD_LENGTH)


class Format(models.Model):
    """Модель для хранения информации о форматах магазинов.
    """

    type_format_id = models.CharField('id формата магазина', max_length=MAX_ID_FIELD_LENGTH)


class Location(models.Model):
    """Модель для хранения информации о типах локаций магазинов.
    """

    type_loc_id = models.CharField('id локации магазина', max_length=MAX_ID_FIELD_LENGTH)


class Size(models.Model):
    """Модель для хранения информации о размерах магазинов.
    """

    type_loc_id = models.CharField('id типа размера магазина', max_length=MAX_ID_FIELD_LENGTH)


class Shop(models.Model):
    """Модель для хранения информации о магазинах.
    """

    store_id = models.CharField('id магазина', max_length=MAX_ID_FIELD_LENGTH, primary_key=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    division_code = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    type_format = models.ForeignKey(Format, on_delete=models.SET_NULL, null=True)
    type_loc_id = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    type_size_id = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)
    is_active = models.PositiveSmallIntegerField('флаг активного магазина', choices=FLAG_CHOICES)