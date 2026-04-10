from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import Transaction, Category, Profile
from .serializers import TransactionSerializer, CategorySerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
# Create your views here.
class TransactionListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, profile_id):
        transactions = Transaction.objects.filter(profile_id=profile_id)
        if transactions.exists() and transactions.first().profile.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
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