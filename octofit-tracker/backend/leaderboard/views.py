from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import (
    LeaderboardEntry, Achievement, UserAchievement,
    WeeklyChallenge, ChallengeParticipation
)
from .serializers import (
    LeaderboardEntrySerializer, AchievementSerializer, UserAchievementSerializer,
    WeeklyChallengeSerializer, ChallengeParticipationSerializer
)


class LeaderboardEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for leaderboard entries - read only"""
    queryset = LeaderboardEntry.objects.all().order_by('-total_points')
    serializer_class = LeaderboardEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        """Get top users by points"""
        limit = int(request.query_params.get('limit', 10))
        top_entries = self.get_queryset()[:limit]
        serializer = self.get_serializer(top_entries, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's leaderboard position"""
        try:
            entry = LeaderboardEntry.objects.get(user=request.user)
            serializer = self.get_serializer(entry)
            return Response(serializer.data)
        except LeaderboardEntry.DoesNotExist:
            # Create entry if it doesn't exist
            entry = LeaderboardEntry.update_user_stats(request.user)
            serializer = self.get_serializer(entry)
            return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def refresh_stats(self, request):
        """Refresh current user's statistics"""
        entry = LeaderboardEntry.update_user_stats(request.user)
        serializer = self.get_serializer(entry)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get leaderboard by different categories"""
        category = request.query_params.get('category', 'points')
        
        if category == 'activities':
            queryset = self.get_queryset().order_by('-total_activities')
        elif category == 'duration':
            queryset = self.get_queryset().order_by('-total_duration_minutes')
        elif category == 'calories':
            queryset = self.get_queryset().order_by('-total_calories_burned')
        elif category == 'distance':
            queryset = self.get_queryset().order_by('-total_distance_km')
        elif category == 'streak':
            queryset = self.get_queryset().order_by('-current_streak_days')
        else:  # default to points
            queryset = self.get_queryset()
        
        limit = int(request.query_params.get('limit', 10))
        top_entries = queryset[:limit]
        serializer = self.get_serializer(top_entries, many=True)
        return Response(serializer.data)


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for achievements - read only"""
    queryset = Achievement.objects.filter(is_active=True)
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_achievements(self, request):
        """Get current user's achievements"""
        user_achievements = UserAchievement.objects.filter(user=request.user)
        serializer = UserAchievementSerializer(user_achievements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get achievements user hasn't earned yet"""
        earned_achievement_ids = UserAchievement.objects.filter(
            user=request.user
        ).values_list('achievement_id', flat=True)
        
        available_achievements = self.get_queryset().exclude(
            id__in=earned_achievement_ids
        )
        serializer = self.get_serializer(available_achievements, many=True)
        return Response(serializer.data)


class WeeklyChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for weekly challenges"""
    serializer_class = WeeklyChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return WeeklyChallenge.objects.filter(is_active=True)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current active challenges"""
        today = timezone.now().date()
        current_challenges = self.get_queryset().filter(
            start_date__lte=today,
            end_date__gte=today
        )
        serializer = self.get_serializer(current_challenges, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a weekly challenge"""
        challenge = self.get_object()
        
        # Check if user is already participating
        participation, created = ChallengeParticipation.objects.get_or_create(
            user=request.user,
            challenge=challenge,
            defaults={'current_progress': 0.0}
        )
        
        if not created:
            return Response(
                {'detail': 'Already participating in this challenge'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ChallengeParticipationSerializer(participation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def my_challenges(self, request):
        """Get challenges user is participating in"""
        participations = ChallengeParticipation.objects.filter(user=request.user)
        challenge_ids = participations.values_list('challenge_id', flat=True)
        my_challenges = self.get_queryset().filter(id__in=challenge_ids)
        serializer = self.get_serializer(my_challenges, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """Get challenge leaderboard"""
        challenge_id = request.query_params.get('challenge_id')
        if not challenge_id:
            return Response(
                {'detail': 'challenge_id parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        participations = ChallengeParticipation.objects.filter(
            challenge_id=challenge_id
        ).order_by('-current_progress')
        
        serializer = ChallengeParticipationSerializer(participations, many=True)
        return Response(serializer.data)
