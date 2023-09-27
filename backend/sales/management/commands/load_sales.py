
import os
import csv
from django.core.management import BaseCommand
from shops.v1.models import Shop
from categories.v1.models import Product
from sales.v1.models import Sales

class Command(BaseCommand):
    """Добавляет данные из data/st_df.csv в базу данных."""
    help = "python manage.py load_all_data"
    
    def handle(self, *args, **options):
        path_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname( __file__ )))), 'data/sales_df_train.csv')
        if Product.objects.exists():
            print('Данные для магизинов уже загружены')
            return
        print("Загрузка данных")
        with open(path_file, encoding='utf-8') as file:
            csvfilereader = csv.reader(file, delimiter=",")
            next(csvfilereader)
            for row in csvfilereader:
                shop = Shop.objects.get(shop=row[0])
                product = Product.objects.get(product=row[1])
                Sales.objects.get_or_create(shop=shop, product=product, 
                                            date=row[2],  
                                            sales_type_id=row[3], 
                                            sales_in_units=row[4],
                                            promo_sales_in_units=row[5],
                                            sales_in_rub=row[6],
                                            promo_sales_in_rub=row[7])


