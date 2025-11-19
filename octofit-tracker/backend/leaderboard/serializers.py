from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    LeaderboardEntry, Achievement, UserAchievement, 
    WeeklyChallenge, ChallengeParticipation
)
from accounts.serializers import UserSerializer


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = LeaderboardEntry
        fields = [
            'id', 'user', 'user_id', 'username', 'total_points', 'total_activities',
            'total_duration_minutes', 'total_calories_burned', 'total_distance_km',
            'current_streak_days', 'longest_streak_days', 'last_activity_date',
            'rank_position', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = [
            'id', 'name', 'description', 'category', 'requirement_type',
            'requirement_value', 'points_reward', 'badge_icon', 'is_active',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserAchievementSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(source='user.id', read_only=True)
    achievement = AchievementSerializer(read_only=True)
    achievement_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UserAchievement
        fields = [
            'id', 'user', 'user_id', 'achievement', 'achievement_id',
            'earned_at', 'is_displayed'
        ]
        read_only_fields = ['id', 'earned_at']


class ChallengeParticipationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(source='user.id', read_only=True)
    challenge_name = serializers.CharField(source='challenge.name', read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = ChallengeParticipation
        fields = [
            'id', 'user', 'user_id', 'challenge_name', 'current_progress',
            'is_completed', 'completion_date', 'progress_percentage', 'joined_at'
        ]
        read_only_fields = ['id', 'completion_date', 'joined_at']


class WeeklyChallengeSerializer(serializers.ModelSerializer):
    participants = ChallengeParticipationSerializer(
        source='challengeparticipation_set', 
        many=True, 
        read_only=True
    )
    participant_count = serializers.SerializerMethodField()
    user_participation = serializers.SerializerMethodField()
    
    def get_participant_count(self, obj):
        return obj.challengeparticipation_set.count()
    
    def get_user_participation(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            participation = obj.challengeparticipation_set.filter(user=request.user).first()
            if participation:
                return ChallengeParticipationSerializer(participation).data
        return None
    
    class Meta:
        model = WeeklyChallenge
        fields = [
            'id', 'name', 'description', 'challenge_type', 'target_value',
            'points_reward', 'start_date', 'end_date', 'is_active',
            'participants', 'participant_count', 'user_participation', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']