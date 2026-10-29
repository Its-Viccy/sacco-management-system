from django.db.models.signals import post_save
from django.dispatch import receiver
from members.models import Member
from .models import SavingsAccount

@receiver(post_save, sender=Member)
def create_member_savings_account(sender, instance, created, **kwargs):
    if created:
        account_num = f"SAV-{instance.member_number}"
        SavingsAccount.objects.create(
            member=instance,
            account_number=account_num,
            balance=0.00
        )