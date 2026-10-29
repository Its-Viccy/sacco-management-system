from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('dormant', 'Dormant'),
        ('suspended', 'Suspended'),
        ('exited', 'Exited'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='member_profile')
    member_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.member_number} - {self.first_name} {self.last_name}"