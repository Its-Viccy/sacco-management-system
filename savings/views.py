from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from decimal import Decimal, InvalidOperation
import uuid
from .models import SavingsAccount, SavingsTransaction

def account_detail(request, account_id):
    account = get_object_or_404(SavingsAccount, id=account_id)
    transactions = account.transactions.all().order_by('-date')
    return render(request, 'savings/account_detail.html', {
        'account': account,
        'transactions': transactions
    })

def deposit_funds(request, account_id):
    account = get_object_or_404(SavingsAccount, id=account_id)
    
    if request.method == 'POST':
        raw_amount = request.POST.get('amount', '0')
        payment_method = request.POST.get('payment_method', 'mpesa')
        description = request.POST.get('description', '')

        try:
            amount = Decimal(raw_amount)
        except InvalidOperation:
            messages.error(request, "Invalid amount entered.")
            return redirect('deposit_funds', account_id=account.id)

        if amount <= 0:
            messages.error(request, "Deposit amount must be greater than zero.")
            return redirect('deposit_funds', account_id=account.id)

        ref_num = f"DEP-{uuid.uuid4().hex[:8].upper()}"

        with transaction.atomic():
            # Update account balance safely using Decimal
            account.balance += amount
            account.save()

            # Record transaction log
            SavingsTransaction.objects.create(
                savings_account=account,
                transaction_type='deposit',
                amount=amount,
                payment_method=payment_method,
                reference_number=ref_num,
                description=description
            )

        messages.success(request, f"Successfully deposited KES {amount:,.2f}. Ref: {ref_num}")
        return redirect('account_detail', account_id=account.id)

    return render(request, 'savings/deposit.html', {'account': account})

def withdraw_funds(request, account_id):
    account = get_object_or_404(SavingsAccount, id=account_id)
    
    if request.method == 'POST':
        raw_amount = request.POST.get('amount', '0')
        payment_method = request.POST.get('payment_method', 'mpesa')
        description = request.POST.get('description', '')

        try:
            amount = Decimal(raw_amount)
        except InvalidOperation:
            messages.error(request, "Invalid amount entered.")
            return redirect('withdraw_funds', account_id=account.id)

        if amount <= 0:
            messages.error(request, "Withdrawal amount must be greater than zero.")
            return redirect('withdraw_funds', account_id=account.id)

        if amount > account.balance:
            messages.error(request, f"Insufficient balance! Current balance is KES {account.balance:,.2f}.")
            return redirect('withdraw_funds', account_id=account.id)

        ref_num = f"WTH-{uuid.uuid4().hex[:8].upper()}"

        with transaction.atomic():
            # Deduct account balance safely using Decimal
            account.balance -= amount
            account.save()

            # Record transaction log
            SavingsTransaction.objects.create(
                savings_account=account,
                transaction_type='withdrawal',
                amount=amount,
                payment_method=payment_method,
                reference_number=ref_num,
                description=description
            )

        messages.success(request, f"Successfully withdrew KES {amount:,.2f}. Ref: {ref_num}")
        return redirect('account_detail', account_id=account.id)

    return render(request, 'savings/withdraw.html', {'account': account})