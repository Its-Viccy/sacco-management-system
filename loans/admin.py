from django.contrib import admin
from .models import Loan, LoanRepayment

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_number', 'member', 'principal_amount', 'interest_rate', 'balance', 'status', 'application_date')
    list_filter = ('status', 'application_date')
    search_fields = ('loan_number', 'member__first_name', 'member__last_name', 'member__id_number')

@admin.register(LoanRepayment)
class LoanRepaymentAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'loan', 'amount', 'payment_method', 'date')
    search_fields = ('reference_number', 'loan__loan_number', 'loan__member__first_name')