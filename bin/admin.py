from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.


class BINAdmin(ImportExportModelAdmin):
    list_display = ('name', 'address', 'type')


admin.site.register(BIN, BINAdmin)
