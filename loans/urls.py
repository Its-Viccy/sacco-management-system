from django.urls import path
from . import views

urlpatterns = [
    path('', views.loan_list, name='loan_list'),
    path('<int:loan_id>/', views.loan_detail, name='loan_detail'),
    path('apply/', views.apply_loan, name='apply_loan'),
    path('<int:loan_id>/repay/', views.make_repayment, name='make_repayment'),
]