from django.contrib import admin
from .models import SavingsAccount, SavingsTransaction

@admin.register(SavingsAccount)
class SavingsAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'member', 'balance', 'created_at')
    search_fields = ('account_number', 'member__first_name', 'member__last_name', 'member__member_number')
    readonly_fields = ('balance',)

@admin.register(SavingsTransaction)
class SavingsTransactionAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'savings_account', 'transaction_type', 'amount', 'payment_method', 'date')
    list_filter = ('transaction_type', 'payment_method', 'date')
    search_fields = ('reference_number', 'savings_account__account_number', 'savings_account__member__first_name')