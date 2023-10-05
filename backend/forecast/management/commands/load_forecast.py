from pathlib import Path
import csv
from django.core.management import BaseCommand
from forecast.v1.models import Forecast
from shops.v1.models import Shop
from categories.v1.models import Product
import logging
from django.core.exceptions import ObjectDoesNotExist

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    """Добавляет данные из data/forecast.csv в базу данных."""
    help = "python manage.py load_forecast"

    def handle(self, *args, **options):
        path_file = self._get_path_to_csv_file()
        
        if Forecast.objects.exists():
            logging.info('Данные для прогноза уже загружены')
            return
        
        logging.info('Загрузка данных прогноза')
        self._load_data_from_csv(path_file)
        logging.info('Загрузка завершена успешно')

    def _get_path_to_csv_file(self) -> Path:
        return Path(__file__).parents[3] / 'data' / 'sales_submission.csv'

    def _load_data_from_csv(self, path_file: Path):
        with open(path_file, encoding='utf-8') as file:
            csvfilereader = csv.reader(file, delimiter=",")
            next(csvfilereader)
            for row in csvfilereader:
                self._create_forecast_from_row(row)

    def _create_forecast_from_row(self, row):
        try:
            shop = Shop.objects.get(store=row[1])
            product = Product.objects.get(sku=row[2])
            Forecast.objects.get_or_create(
                store=shop,
                product=product,
                forecast_date=row[3],
                forecast={'target': row[4]}
            )
        except ObjectDoesNotExist as e:
            logging.error(f'Error while processing row {row}. Error: {str(e)}')


def load_ids_from_csv(file_path, column_name):
    """Загружает уникальные ID из указанной колонки CSV файла."""
    with open(file_path, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return {row[column_name] for row in reader}

def main():
    # Загрузка ID из forecast.csv
    forecast_st_ids = load_ids_from_csv('sales_submission.csv', 'st_id')
    forecast_pr_sku_ids = load_ids_from_csv('sales_submission.csv', 'pr_sku_id')

    # Загрузка ID из других CSV файлов (предполагается, что у вас есть два файла: shops.csv и products.csv)
    other_st_ids = load_ids_from_csv('st_dv.csv', 'st_id')
    other_pr_sku_ids = load_ids_from_csv('pr_df.csv', 'pr_sku_id')

    # Находим отсутствующие ID
    missing_st_ids = forecast_st_ids - other_st_ids
    missing_pr_sku_ids = forecast_pr_sku_ids - other_pr_sku_ids

    # Вывод результатов
    if missing_st_ids:
        print("Отсутствующие st_id из forecast.csv:")
        for id in missing_st_ids:
            print(id)

    if missing_pr_sku_ids:
        print("\nОтсутствующие pr_sku_id из forecast.csv:")
        for id in missing_pr_sku_ids:
            print(id)

if __name__ == "__main__":
    main()