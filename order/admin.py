from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


class RouteAdmin(ImportExportModelAdmin):
    list_display = ('name', 'address')


class OrderStatusAdmin(ImportExportModelAdmin):
    list_display = ('name',)


class OrderItemInline(admin.TabularInline):
    model = ItemInOrder


class OrderAdmin(ImportExportModelAdmin):
    list_display = ('id', 'memo_no', 'outlet')
    inlines = [OrderItemInline]


class ItemInOrderAdmin(ImportExportModelAdmin):
    list_display = ('order', 'product', 'quantity')


class AssignDeliveryAdmin(ImportExportModelAdmin):
    list_display = ('order', 'delivery_man')


class OutletAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'address', 'owner_name', 'owner_phone', 'route')


admin.site.register(Route, RouteAdmin)
admin.site.register(Outlet, OutletAdmin)
admin.site.register(OrderStatus, OrderStatusAdmin)
admin.site.register(OrderSetting)
admin.site.register(Order, OrderAdmin)
admin.site.register(ItemInOrder, ItemInOrderAdmin)
