import csv
import logging
from pathlib import Path
import pandas as pd
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

        if Product.objects.exists():
            logging.info('Данные прогноза уже загружены')
            return 
             
        logging.info('Загрузка данных прогноза') 
        self._load_data_from_csv(path_file) 
        logging.info('Загрузка завершена успешно') 

    def _get_path_to_csv_file(self) -> Path: 
        return Path(__file__).parents[3] / 'data' / 'sales_submission_test.csv' 

    def _load_data_from_csv(self, path_file: Path): 
        df = pd.read_csv(path_file)
        df = df.sort_values(by=["st_id", "pr_sku_id", "date"])
        df = df.reset_index()
        prev_st = ""
        prev_sku = ""
        forecast_d = dict()
        for index, row in df.iterrows():
            try:
                shop = Shop.objects.get(store=row["st_id"]) 
                product = Product.objects.get(sku=row["pr_sku_id"]) 
                forecast_date = row["date"]
                target_value = row["target"]
                if ((row["st_id"] == prev_st or prev_st == "") and 
                    (row["pr_sku_id"] == prev_sku or prev_sku == "")):
                    forecast_d[forecast_date] = target_value
                else:
                    if Forecast.objects.filter(
                        store=shop, 
                        product=product, 
                        forecast_date=forecast_date
                    ).exists:
                        Forecast.objects.filter(
                        store=shop, 
                        product=product, 
                        forecast_date=forecast_date
                    ).update(
                        store=shop, 
                        product=product, 
                        forecast_date=forecast_date, 
                        forecast=forecast_d)
                    else:
                        Forecast.objects.create(
                        store=shop, 
                        product=product, 
                        forecast_date=forecast_date, 
                        forecast=forecast_d)
                    forecast_d = dict()
                    forecast_d[forecast_date] = target_value
                prev_st = row["st_id"]  
                prev_sku = row["pr_sku_id"]
            except ObjectDoesNotExist as e: 
                logging.error(f'Error while processing row {row}. Error: {str(e)}')