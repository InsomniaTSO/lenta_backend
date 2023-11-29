from django.db import models

from lenta_backend.constants import FLAG_CHOICES, MAX_ID_FIELD_LENGTH


class City(models.Model):
    """Модель для хранения информации о городах."""

    city_id = models.CharField("id города", max_length=MAX_ID_FIELD_LENGTH)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return str(self.city_id)


class Division(models.Model):
    """Модель для хранения информации о дивизионах."""

    division_code_id = models.CharField("id дивизиона",
                                        max_length=MAX_ID_FIELD_LENGTH)

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"

    def __str__(self):
        return str(self.division_code_id)


class Format(models.Model):
    """Модель для хранения информации о форматах магазинов."""

    type_format_id = models.IntegerField("id формата магазина")

    class Meta:
        verbose_name = "Формат"
        verbose_name_plural = "Форматы"

    def __str__(self):
        return str(self.type_format_id)


class Location(models.Model):
    """Модель для хранения информации о типах локаций магазинов."""

    type_loc_id = models.IntegerField("id локации магазина")

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return str(self.type_loc_id)


class Size(models.Model):
    """Модель для хранения информации о размерах магазинов."""

    type_size_id = models.IntegerField("id типа размера магазина")

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"

    def __str__(self):
        return str(self.type_size_id)


class Shop(models.Model):
    """Модель для хранения информации о магазинах."""

    store = models.CharField(
        "id магазина", max_length=MAX_ID_FIELD_LENGTH, primary_key=True
    )
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, related_name="shops", null=True
    )
    division = models.ForeignKey(
        Division, on_delete=models.SET_NULL, related_name="shops", null=True
    )
    type_format = models.ForeignKey(
        Format, on_delete=models.SET_NULL, related_name="shops", null=True
    )
    loc = models.ForeignKey(
        Location, on_delete=models.SET_NULL, related_name="shops", null=True
    )
    size = models.ForeignKey(
        Size, on_delete=models.SET_NULL, related_name="shops", null=True
    )

    is_active = models.PositiveSmallIntegerField(
        "флаг активного магазина", choices=FLAG_CHOICES
    )

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def __str__(self):
        return str(self.store)
