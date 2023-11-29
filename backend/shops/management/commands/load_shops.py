import csv
import logging
from pathlib import Path

from django.core.management import BaseCommand

from shops.models import City, Division, Format, Location, Shop, Size

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    """Добавляет данные по магазинам в базу данных."""

    help = "python manage.py load_shops"

    def _get_path_to_csv_file(self, file_name: str) -> Path:
        return Path(__file__).parents[3] / "data" / file_name

    def _load_shops_from_csv(self, path_file: Path):
        with open(path_file, encoding="utf-8") as file:
            csvfilereader = csv.reader(file, delimiter=",")
            next(csvfilereader)
            for row in csvfilereader:
                try:
                    self._create_shop_from_row(row)
                except Exception as err:
                    logging.info(f"Строка не загружена {err=}, {type(err)=}")

    def _create_shop_from_row(self, row):
        store = row[0]
        city = City.objects.get_or_create(city_id=row[1])[0]
        division = Division.objects.get_or_create(division_code_id=row[2])[0]
        format = Format.objects.get_or_create(type_format_id=int(row[3]))[0]
        location = Location.objects.get_or_create(type_loc_id=int(row[4]))[0]
        size = Size.objects.get_or_create(type_size_id=int(row[5]))[0]
        is_active = int(row[6])
        Shop.objects.get_or_create(
            store=store,
            city=city,
            division=division,
            type_format=format,
            loc=location,
            size=size,
            is_active=is_active,
        )

    def add_arguments(self, parser):
        parser.add_argument(
            "file_name",
            nargs="?",
            type=str,
            help="Name of csv file",
            default="st_df.csv",
        )

    def handle(self, *args, **options):
        file_name = options["file_name"]
        path_file = self._get_path_to_csv_file(file_name)
        logging.info("Загрузка данных магазинов")
        self._load_shops_from_csv(path_file)
        logging.info("Загрузка данных магазинов: успешно")
