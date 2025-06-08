from django.urls import path
from .views import dashboard, add_income, add_expense, add_budget, chart_data, edit_expense, delete_expense
from django.contrib.auth import views 

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', dashboard, name='dashboard'),  # ✅ This makes /finance/ work
    path('dashboard/', dashboard, name='dashboard'),
    path('add_income/', add_income, name='add_income'),
    path('add_expense/', add_expense, name='add_expense'),
    path('set_budget/', add_budget, name='add_budget'),
    path('chart_data/', chart_data, name='chart_data'),
    path('edit_expense/<int:pk>/', edit_expense, name='edit_expense'),
    path('delete_expense/<int:pk>/', delete_expense, name='delete_expense'),
]
