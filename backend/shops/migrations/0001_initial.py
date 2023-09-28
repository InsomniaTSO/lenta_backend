# Generated by Django 3.2.15 on 2023-09-28 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_id', models.CharField(max_length=100, verbose_name='id города')),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division_code_id', models.CharField(max_length=100, verbose_name='id дивизиона')),
            ],
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_format_id', models.IntegerField(verbose_name='id формата магазина')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_loc_id', models.IntegerField(verbose_name='id локации магазина')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_size_id', models.IntegerField(verbose_name='id типа размера магазина')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('store', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='id магазина')),
                ('is_active', models.PositiveSmallIntegerField(choices=[(0, 'НЕТ'), (1, 'ДА')], verbose_name='флаг активного магазина')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shops', to='shops.city')),
                ('division', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shops', to='shops.division')),
                ('loc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shops', to='shops.location')),
                ('size', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shops', to='shops.size')),
                ('type_format', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shops', to='shops.format')),
            ],
        ),
    ]
