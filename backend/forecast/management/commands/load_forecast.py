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
        
        logging.info('Загрузка данных прогноза') 
        self._load_data_from_csv(path_file) 
        logging.info('Загрузка завершена успешно') 

    def _get_path_to_csv_file(self) -> Path: 
        return Path(__file__).parents[3] / 'data' / 'sales_submission_test.csv' 

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
            forecast_date = row[3]
            target_value = row[4]
            
            # Создание или обновление записи в базе данных
            forecast, created = Forecast.objects.get_or_create(
                store=shop, 
                product=product, 
                forecast_date=forecast_date, 
                defaults={'forecast': {'target': target_value}}
            )
            
            # Если запись уже существует, обновляем её значение
            if not created:
                forecast.forecast = {'target': target_value}
                forecast.save()
                
        except ObjectDoesNotExist as e: 
            logging.error(f'Error while processing row {row}. Error: {str(e)}')
