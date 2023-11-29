import csv
import logging
from pathlib import Path

from django.core.management import BaseCommand

from categories.models import Product
from sales.models import Sales
from shops.models import Shop

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    """Добавляет данные продаж в базу данных."""

    help = "python manage.py load_sales"

    def _get_path_to_csv_file(self, file_name: str) -> Path:
        return Path(__file__).parents[3] / "data" / file_name

    def _load_data_from_csv(self, path_file: Path):
        with open(path_file, encoding="utf-8") as file:
            csvfilereader = csv.reader(file, delimiter=",")
            next(csvfilereader)
            for row in csvfilereader:
                try:
                    self._create_sales_from_row(row)
                except Exception as err:
                    logging.info(f"Строка не загружена {err=}, {type(err)=}")

    def _create_sales_from_row(self, row):
        shop = Shop.objects.get_or_create(store=row[1])[0]
        product = Product.objects.get_or_create(sku=row[2])[0]
        Sales.objects.get_or_create(
            shop=shop,
            product=product,
            date=row[3],
            sales_type=row[4],
            sales_units=int(float(row[5])),
            sales_units_promo=int(float(row[6])),
            sales_rub=row[7],
            sales_run_promo=row[8],
        )

    def add_arguments(self, parser):
        parser.add_argument(
            "file_name",
            nargs="?",
            type=str,
            help="Name of csv file",
            default="sales_df_train.csv",
        )

    def handle(self, *args, **options):
        file_name = options['file_name']
        path_file = self._get_path_to_csv_file(file_name)
        logging.info("Загрузка данных продаж")
        self._load_data_from_csv(path_file)
        logging.info("Загрузка данных продаж: успешно")
