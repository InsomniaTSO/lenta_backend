from pathlib import Path
import csv
from django.core.management import BaseCommand
from shops.v1.models import Shop
from categories.v1.models import Product
from sales.v1.models import Sales
import logging

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    """Добавляет данные из data/sales_df_train.csv в базу данных."""

    help = "python manage.py load_sales"

    def handle(self, *args, **options):
        path_file = self._get_path_to_csv_file()
        
        if Sales.objects.exists():
            logging.info('Данные для продаж уже загружены')
            return
        
        logging.info('Загрузка данных продаж')
        self._load_data_from_csv(path_file)
        logging.info('Загрузка завершена успешно')

    def _get_path_to_csv_file(self) -> Path:
        return Path(__file__).parents[3] / 'data' / 'sales_df_train.csv'

    def _load_data_from_csv(self, path_file: Path):
        with open(path_file, encoding='utf-8') as file:
            csvfilereader = csv.reader(file, delimiter=",")
            next(csvfilereader)
            for row in csvfilereader:
                self._create_sales_from_row(row)

    def _create_sales_from_row(self, row):
        shop = Shop.objects.get(store=row[0])
        product = Product.objects.get(sku=row[1])
        Sales.objects.get_or_create(
            shop=shop, 
            product=product,
            date=row[2],
            sales_type=row[3],
            sales_units=int(float(row[4])),
            sales_units_promo=int(float(row[5])),
            sales_rub=row[6],
            sales_run_promo=row[7]
        )
