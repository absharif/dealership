from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


class EmployeePositionAdmin(ImportExportModelAdmin):
    list_display = ('name', 'bin')


class HumanResourceAdmin(ImportExportModelAdmin):
    list_display = ('name', 'position', 'phone', 'bin')


admin.site.register(EmployeePosition, EmployeePositionAdmin)
admin.site.register(HumanResource, HumanResourceAdmin)
