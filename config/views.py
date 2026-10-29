from django.shortcuts import render
from django.db.models import Sum
from members.models import Member
from savings.models import SavingsAccount, SavingsTransaction
from loans.models import Loan

def dashboard(request):
    total_members = Member.objects.filter(status='active').count()
    total_savings = SavingsAccount.objects.aggregate(Sum('balance'))['balance__sum'] or 0
    total_loans_disbursed = Loan.objects.aggregate(Sum('principal_amount'))['principal_amount__sum'] or 0
    total_outstanding_loans = Loan.objects.aggregate(Sum('balance'))['balance__sum'] or 0

    recent_transactions = SavingsTransaction.objects.all().order_by('-date')[:5]
    recent_loans = Loan.objects.all().order_by('-application_date')[:5]

    context = {
        'total_members': total_members,
        'total_savings': total_savings,
        'total_loans_disbursed': total_loans_disbursed,
        'total_outstanding_loans': total_outstanding_loans,
        'recent_transactions': recent_transactions,
        'recent_loans': recent_loans,
    }
    return render(request, 'dashboard.html', context)