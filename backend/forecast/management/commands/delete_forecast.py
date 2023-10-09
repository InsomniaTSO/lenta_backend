import logging

from django.core.management import BaseCommand

from forecast.v1.models import Forecast

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    """Удаляет все товары из базы данных."""
    help = "python manage.py delete_forecast"

    def handle(self, *args, **options):
        Forecast.objects.all().delete()
        logging.info('Данные прогноза удалены')
