from django.contrib import admin

# Register your models here.

from .models import Product, Purchase

admin.site.register(Product)
admin.site.register(Purchase)