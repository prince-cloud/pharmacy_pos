from django.contrib import admin

# Register your models here.

from .models import Product, Purchase, Expense


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available_quantity', 'description',)
    list_filter = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('date', 'customer', 'total_amount')
    list_filter = ('customer', 'date')
    search_fields = ('customer', 'date')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount')