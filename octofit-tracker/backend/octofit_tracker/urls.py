"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Import viewsets for API routing
from accounts.views import UserProfileViewSet, FitnessGoalViewSet
from activities.views import ActivityTypeViewSet, ActivityViewSet, WorkoutPlanViewSet
from teams.views import TeamViewSet, TeamMembershipViewSet, TeamChallengeViewSet
from leaderboard.views import LeaderboardEntryViewSet, AchievementViewSet, WeeklyChallengeViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='userprofile')
router.register(r'fitness-goals', FitnessGoalViewSet, basename='fitnessgoal')
router.register(r'activity-types', ActivityTypeViewSet)
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'workout-plans', WorkoutPlanViewSet, basename='workoutplan')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'team-memberships', TeamMembershipViewSet, basename='teammembership')
router.register(r'team-challenges', TeamChallengeViewSet, basename='teamchallenge')
router.register(r'leaderboard', LeaderboardEntryViewSet)
router.register(r'achievements', AchievementViewSet)
router.register(r'weekly-challenges', WeeklyChallengeViewSet, basename='weeklychallenge')

@api_view(['GET'])
def api_root(request, format=None):
    """API root endpoint with links to all available endpoints"""
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev"
    else:
        base_url = "http://localhost:8000"
    
    return Response({
        'accounts': {
            'profiles': reverse('userprofile-list', request=request, format=format),
            'fitness_goals': reverse('fitnessgoal-list', request=request, format=format),
        },
        'activities': {
            'activity_types': reverse('activitytype-list', request=request, format=format),
            'activities': reverse('activity-list', request=request, format=format),
            'workout_plans': reverse('workoutplan-list', request=request, format=format),
        },
        'teams': {
            'teams': reverse('team-list', request=request, format=format),
            'memberships': reverse('teammembership-list', request=request, format=format),
            'challenges': reverse('teamchallenge-list', request=request, format=format),
        },
        'leaderboard': {
            'leaderboard': reverse('leaderboardentry-list', request=request, format=format),
            'achievements': reverse('achievement-list', request=request, format=format),
            'weekly_challenges': reverse('weeklychallenge-list', request=request, format=format),
        },
        'authentication': {
            'login': f"{base_url}/api/auth/login/",
            'logout': f"{base_url}/api/auth/logout/",
            'register': f"{base_url}/api/auth/registration/",
            'user': f"{base_url}/api/auth/user/",
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
