from rest_framework import generics, viewsets, permissions
from .models import Transaction, Category, Profile, Budget
from .serializers import TransactionSerializer, CategorySerializer, ProfileSerializer, BudgetSerializer
from django.utils import timezone
from datetime import timedelta
from .permissions import IsOwnerProfile, IsProfileOwnerForObject
from django.db.models import Q
# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Category.objects.filter(Q(profile__user=self.request.user)| Q(profile = None))
    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(profile=profile)
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerProfile]
    lookup_field = 'user__username'
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    def perform_update(self, serializer):
        serializer.save()
class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated,IsProfileOwnerForObject]
    lookup_field = 'pk'
    def get_queryset(self):
        return Budget.objects.filter(profile__user=self.request.user).select_related('category','profile')
    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(profile=profile)
class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        return Transaction.objects.filter(profile_id=profile_id, profile__user=self.request.user)
    def perform_create(self, serializer):
        profile = Profile.objects.get(id=self.kwargs['profile_id'], user=self.request.user)
        serializer.save(profile=profile)
class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerForObject]
    
    def get_queryset(self):
        return Transaction.objects.filter(profile__user=self.request.user)
class MonthlyTransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        now = timezone.now()
        return Transaction.objects.filter(
            profile_id=profile_id, 
            profile__user=self.request.user,
            created_at__month=now.month,
            created_at__year=now.year
        )
class LastTenDaysTransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        now = timezone.now()
        return Transaction.objects.filter(
            profile_id=profile_id, 
            profile__user=self.request.user,
            created_at__range=(now - timedelta(days=10), now)
        )