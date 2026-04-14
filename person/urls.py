from django.urls import path
from .views import TransactionListCreateView, CategoryListCreateView, ProfileListCreateView, ProfileRetrieveUpdateDestroyView, MonthlyTransactionListView, LastTenDaysTransactionListView
urlpatterns = [
    path('transactions/<str:profile_id>/', TransactionListCreateView.as_view()),
    path('transactions/<str:profile_id>/monthly/', MonthlyTransactionListView.as_view()),
    path('transactions/<str:profile_id>/last-ten-days/', LastTenDaysTransactionListView.as_view()),
    path('categories/', CategoryListCreateView.as_view()),
    path('profiles/', ProfileListCreateView.as_view()),
    path('profiles/<str:profile_username>/', ProfileRetrieveUpdateDestroyView.as_view()),
]