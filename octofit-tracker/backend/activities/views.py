from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import ActivityType, Activity, WorkoutPlan
from .serializers import (
    ActivityTypeSerializer, ActivitySerializer, WorkoutPlanSerializer,
    WorkoutPlanCreateSerializer
)


class ActivityTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for activity types - read only for all users"""
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get activity types grouped by category"""
        categories = {}
        for activity_type in self.get_queryset():
            category = activity_type.category
            if category not in categories:
                categories[category] = []
            categories[category].append(ActivityTypeSerializer(activity_type).data)
        return Response(categories)


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for user activities with filtering and stats"""
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user activity statistics"""
        queryset = self.get_queryset()
        
        # Get date range from query params
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        recent_activities = queryset.filter(date_recorded__gte=start_date)
        
        stats = {
            'total_activities': queryset.count(),
            'recent_activities': recent_activities.count(),
            'total_duration': queryset.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0,
            'total_calories': queryset.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
            'total_distance': queryset.aggregate(Sum('distance_km'))['distance_km__sum'] or 0,
            'avg_duration': queryset.aggregate(Avg('duration_minutes'))['duration_minutes__avg'] or 0,
            'activities_by_type': queryset.values('activity_type__name').annotate(
                count=Count('id'),
                total_duration=Sum('duration_minutes')
            ),
            'activities_by_intensity': queryset.values('intensity').annotate(
                count=Count('id')
            )
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities"""
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now() - timedelta(days=days)
        recent_activities = self.get_queryset().filter(date_recorded__gte=start_date)
        serializer = self.get_serializer(recent_activities, many=True)
        return Response(serializer.data)


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    """ViewSet for workout plans"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Show user's own plans and public plans
        return WorkoutPlan.objects.filter(
            Q(created_by=self.request.user) | Q(is_public=True)
        )
    
    def get_serializer_class(self):
        if self.action == 'create':
            return WorkoutPlanCreateSerializer
        return WorkoutPlanSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_plans(self, request):
        """Get user's own workout plans"""
        my_plans = WorkoutPlan.objects.filter(created_by=request.user)
        serializer = self.get_serializer(my_plans, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def public_plans(self, request):
        """Get public workout plans"""
        public_plans = WorkoutPlan.objects.filter(is_public=True)
        serializer = self.get_serializer(public_plans, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def copy(self, request, pk=None):
        """Copy a workout plan to user's collection"""
        original_plan = self.get_object()
        
        # Create a copy
        new_plan = WorkoutPlan.objects.create(
            name=f"{original_plan.name} (Copy)",
            description=original_plan.description,
            created_by=request.user,
            difficulty_level=original_plan.difficulty_level,
            duration_weeks=original_plan.duration_weeks,
            is_public=False
        )
        
        # Copy exercises
        for exercise in original_plan.exercises.all():
            exercise.pk = None  # This will create a new object
            exercise.workout_plan = new_plan
            exercise.save()
        
        serializer = self.get_serializer(new_plan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
