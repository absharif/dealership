from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


class ChartOfAccountAdmin(ImportExportModelAdmin):
    list_display = ('name', 'chart_type', 'balance')


class LedgerPostingAdmin(ImportExportModelAdmin):
    list_display = ('date', 'narration', 'ledger', 'particular', 'debit_amount', 'credit_amount', 'balance')


admin.site.register(ChartOfAccount, ChartOfAccountAdmin)
admin.site.register(LedgerPosting, LedgerPostingAdmin)

