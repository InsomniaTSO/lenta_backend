import os
import csv
from django.core.management import BaseCommand
from categories.v1.models import Group, Category, Subcategory, Product
import logging

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    """Добавляет данные из data/st_df.csv в базу данных."""
    help = "python manage.py load_all_data"
    
    def handle(self, *args, **options):
        path_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname( __file__ )))), 'data/pr_df.csv')
        if Product.objects.exists():
            logging.info('Данные товарной иерархии уже загружены')
            return
        logging.info('Загрузка данных товарной иерархии')
        with open(path_file, encoding='utf-8') as file:
            csvfilereader = csv.reader(file, delimiter=",")
            next(csvfilereader)
            for row in csvfilereader:
                sku = row[0]
                group = Group.objects.get_or_create(group_id=row[1])[0]
                category = Category.objects.get_or_create(cat_id=row[2])[0]
                subcategory = Subcategory.objects.get_or_create(subcat_id=row[3])[0]
                uom = int(row[4])
                Product.objects.get_or_create(sku=sku, group=group, 
                                           category=category, 
                                           subcategory=subcategory, 
                                           uom=uom)
        logging.info('Загрузка завершена успешно')
