from django.contrib import admin

# Register your models here.

from .models import Product, Purchase, Expense, ItemPurchase


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available_quantity', 'description', 'expected_sales')
    search_fields = ('name', 'description')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'amount')

admin.site.register(Purchase)

admin.site.register(ItemPurchase)
