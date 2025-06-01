from django.urls import path
from . import views
from finance.views import dashboard
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('set_budget/', views.add_budget, name='add_budget'),
    path('chart_data/', views.chart_data, name='chart_data'),
    path('edit_expense/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:pk>/', views.delete_expense, name='delete_expense'),
]
