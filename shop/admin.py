from django.contrib import admin

# Register your models here.

from .models import Product, Purchase


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'available_quantity')
    list_filter = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('date', 'customer', 'total_amount')
    list_filter = ('customer', 'date')
    search_fields = ('customer', 'date')