import os
from pathlib import Path
import csv
from django.core.management import BaseCommand
from shops.v1.models import City, Division, Format, Location, Shop, Size
import logging

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    """Добавляет данные из data/st_df.csv в базу данных."""
    help = "python manage.py load_shops"
    
    def handle(self, *args, **options):
        path_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname( __file__ )))), 'data/st_df.csv')
        if Shop.objects.exists():
            logging.info('Данные для магазинов уже загружены')
            return
        logging.info('Загрузка данных магазинов')
        with open(path_file, encoding='utf-8') as file:
            csvfilereader = csv.reader(file, delimiter=",")
            next(csvfilereader)
            for row in csvfilereader:
                store = row[0]
                city = City.objects.get_or_create(city_id=row[1])[0]
                division = Division.objects.get_or_create(division_code_id=row[2])[0]
                format = Format.objects.get_or_create(type_format_id=int(row[3]))[0]
                location = Location.objects.get_or_create(type_loc_id=int(row[4]))[0]
                size = Size.objects.get_or_create(type_size_id=int(row[5]))[0]
                is_active = int(row[6])
                Shop.objects.get_or_create(store=store, city=city, 
                                           division=division, 
                                           type_format=format, 
                                           loc=location, 
                                           size=size, 
                                           is_active=is_active)
        logging.info('Загрузка завершена успешно')
