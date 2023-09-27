from django.core.management import BaseCommand
from sales.v1.models import Sales


class Command(BaseCommand):
    """Удаляет все ингредиенты из базы данных."""
    help = "python manage.py delete_shops"

    def handle(self, *args, **options):
        print("Delete shops data")
        Sales.objects.all().delete()
