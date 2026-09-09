from django.urls import path
from .views import expense_list, financial_report, gross_turnover_report, balance_sheet_report, tax_report
from .pdf_reports import report_pdf

urlpatterns=[
    path('', expense_list, name='expense_list'),
    path('laporan/', financial_report, name='financial_report'),
    path('peredaran-bruto/', gross_turnover_report, name='gross_turnover_report'),
    path('neraca/', balance_sheet_report, name='balance_sheet_report'),
    path('pajak/', tax_report, name='tax_report'),
    path('laporan/pdf/', report_pdf, name='report_pdf'),
]
