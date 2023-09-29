# Generated by Django 4.2.5 on 2023-09-29 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('shops', '0001_initial'),
        ('forecast', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecast', to='categories.product'),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecast', to='shops.shop'),
        ),
        migrations.AlterField(
            model_name='forprediction',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='for_prediction', to='categories.product'),
        ),
        migrations.AlterField(
            model_name='forprediction',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='for_prediction', to='shops.shop'),
        ),
    ]
