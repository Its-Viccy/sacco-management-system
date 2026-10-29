from django.db import models
from members.models import Member
from decimal import Decimal

class Loan(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('disbursed', 'Disbursed'),
        ('rejected', 'Rejected'),
        ('cleared', 'Fully Paid'),
    )

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='loans')
    loan_number = models.CharField(max_length=20, unique=True)
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Annual interest rate in %")
    duration_months = models.IntegerField(help_text="Repayment duration in months")
    total_repayment = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    application_date = models.DateTimeField(auto_now_add=True)
    disbursement_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculate simple interest total repayment if new
        if not self.total_repayment or self.total_repayment == Decimal('0.00'):
            interest = self.principal_amount * (self.interest_rate / Decimal('100')) * (Decimal(self.duration_months) / Decimal('12'))
            self.total_repayment = self.principal_amount + interest
            self.balance = self.total_repayment
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan {self.loan_number} - {self.member.first_name} (KES {self.principal_amount})"


class LoanRepayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference_number = models.CharField(max_length=50, unique=True)
    payment_method = models.CharField(max_length=15, default='mpesa')
    date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Repayment {self.reference_number} - KES {self.amount}"