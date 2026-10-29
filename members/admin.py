from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_number', 'first_name', 'last_name', 'id_number', 'phone_number', 'status', 'date_joined')
    search_fields = ('member_number', 'first_name', 'last_name', 'id_number', 'phone_number')
    list_filter = ('status', 'date_joined')