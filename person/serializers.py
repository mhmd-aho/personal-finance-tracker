from rest_framework import serializers
from .models import Transaction, Category, Profile
from django.contrib.auth.models import User
from django.db import transaction
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'balance', 'user', 'user_id']
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
class TransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True,source='category')
    profile = ProfileSerializer(read_only=True)
    profile_id = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True,source='profile')
    class Meta:
        model = Transaction
        read_only_fields = ['created_at']
        fields = ['id','amount', 'type', 'created_at', 'category', 'category_id', 'profile', 'profile_id']

    def validate(self, attrs):
        profile = attrs['profile']
        amount = attrs['amount']
        category = attrs['category']
        type = attrs['type']
        if amount <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        if type == 'expense' and amount > profile.balance:
            raise serializers.ValidationError("Insufficient balance")
        return attrs
    def create(self, validated_data):
        with transaction.atomic():
            profile = validated_data['profile']
            amount = validated_data['amount']
            type = validated_data['type']
            if type == 'expense':
                profile.balance -= amount
            else:
                profile.balance += amount
            profile.save()
        return super().create(validated_data)