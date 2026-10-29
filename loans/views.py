from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from decimal import Decimal, InvalidOperation
import uuid
from members.models import Member
from .models import Loan, LoanRepayment

def loan_list(request):
    loans = Loan.objects.all().order_by('-application_date')
    return render(request, 'loans/loan_list.html', {'loans': loans})

def loan_detail(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    repayments = loan.repayments.all().order_by('-date')
    return render(request, 'loans/loan_detail.html', {'loan': loan, 'repayments': repayments})

def apply_loan(request):
    members = Member.objects.filter(status='active')
    
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        raw_principal = request.POST.get('principal_amount', '0')
        raw_interest = request.POST.get('interest_rate', '12.0')
        duration_months = int(request.POST.get('duration_months', 12))

        member = get_object_or_404(Member, id=member_id)

        try:
            principal = Decimal(raw_principal)
            interest_rate = Decimal(raw_interest)
        except InvalidOperation:
            messages.error(request, "Invalid numeric input for loan amount or interest rate.")
            return redirect('apply_loan')

        loan_num = f"LN-{uuid.uuid4().hex[:8].upper()}"

        Loan.objects.create(
            member=member,
            loan_number=loan_num,
            principal_amount=principal,
            interest_rate=interest_rate,
            duration_months=duration_months,
            status='pending'
        )

        messages.success(request, f"Loan application submitted successfully for {member.first_name}. Ref: {loan_num}")
        return redirect('loan_list')

    return render(request, 'loans/apply_loan.html', {'members': members})

def make_repayment(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)

    if request.method == 'POST':
        raw_amount = request.POST.get('amount', '0')
        payment_method = request.POST.get('payment_method', 'mpesa')
        remarks = request.POST.get('remarks', '')

        try:
            amount = Decimal(raw_amount)
        except InvalidOperation:
            messages.error(request, "Invalid repayment amount entered.")
            return redirect('make_repayment', loan_id=loan.id)

        if amount <= 0:
            messages.error(request, "Repayment amount must be greater than zero.")
            return redirect('make_repayment', loan_id=loan.id)

        if amount > loan.balance:
            messages.error(request, f"Repayment exceeds outstanding balance of KES {loan.balance:,.2f}.")
            return redirect('make_repayment', loan_id=loan.id)

        ref_num = f"PAY-{uuid.uuid4().hex[:8].upper()}"

        with transaction.atomic():
            loan.balance -= amount
            if loan.balance == Decimal('0.00'):
                loan.status = 'cleared'
            loan.save()

            LoanRepayment.objects.create(
                loan=loan,
                amount=amount,
                reference_number=ref_num,
                payment_method=payment_method,
                remarks=remarks
            )

        messages.success(request, f"Repayment of KES {amount:,.2f} recorded! Outstanding Balance: KES {loan.balance:,.2f}")
        return redirect('loan_detail', loan_id=loan.id)

    return render(request, 'loans/repayment.html', {'loan': loan})