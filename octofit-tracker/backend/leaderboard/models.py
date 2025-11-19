from djongo import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta


class LeaderboardEntry(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leaderboard_entry')
    total_points = models.PositiveIntegerField(default=0)
    total_activities = models.PositiveIntegerField(default=0)
    total_duration_minutes = models.PositiveIntegerField(default=0)
    total_calories_burned = models.PositiveIntegerField(default=0)
    total_distance_km = models.FloatField(default=0.0)
    current_streak_days = models.PositiveIntegerField(default=0)
    longest_streak_days = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateTimeField(null=True, blank=True)
    rank_position = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Rank #{self.rank_position}"

    @classmethod
    def update_user_stats(cls, user):
        """Update leaderboard statistics for a user"""
        from activities.models import Activity
        
        # Get all activities for the user
        activities = Activity.objects.filter(user=user)
        
        # Calculate totals
        totals = activities.aggregate(
            total_points=Sum('points_earned'),
            total_duration=Sum('duration_minutes'),
            total_calories=Sum('calories_burned'),
            total_distance=Sum('distance_km')
        )
        
        # Get or create leaderboard entry
        entry, created = cls.objects.get_or_create(user=user)
        
        # Update basic stats
        entry.total_points = totals['total_points'] or 0
        entry.total_activities = activities.count()
        entry.total_duration_minutes = totals['total_duration'] or 0
        entry.total_calories_burned = totals['total_calories'] or 0
        entry.total_distance_km = totals['total_distance'] or 0.0
        
        # Update streak information
        entry._update_streak_info()
        
        entry.save()
        return entry

    def _update_streak_info(self):
        """Calculate current and longest streaks"""
        from activities.models import Activity
        
        activities = Activity.objects.filter(
            user=self.user
        ).order_by('-date_recorded').values_list('date_recorded__date', flat=True).distinct()
        
        if not activities:
            self.current_streak_days = 0
            self.longest_streak_days = 0
            self.last_activity_date = None
            return
        
        activity_dates = list(activities)
        self.last_activity_date = timezone.make_aware(
            timezone.datetime.combine(activity_dates[0], timezone.datetime.min.time())
        )
        
        # Calculate current streak
        current_streak = 0
        today = timezone.now().date()
        
        for i, date in enumerate(activity_dates):
            expected_date = today - timedelta(days=i)
            if date == expected_date:
                current_streak += 1
            else:
                break
        
        self.current_streak_days = current_streak
        
        # Calculate longest streak
        longest_streak = 0
        temp_streak = 1
        
        for i in range(1, len(activity_dates)):
            if activity_dates[i-1] - activity_dates[i] == timedelta(days=1):
                temp_streak += 1
            else:
                longest_streak = max(longest_streak, temp_streak)
                temp_streak = 1
        
        self.longest_streak_days = max(longest_streak, temp_streak, current_streak)

    class Meta:
        verbose_name = 'Leaderboard Entry'
        verbose_name_plural = 'Leaderboard Entries'
        ordering = ['-total_points', '-total_activities']


class Achievement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(
        max_length=30,
        choices=[
            ('activity', 'Activity Based'),
            ('streak', 'Streak Based'),
            ('distance', 'Distance Based'),
            ('duration', 'Duration Based'),
            ('social', 'Social/Team Based'),
            ('milestone', 'Milestone'),
        ]
    )
    requirement_type = models.CharField(
        max_length=30,
        choices=[
            ('total_activities', 'Total Activities'),
            ('total_points', 'Total Points'),
            ('total_duration', 'Total Duration'),
            ('total_distance', 'Total Distance'),
            ('current_streak', 'Current Streak'),
            ('longest_streak', 'Longest Streak'),
            ('team_activities', 'Team Activities'),
        ]
    )
    requirement_value = models.PositiveIntegerField()
    points_reward = models.PositiveIntegerField(default=0)
    badge_icon = models.CharField(max_length=50, blank=True)  # FontAwesome icon class
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Achievement'
        verbose_name_plural = 'Achievements'


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    is_displayed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"

    class Meta:
        verbose_name = 'User Achievement'
        verbose_name_plural = 'User Achievements'
        unique_together = ['user', 'achievement']
        ordering = ['-earned_at']


class WeeklyChallenge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    challenge_type = models.CharField(
        max_length=30,
        choices=[
            ('total_activities', 'Total Activities'),
            ('total_duration', 'Total Duration (minutes)'),
            ('total_distance', 'Total Distance (km)'),
            ('consistency', 'Daily Consistency'),
            ('variety', 'Activity Variety'),
        ]
    )
    target_value = models.FloatField()
    points_reward = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    participants = models.ManyToManyField(User, through='ChallengeParticipation', related_name='weekly_challenges')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"

    class Meta:
        verbose_name = 'Weekly Challenge'
        verbose_name_plural = 'Weekly Challenges'
        ordering = ['-start_date']


class ChallengeParticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(WeeklyChallenge, on_delete=models.CASCADE)
    current_progress = models.FloatField(default=0.0)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.challenge.name}"

    @property
    def progress_percentage(self):
        if self.challenge.target_value == 0:
            return 0
        return min(100, (self.current_progress / self.challenge.target_value) * 100)

    class Meta:
        verbose_name = 'Challenge Participation'
        verbose_name_plural = 'Challenge Participations'
        unique_together = ['user', 'challenge']
