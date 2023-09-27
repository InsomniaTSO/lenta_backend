from django.core.management import BaseCommand
from categories.v1.models import Group, Category, Subcategory, Product


class Command(BaseCommand):
    """Удаляет все товары из базы данных."""
    help = "python manage.py delete_cat"

    def handle(self, *args, **options):
        print("Delete shops data")
        Group.objects.all().delete()
        Category.objects.all().delete()
        Subcategory.objects.all().delete()
        Product.objects.all().delete()
