from django.core.management import BaseCommand
from categories.v1.models import Group, Category, Subcategory, Product
import logging

logging.basicConfig(level=logging.INFO)

class Command(BaseCommand):
    """Удаляет все товары из базы данных."""
    help = "python manage.py delete_cat"

    def handle(self, *args, **options):
        logging.info('Данные товарной иерархии удалены')
        Group.objects.all().delete()
        Category.objects.all().delete()
        Subcategory.objects.all().delete()
        Product.objects.all().delete()
