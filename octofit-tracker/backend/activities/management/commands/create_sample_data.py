from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from activities.models import ActivityType
from accounts.models import UserProfile
from leaderboard.models import Achievement


class Command(BaseCommand):
    help = 'Create initial sample data for OctoFit Tracker'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create activity types
        activity_types = [
            {
                'name': 'Running',
                'description': 'Outdoor or treadmill running',
                'category': 'cardio',
                'calories_per_minute': 12.0,
                'points_multiplier': 1.5
            },
            {
                'name': 'Walking',
                'description': 'Casual or brisk walking',
                'category': 'cardio',
                'calories_per_minute': 5.0,
                'points_multiplier': 1.0
            },
            {
                'name': 'Push-ups',
                'description': 'Upper body strength exercise',
                'category': 'strength',
                'calories_per_minute': 8.0,
                'points_multiplier': 1.3
            },
            {
                'name': 'Cycling',
                'description': 'Bicycle riding indoor or outdoor',
                'category': 'cardio',
                'calories_per_minute': 10.0,
                'points_multiplier': 1.4
            },
            {
                'name': 'Yoga',
                'description': 'Flexibility and mindfulness practice',
                'category': 'flexibility',
                'calories_per_minute': 3.0,
                'points_multiplier': 1.2
            },
            {
                'name': 'Swimming',
                'description': 'Pool or open water swimming',
                'category': 'cardio',
                'calories_per_minute': 14.0,
                'points_multiplier': 1.8
            },
            {
                'name': 'Weight Training',
                'description': 'Resistance training with weights',
                'category': 'strength',
                'calories_per_minute': 6.0,
                'points_multiplier': 1.4
            },
            {
                'name': 'Basketball',
                'description': 'Team sport - basketball',
                'category': 'sports',
                'calories_per_minute': 11.0,
                'points_multiplier': 1.6
            },
            {
                'name': 'Stretching',
                'description': 'Basic stretching routine',
                'category': 'flexibility',
                'calories_per_minute': 2.0,
                'points_multiplier': 0.8
            },
            {
                'name': 'Dance',
                'description': 'Various forms of dance',
                'category': 'cardio',
                'calories_per_minute': 7.0,
                'points_multiplier': 1.3
            }
        ]
        
        for activity_data in activity_types:
            activity_type, created = ActivityType.objects.get_or_create(
                name=activity_data['name'],
                defaults=activity_data
            )
            if created:
                self.stdout.write(f'Created activity type: {activity_type.name}')
        
        # Create achievements
        achievements = [
            {
                'name': 'First Step',
                'description': 'Complete your first activity',
                'category': 'milestone',
                'requirement_type': 'total_activities',
                'requirement_value': 1,
                'points_reward': 10,
                'badge_icon': 'fas fa-baby-carriage'
            },
            {
                'name': 'Getting Started',
                'description': 'Complete 5 activities',
                'category': 'activity',
                'requirement_type': 'total_activities',
                'requirement_value': 5,
                'points_reward': 25,
                'badge_icon': 'fas fa-play'
            },
            {
                'name': 'Consistent',
                'description': 'Maintain a 7-day streak',
                'category': 'streak',
                'requirement_type': 'current_streak',
                'requirement_value': 7,
                'points_reward': 50,
                'badge_icon': 'fas fa-fire'
            },
            {
                'name': 'Century Club',
                'description': 'Earn 100 total points',
                'category': 'milestone',
                'requirement_type': 'total_points',
                'requirement_value': 100,
                'points_reward': 30,
                'badge_icon': 'fas fa-trophy'
            },
            {
                'name': 'Marathon Time',
                'description': 'Exercise for 1000 total minutes',
                'category': 'duration',
                'requirement_type': 'total_duration',
                'requirement_value': 1000,
                'points_reward': 75,
                'badge_icon': 'fas fa-stopwatch'
            },
            {
                'name': 'Long Distance',
                'description': 'Travel 50km total distance',
                'category': 'distance',
                'requirement_type': 'total_distance',
                'requirement_value': 50,
                'points_reward': 60,
                'badge_icon': 'fas fa-road'
            },
            {
                'name': 'Dedication',
                'description': 'Complete 50 activities',
                'category': 'activity',
                'requirement_type': 'total_activities',
                'requirement_value': 50,
                'points_reward': 100,
                'badge_icon': 'fas fa-medal'
            },
            {
                'name': 'Streak Master',
                'description': 'Maintain a 30-day streak',
                'category': 'streak',
                'requirement_type': 'current_streak',
                'requirement_value': 30,
                'points_reward': 200,
                'badge_icon': 'fas fa-crown'
            }
        ]
        
        for achievement_data in achievements:
            achievement, created = Achievement.objects.get_or_create(
                name=achievement_data['name'],
                defaults=achievement_data
            )
            if created:
                self.stdout.write(f'Created achievement: {achievement.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )