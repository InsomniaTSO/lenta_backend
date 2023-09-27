
import os
from pathlib import Path
import csv
from django.core.management import BaseCommand
from shops.v1.models import City, Division, Format, Location, Shop, Size

class Command(BaseCommand):
    """Добавляет данные из data/st_df.csv в базу данных."""
    help = "python manage.py load_all_data"
    
    def handle(self, *args, **options):
        path_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname( __file__ )))), 'data/st_df.csv')
        if Shop.objects.exists():
            print('Данные для магизинов уже загружены')
            return
        print("Загрузка данных")
        with open(path_file, encoding='utf-8') as file:
            csvfilereader = csv.reader(file, delimiter=",")
            next(csvfilereader)
            for row in csvfilereader:
                shop_id = row[0]
                city = City.objects.get_or_create(city_id=row[1])[0]
                division = Division.objects.get_or_create(division_code_id=row[2])[0]
                format = Format.objects.get_or_create(type_format_id=int(row[3]))[0]
                location = Location.objects.get_or_create(type_loc_id=int(row[4]))[0]
                size = Size.objects.get_or_create(type_size_id=int(row[5]))[0]
                is_active = int(row[6])
                Shop.objects.get_or_create(shop_id=shop_id, city=city, 
                                           division_code=division, 
                                           type_format=format, 
                                           type_loc_id=location, 
                                           type_size_id=size, 
                                           is_active=is_active)
