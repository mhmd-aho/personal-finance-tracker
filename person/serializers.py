from rest_framework import serializers
from .models import Transaction, Category, Profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'balance']
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
class TransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    profile = ProfileSerializer(read_only=True)
    profile_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Transaction
        fields = ['amount', 'type', 'created_at', 'category', 'category_id', 'profile', 'profile_id']
    def validate(self, attrs):
        profile = attrs['profile']
        amount = attrs['amount']
        type = attrs['type']
        if amount <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        if type == 'expense' and amount > profile.balance:
            raise serializers.ValidationError("Insufficient balance")
        return attrs