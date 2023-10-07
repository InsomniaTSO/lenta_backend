import csv
import logging
from pathlib import Path

from django.core.management import BaseCommand

from categories.v1.models import Category, Group, Product, Subcategory

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    """Добавляет данные из data/st_df.csv в базу данных."""
    
    help = "python manage.py load_all_data"
    
    def handle(self, *args, **options):
        path_file = self._get_path_to_csv_file()
        
        if Product.objects.exists():
            logging.info('Данные товарной иерархии уже загружены')
            return
        
        logging.info('Загрузка данных товарной иерархии')
        self._load_products_from_csv(path_file)
        logging.info('Загрузка завершена успешно')

    def _get_path_to_csv_file(self) -> Path:
        return Path(__file__).parents[3] / 'data' / 'pr_df.csv'

    def _load_products_from_csv(self, path_file: Path):
        with open(path_file, encoding='utf-8') as file:
            csvfilereader = csv.reader(file, delimiter=",")
            next(csvfilereader)
            for row in csvfilereader:
                self._create_product_from_row(row)

    def _create_product_from_row(self, row):
        sku = row[0]
        group = Group.objects.get_or_create(group_id=row[1])[0]
        category = Category.objects.get_or_create(cat_id=row[2])[0]
        subcategory = Subcategory.objects.get_or_create(subcat_id=row[3])[0]
        uom = int(row[4])
        
        Product.objects.get_or_create(
            sku=sku, 
            group=group, 
            category=category, 
            subcategory=subcategory, 
            uom=uom
        )
