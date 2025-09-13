from django.contrib import admin

from logistic.models import Product, Stock, StockProduct


# Register your models here.

class StockProductInline(admin.StackedInline):
    model = StockProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','description']
    inlines = [StockProductInline]



