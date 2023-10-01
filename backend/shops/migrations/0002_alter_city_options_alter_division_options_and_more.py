# Generated by Django 4.2.5 on 2023-09-30 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'Город', 'verbose_name_plural': 'Города'},
        ),
        migrations.AlterModelOptions(
            name='division',
            options={'verbose_name': 'Подразделение', 'verbose_name_plural': 'Подразделения'},
        ),
        migrations.AlterModelOptions(
            name='format',
            options={'verbose_name': 'Формат', 'verbose_name_plural': 'Форматы'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'Локация', 'verbose_name_plural': 'Локации'},
        ),
        migrations.AlterModelOptions(
            name='shop',
            options={'verbose_name': 'Магазин', 'verbose_name_plural': 'Магазины'},
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'verbose_name': 'Размер', 'verbose_name_plural': 'Размеры'},
        ),
    ]