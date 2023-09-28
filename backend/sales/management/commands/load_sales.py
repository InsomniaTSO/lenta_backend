
import os
import csv
from django.core.management import BaseCommand
from shops.v1.models import Shop
from categories.v1.models import Product
from sales.v1.models import Sales
import logging

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    """Добавляет данные из data/st_df.csv в базу данных."""
    help = "python manage.py load_sales"
    
    def handle(self, *args, **options):
        path_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname( __file__ )))), 'data/sales_df_train.csv')
        if Sales.objects.exists():
            logging.info('Данные для продаж уже загружены')
            return
        logging.info('Загрузка данных продаж')
        with open(path_file, encoding='utf-8') as file:
            csvfilereader = csv.reader(file, delimiter=",")
            next(csvfilereader)
            for row in csvfilereader:
                shop = Shop.objects.get(store=row[0])
                product = Product.objects.get(sku=row[1])
                Sales.objects.get_or_create(shop=shop, product=product, 
                                            date=row[2],  
                                            sales_type_id=row[3], 
                                            sales_in_units=int(float(row[4])),
                                            promo_sales_in_units=int(float(row[5])),
                                            sales_in_rub=row[6],
                                            promo_sales_in_rub=row[7])
        logging.info('Загрузка завершена успешно')
