import csv
import logging
from pathlib import Path
from django.core.management import BaseCommand
from categories.v1.models import Product
from forecast.v1.models import Forecast
from shops.v1.models import Shop


logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    """Добавляет данные из data/forecast.csv в базу данных."""
    help = "python manage.py load_forecast"

    def handle(self, *args, **options):
        path_file = self._get_path_to_csv_file()
        if Forecast.objects.exists():
            logging.info('Данные прогноза уже загружены')
            return 
        logging.info('Загрузка данных прогноза') 
        self._load_data_from_csv(path_file)
        logging.info('Загрузка завершена успешно')

    def _get_path_to_csv_file(self) -> Path:
        return Path(__file__).parents[3] / 'data' / 'lenta_last14_v3.csv'

    def _load_data_from_csv(self, path_file: Path):
        with open(path_file, encoding='utf-8') as file:
            csvfilereader = csv.reader(file, delimiter=",")
            next(csvfilereader)
            for row in csvfilereader:
                try:
                    self._create_forecast_from_row(row)
                except:
                    logging.info("Не удалось загрузить строку.")

    def _create_forecast_from_row(self, row):
        shop = Shop.objects.get(store=row[1])
        product = Product.objects.get(sku=row[2])
        Forecast.objects.get_or_create(
            store=shop,
            product=product,
            forecast_date="2023-07-06",
            date=row[3],
            target=int(row[5])
        )
