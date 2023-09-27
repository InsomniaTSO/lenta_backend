from django.core.management import BaseCommand
from shops.v1.models import City, Division, Format, Location, Shop, Size


class Command(BaseCommand):
    """Удаляет все ингредиенты из базы данных."""
    help = "python manage.py delete_shops"

    def handle(self, *args, **options):
        print("Delete shops data")
        City.objects.all().delete()
        Division.objects.all().delete()
        Format.objects.all().delete()
        Location.objects.all().delete()
        Shop.objects.all().delete()
        Size.objects.all().delete()
