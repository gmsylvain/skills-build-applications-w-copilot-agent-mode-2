from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile, FitnessGoal
from .serializers import UserProfileSerializer, FitnessGoalSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user profiles with automatic user assignment"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update the current user's profile"""
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            if request.method == 'GET':
                return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
            # Create profile if it doesn't exist during update
            profile = UserProfile.objects.create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FitnessGoalViewSet(viewsets.ModelViewSet):
    """ViewSet for fitness goals with user filtering"""
    serializer_class = FitnessGoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return FitnessGoal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active (non-achieved) goals"""
        active_goals = self.get_queryset().filter(is_achieved=False)
        serializer = self.get_serializer(active_goals, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def achieved(self, request):
        """Get all achieved goals"""
        achieved_goals = self.get_queryset().filter(is_achieved=True)
        serializer = self.get_serializer(achieved_goals, many=True)
        return Response(serializer.data)
