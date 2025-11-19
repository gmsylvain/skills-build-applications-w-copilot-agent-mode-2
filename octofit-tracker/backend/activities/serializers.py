from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ActivityType, Activity, WorkoutPlan, WorkoutExercise
from accounts.serializers import UserSerializer


class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = [
            'id', 'name', 'description', 'category', 'calories_per_minute',
            'points_multiplier', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(source='user.id', read_only=True)
    activity_type = ActivityTypeSerializer(read_only=True)
    activity_type_id = serializers.IntegerField(write_only=True)
    points_earned = serializers.ReadOnlyField()
    
    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'user_id', 'activity_type', 'activity_type_id', 'name',
            'description', 'duration_minutes', 'intensity', 'calories_burned',
            'distance_km', 'notes', 'date_recorded', 'points_earned',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    activity_type = ActivityTypeSerializer(read_only=True)
    activity_type_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = WorkoutExercise
        fields = [
            'id', 'activity_type', 'activity_type_id', 'order', 'sets', 'reps',
            'duration_minutes', 'rest_seconds', 'notes'
        ]
        read_only_fields = ['id']


class WorkoutPlanSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.CharField(source='created_by.id', read_only=True)
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)
    
    class Meta:
        model = WorkoutPlan
        fields = [
            'id', 'name', 'description', 'created_by', 'created_by_id',
            'difficulty_level', 'duration_weeks', 'is_public', 'exercises',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkoutPlanCreateSerializer(serializers.ModelSerializer):
    """Separate serializer for creating workout plans with exercises"""
    exercises = WorkoutExerciseSerializer(many=True, required=False)
    
    class Meta:
        model = WorkoutPlan
        fields = [
            'name', 'description', 'difficulty_level', 'duration_weeks',
            'is_public', 'exercises'
        ]
    
    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises', [])
        workout_plan = WorkoutPlan.objects.create(**validated_data)
        
        for exercise_data in exercises_data:
            WorkoutExercise.objects.create(workout_plan=workout_plan, **exercise_data)
        
        return workout_plan