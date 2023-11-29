import csv
import logging
from pathlib import Path
from django.core.management import BaseCommand
from categories.models import Product
from forecast.models import Forecast
from shops.models import Shop


logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    """Добавляет данные прогнозов в базу данных."""

    help = "python manage.py load_forecast"

    def _get_path_to_csv_file(self, file_name: str) -> Path:
        return Path(__file__).parents[3] / "data" / file_name

    def _load_data_from_csv(self, path_file: Path):
        with open(path_file, encoding="utf-8") as file:
            csvfilereader = csv.reader(file, delimiter=",")
            next(csvfilereader)
            for row in csvfilereader:
                try:
                    self._create_forecast_from_row(row)
                except Exception as err:
                    logging.info(f"Строка не загружена {err=}, {type(err)=}")

    def _create_forecast_from_row(self, row):
        shop = Shop.objects.get_or_create(store=row[1])[0]
        product = Product.objects.get_or_create(sku=row[2])[0]
        Forecast.objects.get_or_create(
            store=shop,
            product=product,
            forecast_date="2023-07-06",
            date=row[3],
            target=int(row[5]),
        )

    def add_arguments(self, parser):
        parser.add_argument(
            "file_name",
            nargs="?",
            type=str,
            help="Name of csv file",
            default="lenta_last14_v3.csv",
        )

    def handle(self, *args, **options):
        file_name = options["file_name"]
        path_file = self._get_path_to_csv_file(file_name)
        logging.info("Загрузка данных прогноза")
        self._load_data_from_csv(path_file)
        logging.info("Загрузка данных прогноза: успешно")
