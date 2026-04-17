from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import Transaction, Category, Profile
from .serializers import TransactionSerializer, CategorySerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
# Create your views here.
class TransactionListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, profile_id):
        transactions = Transaction.objects.filter(profile_id=profile_id,profile__user=request.user)
        transactions_type = request.query_params.get('type')
        if transactions_type:
            transactions = transactions.filter(type=transactions_type)
        transactions_month = request.query_params.get('month')
        if transactions_month:
            transactions = transactions.filter(created_at__month=transactions_month)
        transactions_year = request.query_params.get('year')
        if transactions_year:
            transactions = transactions.filter(created_at__year=transactions_year)
        transactions_range = request.query_params.get('range')
        if transactions_range:
            transactions = transactions.filter(created_at__range=transactions_range)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
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
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        user = self.request.user
        queryset = Transaction.objects.filter(profile_id=profile_id,profile__user=user)
        now = timezone.now()
        transactions_type = self.request.query_params.get('type')
        if transactions_type:
            queryset = queryset.filter(type=transactions_type)
        return queryset.filter(created_at__month=now.month,created_at__year=now.year)
class LastTenDaysTransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        user = self.request.user
        queryset = Transaction.objects.filter(profile_id=profile_id,profile__user=user)
        now = timezone.now()
        return queryset.filter(created_at__range=(now - timedelta(days=10), now))
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
class ProfileListCreateView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
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