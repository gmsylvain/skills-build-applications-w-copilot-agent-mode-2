from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, FitnessGoal


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(source='user.id', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'user_id', 'bio', 'birth_date', 'fitness_level', 
            'height', 'weight', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FitnessGoalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(source='user.id', read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = FitnessGoal
        fields = [
            'id', 'user', 'user_id', 'goal_type', 'target_value', 'current_value',
            'target_date', 'is_achieved', 'progress_percentage', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']