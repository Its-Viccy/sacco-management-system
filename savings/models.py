from django.db import models
from members.models import Member

class SavingsAccount(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='savings_account')
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_number} - {self.member.first_name} {self.member.last_name} (KES {self.balance})"


class SavingsTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    )

    PAYMENT_METHODS = (
        ('mpesa', 'M-Pesa'),
        ('bank', 'Bank Transfer'),
        ('cash', 'Cash'),
    )

    savings_account = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHODS, default='mpesa')
    reference_number = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type.upper()} - KES {self.amount} ({self.reference_number})"