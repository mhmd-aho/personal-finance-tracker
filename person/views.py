from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from .models import Transaction, Category, Profile, Budget
from .serializers import TransactionSerializer, CategorySerializer, ProfileSerializer, BudgetSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
# Create your views here.
class TransactionListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        if profile.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, profile_id):
        transaction = Transaction.objects.get(id=profile_id)
        if transaction.profile.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class MonthlyTransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        user = self.request.user
        queryset = Transaction.objects.filter(profile_id=profile_id,profile__user=user)
        now = timezone.now()
        return queryset.filter(created_at__month=now.month,created_at__year=now.year)
class LastTenDaysTransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        user = self.request.user
        queryset = Transaction.objects.filter(profile_id=profile_id,profile__user=user)
        now = timezone.now()
        return queryset.filter(created_at__range=(now - timedelta(days=10), now))
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
class ProfileListCreateView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
class ProfileRetrieveUpdateDestroyView(APIView):
    def get(self, request, profile_username):
        profile = get_object_or_404(Profile, user__username = profile_username)
        if profile.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    def delete(self, request, profile_username):
        profile = Profile.objects.get(user__username = profile_username)
        if profile.user != request.user or not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class BudgetListCreateView(generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Optimized with select_related to avoid N+1 queries
        return Budget.objects.filter(
            profile_id=self.kwargs['profile_id'],
            profile__user=self.request.user
        ).select_related('category', 'profile')

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, id=self.kwargs['profile_id'], user=self.request.user)
        serializer.save(profile=profile)
class BudgetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Budget.objects.filter(profile__user=self.request.user)