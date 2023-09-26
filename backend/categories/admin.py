from django.contrib import admin
from .models import Group, Category, Subcategory, Product

admin.site.register(Group)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
