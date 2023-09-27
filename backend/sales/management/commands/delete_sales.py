from django.core.management import BaseCommand
from sales.v1.models import Sales


class Command(BaseCommand):
    """Удаляет все продажи из базы данных."""
    help = "python manage.py delete_sales"

    def handle(self, *args, **options):
        print("Delete shops data")
        Sales.objects.all().delete()
