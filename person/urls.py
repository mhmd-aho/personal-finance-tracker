from django.urls import path
from .views import TransactionListCreateView, CategoryListCreateView, ProfileListCreateView, ProfileRetrieveUpdateDestroyView
urlpatterns = [
    path('transactions/', TransactionListCreateView.as_view()),
    path('categories/', CategoryListCreateView.as_view()),
    path('profiles/', ProfileListCreateView.as_view()),
    path('profiles/<str:profile_username>/', ProfileRetrieveUpdateDestroyView.as_view()),
]