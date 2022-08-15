from django.urls import path
from . import views

urlpatterns = [
    # path('date_wise_transaction/', views.date_wise_transaction, name='date_wise_transaction'),
    #
    # path('class_wise_payment_summary/', views.class_wise_payment_summary, name='class_wise_payment_summary'),
    # path('payment_details_section_wise/', views.payment_details_section_wise, name='payment_details_section_wise'),
    # path('payment_details_student_wise/', views.payment_details_student_wise, name='payment_details_student_wise'),
    # path('payment_information_section_wise/', views.payment_information_section_wise,
    #      name='payment_information_section_wise'),
    # path('payment_information_student_wise/', views.payment_information_student_wise,
    #      name='payment_information_student_wise'),
    # path('monthly_paid_details/', views.monthly_paid_details, name='monthly_paid_details'),
    # path('fee_head_payment_info_summary/', views.fee_head_payment_info_summary, name='fee_head_payment_info_summary'),
    # path('payment_ratio/', views.payment_ratio, name='payment_ratio'),
    # path('fee_head_collection_summary/', views.fee_head_collection_summary, name='fee_head_collection_summary'),
    # path('assigned_fee/', views.assigned_fee, name='assigned_fee'),

    path('payments/', views.payments, name='payments'),
    path('new_payment/', views.new_payment, name='new_payment'),
    path('edit_payment/<int:id>/', views.edit_payment, name='edit_payment'),


    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_income/', views.add_income, name='add_income'),
    path('double_entry/', views.double_entry, name='double_entry'),


    path('trial_balance/', views.trial_balance, name='trial_balance'),
    path('balance_sheet/', views.balance_sheet, name='balance_sheet'),
    path('income_statement/', views.income_statement, name='income_statement'),
    path('cash_flow_statement/', views.cash_flow_statement, name='cash_flow_statement'),
    path('cash_summary/', views.cash_summary, name='cash_summary'),
    path('account_statement_book/', views.account_statement_book, name='account_statement_book'),
    path('cash_and_bank_book/', views.cash_and_bank_book, name='cash_and_bank_book'),
    path('ledger_summary/', views.ledger_summary, name='ledger_summary'),

    # path('fund_transaction_summary/', views.fund_transaction_summary, name='fund_transaction_summary'),
    # path('fund_flow_statement/', views.fund_flow_statement, name='fund_flow_statement'),
    # path('fund_details_list/', views.fund_details_list, name='fund_details_list'),
    # path('monthly_fund_transaction/', views.monthly_fund_transaction, name='monthly_fund_transaction'),

    path('accounting_reports/', views.accounting_reports, name='accounting_reports'),
]
