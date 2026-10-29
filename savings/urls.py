from django.urls import path
from . import views

urlpatterns = [
    path('account/<int:account_id>/', views.account_detail, name='account_detail'),
    path('account/<int:account_id>/deposit/', views.deposit_funds, name='deposit_funds'),
    path('account/<int:account_id>/withdraw/', views.withdraw_funds, name='withdraw_funds'),
]