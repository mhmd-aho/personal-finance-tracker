from django.urls import path,include
from rest_framework import routers
from .views import (
    TransactionListCreateView,
    TransactionRetrieveUpdateDestroyView,
    CategoryViewSet,
    ProfileViewSet,
    BudgetViewSet,
    MonthlyTransactionListView,
    LastTenDaysTransactionListView,
)
router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'budgets', BudgetViewSet, basename='budget')

urlpatterns = [
    path('',include(router.urls)),
    path('transactions/profile/<str:profile_id>/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>',TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-detail'),
    path('transactions/profile/<int:profile_id>/monthly/', MonthlyTransactionListView.as_view(), name='transaction-monthly'),
    path('transactions/profile/<int:profile_id>/last-ten-days/', LastTenDaysTransactionListView.as_view(), name='transaction-ten-days'),
]