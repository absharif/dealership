from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


class ProductCategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'bin')


class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'intake', 'damaged', 'stock', 'trade_price', 'bin')


class ProductTransactionAdmin(ImportExportModelAdmin):
    list_display = ('product', 'stock')


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductTransaction, ProductTransactionAdmin)
