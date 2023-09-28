from django.core.management import BaseCommand
from sales.v1.models import Sales
import logging

logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    """Удаляет все продажи из базы данных."""
    help = "python manage.py delete_sales"

    def handle(self, *args, **options):
        logging.info('Данные для продаж удалены')
        Sales.objects.all().delete()
