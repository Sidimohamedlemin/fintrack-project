from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-income/', views.add_income, name='add_income'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-budget/', views.add_budget, name='add_budget'),
    path('chart-data/', views.chart_data, name='chart_data'),
]
