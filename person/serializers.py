from rest_framework import serializers
from .models import Transaction, Category, Profile, Budget
from django.contrib.auth.models import User
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
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'profile']
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
            raise serializers.ValidationError({"amount": "Amount must be greater than 0"})
        if type == 'expense' and amount > profile.balance:
            raise serializers.ValidationError({"amount": "Insufficient balance"})
        return attrs
class BudgetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        write_only=True, 
        source='category'
    )
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Budget
        fields = ['id', 'amount', 'category', 'category_id', 'profile']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError({"amount": "Amount must be greater than 0"})
        return value

    def create(self, validated_data):
        profile = validated_data['profile']
        category = validated_data['category']
        amount = validated_data['amount']
        budget, created = Budget.objects.get_or_create(
            profile=profile, 
            category=category,
            defaults={'amount': amount}
        )

        if not created:
            budget.amount += amount
            budget.save()
        
        return budget
    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()
        return instance