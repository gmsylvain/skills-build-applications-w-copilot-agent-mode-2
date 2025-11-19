from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Team, TeamMembership, TeamChallenge, TeamInvitation
from accounts.serializers import UserSerializer


class TeamMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(source='user.id', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    
    class Meta:
        model = TeamMembership
        fields = [
            'id', 'user', 'user_id', 'team_name', 'role', 'joined_at',
            'is_active', 'points_contributed'
        ]
        read_only_fields = ['id', 'joined_at', 'points_contributed']


class TeamSerializer(serializers.ModelSerializer):
    captain = UserSerializer(read_only=True)
    captain_id = serializers.CharField(source='captain.id', read_only=True)
    member_count = serializers.ReadOnlyField()
    total_points = serializers.ReadOnlyField()
    members = TeamMembershipSerializer(source='teammembership_set', many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'captain', 'captain_id', 'max_members',
            'is_public', 'join_code', 'member_count', 'total_points', 'members',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'join_code', 'created_at', 'updated_at']


class TeamCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for team creation"""
    class Meta:
        model = Team
        fields = ['name', 'description', 'max_members', 'is_public']


class TeamChallengeSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.CharField(source='created_by.id', read_only=True)
    participating_teams = TeamSerializer(many=True, read_only=True)
    participating_team_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    winner_team = TeamSerializer(read_only=True)
    winner_team_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = TeamChallenge
        fields = [
            'id', 'name', 'description', 'created_by', 'created_by_id',
            'participating_teams', 'participating_team_ids', 'challenge_type',
            'target_value', 'start_date', 'end_date', 'is_active',
            'winner_team', 'winner_team_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        participating_team_ids = validated_data.pop('participating_team_ids', [])
        challenge = TeamChallenge.objects.create(**validated_data)
        
        if participating_team_ids:
            teams = Team.objects.filter(id__in=participating_team_ids)
            challenge.participating_teams.set(teams)
        
        return challenge


class TeamInvitationSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    team_id = serializers.IntegerField(write_only=True)
    invited_user = UserSerializer(read_only=True)
    invited_user_id = serializers.IntegerField(write_only=True)
    invited_by = UserSerializer(read_only=True)
    invited_by_id = serializers.CharField(source='invited_by.id', read_only=True)
    
    class Meta:
        model = TeamInvitation
        fields = [
            'id', 'team', 'team_id', 'invited_user', 'invited_user_id',
            'invited_by', 'invited_by_id', 'status', 'message',
            'created_at', 'responded_at'
        ]
        read_only_fields = ['id', 'created_at', 'responded_at']