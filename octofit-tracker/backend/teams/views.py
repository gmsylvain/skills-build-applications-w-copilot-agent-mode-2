from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from .models import Team, TeamMembership, TeamChallenge, TeamInvitation
from .serializers import (
    TeamSerializer, TeamCreateSerializer, TeamMembershipSerializer,
    TeamChallengeSerializer, TeamInvitationSerializer
)


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for teams with membership management"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Show teams user is a member of or public teams
        user_teams = Team.objects.filter(
            teammembership__user=self.request.user,
            teammembership__is_active=True
        )
        public_teams = Team.objects.filter(is_public=True)
        return (user_teams | public_teams).distinct()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TeamCreateSerializer
        return TeamSerializer
    
    def perform_create(self, serializer):
        team = serializer.save(captain=self.request.user)
        # Automatically add creator as captain member
        TeamMembership.objects.create(
            team=team,
            user=self.request.user,
            role='captain'
        )
    
    @action(detail=False, methods=['get'])
    def my_teams(self, request):
        """Get teams where user is a member"""
        my_teams = Team.objects.filter(
            teammembership__user=request.user,
            teammembership__is_active=True
        )
        serializer = self.get_serializer(my_teams, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a team using join code or direct invitation"""
        team = self.get_object()
        join_code = request.data.get('join_code')
        
        # Check if team is full
        if team.member_count >= team.max_members:
            return Response(
                {'detail': 'Team is full'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check join code for public teams
        if team.is_public and join_code and team.join_code != join_code:
            return Response(
                {'detail': 'Invalid join code'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user is already a member
        existing_membership = TeamMembership.objects.filter(
            team=team, 
            user=request.user,
            is_active=True
        ).exists()
        
        if existing_membership:
            return Response(
                {'detail': 'Already a member of this team'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create membership
        membership = TeamMembership.objects.create(
            team=team,
            user=request.user,
            role='member'
        )
        
        serializer = TeamMembershipSerializer(membership)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a team"""
        team = self.get_object()
        
        try:
            membership = TeamMembership.objects.get(
                team=team, 
                user=request.user,
                is_active=True
            )
            
            if membership.role == 'captain':
                return Response(
                    {'detail': 'Captain cannot leave team. Transfer captaincy first.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            membership.is_active = False
            membership.save()
            
            return Response({'detail': 'Successfully left team'})
            
        except TeamMembership.DoesNotExist:
            return Response(
                {'detail': 'Not a member of this team'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class TeamMembershipViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing team memberships"""
    serializer_class = TeamMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only show memberships for teams user belongs to
        user_teams = Team.objects.filter(
            teammembership__user=self.request.user,
            teammembership__is_active=True
        )
        return TeamMembership.objects.filter(
            team__in=user_teams,
            is_active=True
        )


class TeamChallengeViewSet(viewsets.ModelViewSet):
    """ViewSet for team challenges"""
    serializer_class = TeamChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Show challenges for teams user belongs to
        user_teams = Team.objects.filter(
            teammembership__user=self.request.user,
            teammembership__is_active=True
        )
        return TeamChallenge.objects.filter(
            participating_teams__in=user_teams
        ).distinct()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active challenges"""
        active_challenges = self.get_queryset().filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
        serializer = self.get_serializer(active_challenges, many=True)
        return Response(serializer.data)
