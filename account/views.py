from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.db.models import Sum
from datetime import datetime, date
from calendar import monthrange
from bin.models import BIN
from django.shortcuts import redirect

# Create your views here.


def school_info(request):
    pass


@login_required
def accounting_reports(request):
    return render(request, "account/accounting_reports.html")


def month_name_from_number(number):
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
             'November', 'December']
    return month[int(number)-1]


@login_required
def add_expense(request):
    submitted = False
    info = {}
    data = {}
    if request.method == 'POST':
        form = ExpanseForm(data=request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            ledger_to = form.cleaned_data['ledger_to']
            ledger_from = form.cleaned_data['ledger_from']
            narration = form.cleaned_data['narration']
            voucher = form.cleaned_data['voucher']
            amount = form.cleaned_data['amount']
            source_doc = form.cleaned_data['source_doc']
            try:
                bin = BIN.objects.get(id=request.session['bin'])
            except BIN.DoesNotExist:
                bin = None

            ledger_to_obj = LedgerPosting()
            ledger_from_obj = LedgerPosting()

            ledger_to_obj.date = date
            ledger_to_obj.voucher = voucher
            ledger_to_obj.particular = 'From ' + str(ledger_from)
            ledger_to_obj.narration = narration
            ledger_to_obj.source_doc = source_doc
            ledger_to_obj.ledger = ledger_to
            ledger_to_obj.debit_amount = amount
            ledger_to_obj.bin = bin

            ledger_from_obj.date = date
            ledger_from_obj.voucher = voucher
            ledger_from_obj.particular = 'To ' + str(ledger_to)
            ledger_from_obj.narration = narration
            ledger_from_obj.source_doc = source_doc
            ledger_from_obj.ledger = ledger_from
            ledger_from_obj.credit_amount = amount
            ledger_from_obj.bin = bin

            ledger_to_obj.save()
            ledger_from_obj.save()

            form = ExpanseForm()
    else:
        form = ExpanseForm()
    return render(request, "account/add_expense.html",
                  {'form': form, 'submitted': submitted, 'data': data, 'info': info})


@login_required
def add_income(request):
    submitted = False
    info = {}
    data = {}
    if request.method == 'POST':
        form = IncomeForm(data=request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            ledger_to = form.cleaned_data['ledger_to']
            ledger_from = form.cleaned_data['ledger_from']
            narration = form.cleaned_data['narration']
            voucher = form.cleaned_data['voucher']
            amount = form.cleaned_data['amount']
            source_doc = form.cleaned_data['source_doc']
            try:
                bin = BIN.objects.get(id=request.session['bin'])
            except BIN.DoesNotExist:
                bin = None

            ledger_to_obj = LedgerPosting()
            ledger_from_obj = LedgerPosting()

            ledger_to_obj.date = date
            ledger_to_obj.voucher = voucher
            ledger_to_obj.particular = 'From ' + str(ledger_from)
            ledger_to_obj.narration = narration
            ledger_to_obj.source_doc = source_doc
            ledger_to_obj.ledger = ledger_to
            ledger_to_obj.debit_amount = amount
            ledger_to_obj.bin = bin

            ledger_from_obj.date = date
            ledger_from_obj.voucher = voucher
            ledger_from_obj.particular = 'To ' + str(ledger_to)
            ledger_from_obj.narration = narration
            ledger_from_obj.source_doc = source_doc
            ledger_from_obj.ledger = ledger_from
            ledger_from_obj.credit_amount = amount
            ledger_from_obj.bin = bin

            ledger_to_obj.save()
            ledger_from_obj.save()

            form = IncomeForm()
    else:
        form = IncomeForm()
    return render(request, "account/add_income.html",
                  {'form': form, 'submitted': submitted, 'data': data, 'info': info})


@login_required
def double_entry(request):
    submitted = False
    info = {}
    data = {}
    if request.method == 'POST':
        form = DoubleEntryForm(request=request, data=request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            ledger_to = form.cleaned_data['ledger_to']
            ledger_from = form.cleaned_data['ledger_from']
            narration = form.cleaned_data['narration']
            voucher = form.cleaned_data['voucher']
            amount = form.cleaned_data['amount']
            source_doc = form.cleaned_data['source_doc']
            try:
                bin = BIN.objects.get(id=request.session['bin'])
            except BIN.DoesNotExist:
                bin = None

            ledger_to_obj = LedgerPosting()
            ledger_from_obj = LedgerPosting()

            ledger_to_obj.date = date
            ledger_to_obj.voucher = voucher
            ledger_to_obj.particular = 'From ' + str(ledger_from)
            ledger_to_obj.narration = narration
            ledger_to_obj.source_doc = source_doc
            ledger_to_obj.ledger = ledger_to
            ledger_to_obj.debit_amount = amount
            ledger_to_obj.bin = bin

            ledger_from_obj.date = date
            ledger_from_obj.voucher = voucher
            ledger_from_obj.particular = 'To ' + str(ledger_to)
            ledger_from_obj.narration = narration
            ledger_from_obj.source_doc = source_doc
            ledger_from_obj.ledger = ledger_from
            ledger_from_obj.credit_amount = amount
            ledger_from_obj.bin = bin

            ledger_to_obj.save()
            ledger_from_obj.save()

            form = DoubleEntryForm(request=request)
    else:
        form = DoubleEntryForm(request=request)
    return render(request, "account/double_entry.html",
                  {'form': form, 'submitted': submitted, 'data': data, 'info': info})


@login_required
def trial_balance(request):
    submitted = False
    info = {}
    data = {}
    if request.method == 'POST':
        form = DateRangeForm(data=request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            trx_query = LedgerPosting.objects.filter(date__range=[start_date, end_date])

            assets = ChartOfAccount.objects.filter(chart_type='asset')
            liability = ChartOfAccount.objects.filter(chart_type='liability')
            equity = ChartOfAccount.objects.filter(chart_type='equity')
            revenue = ChartOfAccount.objects.filter(chart_type='revenue')
            expense = ChartOfAccount.objects.filter(chart_type='expense')

            all_accounts = [assets, liability, equity, revenue, expense]

            info['total_debit'] = 0
            info['total_credit'] = 0
            for accounts in all_accounts:
                for account in accounts:
                    total = trx_query.filter(ledger=account).aggregate(Sum('debit_amount'), Sum('credit_amount'))
                    if total['debit_amount__sum'] or total['credit_amount__sum']:
                        info['total_debit'] += total['debit_amount__sum']
                        info['total_credit'] += total['credit_amount__sum']
                        data[account] = total

        submitted = True
        form = DateRangeForm()
    else:
        form = DateRangeForm()
    return render(request, "account/trial_balance.html",
                  {'form': form, 'submitted': submitted, 'data': data, 'info': info})


@login_required
def balance_sheet(request):
    info = {}
    data = {}

    assets = ChartOfAccount.objects.filter(chart_type='asset')
    liabilities = ChartOfAccount.objects.filter(chart_type='liability')
    equities = ChartOfAccount.objects.filter(chart_type='equity')

    data['Assets'] = assets
    data['Liabilities'] = liabilities
    data['Equities'] = equities
    info['Assets'] = assets.aggregate(Sum('balance'))['balance__sum']
    info['Liabilities'] = liabilities.aggregate(Sum('balance'))['balance__sum']
    info['Equities'] = equities.aggregate(Sum('balance'))['balance__sum']

    return render(request, "account/balance_sheet.html", {'data': data, 'info': info})


@login_required
def income_statement(request):
    submitted = False
    info = {}
    data = {}
    if request.method == 'POST':
        form = DateRangeForm(data=request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            trx_query = LedgerPosting.objects.filter(date__range=[start_date, end_date])
            revenue = ChartOfAccount.objects.filter(chart_type='revenue')
            expense = ChartOfAccount.objects.filter(chart_type='expense')

            revenue_data = {}
            info['total_revenue_debit'] = 0
            info['total_revenue_credit'] = 0
            for account in revenue:
                total = trx_query.filter(ledger=account).aggregate(Sum('debit_amount'), Sum('credit_amount'))
                if total['debit_amount__sum'] or total['credit_amount__sum']:
                    info['total_revenue_debit'] += total['debit_amount__sum']
                    info['total_revenue_credit'] += total['credit_amount__sum']
                    revenue_data[account] = total

            expense_data = {}
            info['total_expense_debit'] = 0
            info['total_expense_credit'] = 0
            for account in expense:
                total = trx_query.filter(ledger=account).aggregate(Sum('debit_amount'), Sum('credit_amount'))
                if total['debit_amount__sum'] or total['credit_amount__sum']:
                    info['total_expense_debit'] += total['debit_amount__sum']
                    info['total_expense_credit'] += total['credit_amount__sum']
                    expense_data[account] = total

            data['Expence'] = expense_data
            data['Revenue'] = revenue_data
            info['total_profit'] = info['total_revenue_credit'] - info['total_expense_debit']
        submitted = True
        form = DateRangeForm()
    else:
        form = DateRangeForm()
    return render(request, "account/income_statement.html",
                  {'form': form, 'submitted': submitted, 'data': data, 'info': info})


@login_required
def cash_flow_statement(request):
    submitted = False
    info = {}
    data = {}

    if request.method == 'POST':
        form = YearForm(data=request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            info['school'] = school_info()

            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                      'November', 'December']

            counter = 0
            total_inflow = 0
            total_outflow = 0
            total_net_flow = 0
            for month in months:
                counter += 1
                number_of_days_in_month = monthrange(int(year.name), counter)[1]
                start_date = date.today().replace(year=int(year.name), month=counter, day=1)
                end_date = date.today().replace(year=int(year.name), month=counter, day=number_of_days_in_month)
                inflow = find_income(start_date, end_date)
                total_inflow += inflow
                outflow = find_expense(start_date, end_date)
                total_outflow += outflow
                net_flow = inflow - outflow
                total_net_flow += net_flow
                data[month] = {'inflow': inflow, 'outflow': outflow, 'net_flow': net_flow}
            info['total_inflow'] = total_inflow
            info['total_outflow'] = total_outflow
            info['total_net_flow'] = total_net_flow

            submitted = True
            form = YearForm()
    else:
        form = YearForm()
    return render(request, "account/cash_flow_statement.html",
                  {'form': form, 'submitted': submitted, 'data': data, 'info': info})


def find_income(start_date, end_date):
    trx_query = LedgerPosting.objects.filter(date__range=[start_date, end_date])
    revenue = ChartOfAccount.objects.filter(chart_type='revenue')

    total = 0
    for account in revenue:
        total_dict = trx_query.filter(ledger=account).aggregate(Sum('credit_amount'))
        if total_dict['credit_amount__sum']:
            total += total_dict['credit_amount__sum']
    return total


def find_expense(start_date, end_date):
    trx_query = LedgerPosting.objects.filter(date__range=[start_date, end_date])
    revenue = ChartOfAccount.objects.filter(chart_type='expense')

    total = 0
    for account in revenue:
        total_dict = trx_query.filter(ledger=account).aggregate(Sum('debit_amount'))
        if total_dict['debit_amount__sum']:
            total += total_dict['debit_amount__sum']
    return total


@login_required
def cash_summary(request):
    submitted = False
    info = {}
    data = {}
    if request.method == 'POST':
        form = DateRangeForm(data=request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            info['start_date'] = start_date
            info['end_date'] = end_date

            trx_query = LedgerPosting.objects.filter(date__range=[start_date, end_date])
            revenue = ChartOfAccount.objects.filter(chart_type='revenue')
            expense = ChartOfAccount.objects.filter(chart_type='expense')

            revenue_data = {}
            info['total_revenue_debit'] = 0
            info['total_revenue_credit'] = 0
            for account in revenue:
                total = trx_query.filter(ledger=account).aggregate(Sum('debit_amount'), Sum('credit_amount'))
                if total['debit_amount__sum'] or total['credit_amount__sum']:
                    info['total_revenue_debit'] += total['debit_amount__sum']
                    info['total_revenue_credit'] += total['credit_amount__sum']
                    revenue_data[account] = total

            expense_data = {}
            info['total_expense_debit'] = 0
            info['total_expense_credit'] = 0
            for account in expense:
                total = trx_query.filter(ledger=account).aggregate(Sum('debit_amount'), Sum('credit_amount'))
                if total['debit_amount__sum'] or total['credit_amount__sum']:
                    info['total_expense_debit'] += total['debit_amount__sum']
                    info['total_expense_credit'] += total['credit_amount__sum']
                    expense_data[account] = total

            data['Expence'] = expense_data
            data['Revenue'] = revenue_data
            info['total_profit'] = info['total_revenue_credit'] - info['total_expense_debit']
        submitted = True
        form = DateRangeForm()
    else:
        form = DateRangeForm()
    return render(request, "account/cash_summary.html",
                  {'form': form, 'submitted': submitted, 'data': data, 'info': info})


@login_required
def account_statement_book(request):
    submitted = False
    info = {}
    data = {}
    if request.method == 'POST':
        form = DateRangeForm(data=request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            trx_query = LedgerPosting.objects.filter(date__range=[start_date, end_date])
            all_account = ChartOfAccount.objects.all()
            for account in all_account:
                data[account] = trx_query.filter(ledger=account)

        submitted = True
        form = DateRangeForm()
    else:
        form = DateRangeForm()
    return render(request, "account/account_statement_book.html",
                  {'form': form, 'submitted': submitted, 'data': data, 'info': info})


@login_required
def ledger_summary(request):
    submitted = False
    info = {}
    data = {}
    if request.method == 'POST':
        form = DateRangeForm(data=request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            trx_query = LedgerPosting.objects.filter(date__range=[start_date, end_date])
            all_account = ChartOfAccount.objects.all().order_by('chart_type')
            for account in all_account:
                temp = trx_query.filter(ledger=account).aggregate(Sum('debit_amount'), Sum('credit_amount'))
                data[account] = {'debit': temp['debit_amount__sum'], 'credit': temp['credit_amount__sum']}

        submitted = True
        form = DateRangeForm()
    else:
        form = DateRangeForm()
    return render(request, "account/ledger_summary.html",
                  {'form': form, 'submitted': submitted, 'data': data, 'info': info})


@login_required
def cash_and_bank_book(request):
    submitted = False
    info = {}
    data = {}
    if request.method == 'POST':
        form = DateRangeForm(data=request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            trx_query = LedgerPosting.objects.filter(date__range=[start_date, end_date])
            all_account = ChartOfAccount.objects.filter(is_cash=True)
            for account in all_account:
                data[account] = trx_query.filter(ledger=account)

        submitted = True
        form = DateRangeForm()
    else:
        form = DateRangeForm()
    return render(request, "account/cash_and_bank_book.html",
                  {'form': form, 'submitted': submitted, 'data': data, 'info': info})

#
# @login_required
# def payments(request):
#     info = {}
#     try:
#         bin = BIN.objects.get(id=request.session['bin'])
#     except BIN.DoesNotExist:
#         bin = None
#
#     start_date = datetime.today()
#     end_date = datetime.today()
#     try:
#         payment_list = Payment.objects.filter(bin=bin)
#     except Payment.DoesNotExist():
#         payment_list = None
#
#     if request.method == 'POST':
#         submitted = True
#         form = PaymentFilterForm(data=request.POST)
#         if form.is_valid():
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']
#             token = form.cleaned_data['token']
#             order = form.cleaned_data['order']
#             type = form.cleaned_data['type']
#             bank_name = form.cleaned_data['bank_name']
#             check_no = form.cleaned_data['check_no']
#             check_date = form.cleaned_data['check_date']
#             check_status = form.cleaned_data['check_status']
#
#             info['type'] = type
#             info['check_status'] = check_status
#
#             if not start_date:
#                 start_date = datetime.today()
#
#             if not end_date:
#                 end_date = datetime.today()
#
#             payment_list = payment_list.filter(date__range=[start_date, end_date])
#
#             if token and payment_list:
#                 payment_list = payment_list.filter(token=token)
#             if order and payment_list:
#                 payment_list = payment_list.filter(order__id=order)
#             if type and payment_list:
#                 payment_list = payment_list.filter(type=type)
#             if bank_name and payment_list:
#                 payment_list = payment_list.filter(bank_name=bank_name)
#             if check_no and payment_list:
#                 payment_list = payment_list.filter(check_no=check_no)
#             if check_date and payment_list:
#                 payment_list = payment_list.filter(check_date=check_date)
#             if check_status and payment_list:
#                 payment_list = payment_list.filter(check_status=check_status)
#     else:
#         payment_list = payment_list.filter(date__range=[start_date, end_date])
#         form = PaymentFilterForm()
#     return render(request, "account/payments.html", {'form': form, 'payments': payment_list, 'info': info})
#
#
# @login_required
# def new_payment(request):
#     try:
#         bin = BIN.objects.get(id=request.session['bin'])
#     except BIN.DoesNotExist:
#         bin = None
#
#     if request.method == 'POST':
#         form = NewPaymentForm(data=request.POST)
#         if form.is_valid():
#             token = form.cleaned_data['token']
#             order = form.cleaned_data['order']
#             type = form.cleaned_data['type']
#             bank_name = form.cleaned_data['bank_name']
#             check_no = form.cleaned_data['check_no']
#             check_date = form.cleaned_data['check_date']
#             check_status = form.cleaned_data['check_status']
#             amount = form.cleaned_data['amount']
#             remark = form.cleaned_data['remark']
#
#             payment = Payment()
#             payment.token = token
#             payment.order = order
#             payment.type = type
#             payment.bank_name = bank_name
#             payment.check_no = check_no
#             payment.check_date = check_date
#             payment.check_status = check_status
#             payment.amount = amount
#             payment.remark = remark
#             payment.date = datetime.today()
#             payment.bin = bin
#             payment.save()
#         return redirect('payments')
#     form = NewPaymentForm()
#     return render(request, "account/new_payment.html", {'form': form})
#
#
# @login_required
# def edit_payment(request, id):
#     try:
#         bin = BIN.objects.get(id=request.session['bin'])
#     except BIN.DoesNotExist:
#         bin = None
#     try:
#         payment = Payment.objects.get(id=id)
#     except Payment.DoesNotExist():
#         payment = None
#
#     if request.method == 'POST':
#         form = NewPaymentForm(request.POST, request.FILES, instance=payment)
#         if form.is_valid():
#             token = form.cleaned_data['token']
#             order = form.cleaned_data['order']
#             type = form.cleaned_data['type']
#             bank_name = form.cleaned_data['bank_name']
#             check_no = form.cleaned_data['check_no']
#             check_date = form.cleaned_data['check_date']
#             check_status = form.cleaned_data['check_status']
#             amount = form.cleaned_data['amount']
#             remark = form.cleaned_data['remark']
#
#             if payment:
#                 payment.token = token
#                 payment.order = order
#                 payment.type = type
#                 payment.bank_name = bank_name
#                 payment.check_no = check_no
#                 payment.check_date = check_date
#                 payment.check_status = check_status
#                 payment.amount = amount
#                 payment.remark = remark
#                 payment.save()
#         return redirect('payments')
#     form = NewPaymentForm(request.POST or None, instance=payment)
#     return render(request, "account/new_payment.html", {'form': form})
