from djongo import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class ActivityType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=30,
        choices=[
            ('cardio', 'Cardio'),
            ('strength', 'Strength Training'),
            ('flexibility', 'Flexibility'),
            ('sports', 'Sports'),
            ('other', 'Other'),
        ]
    )
    calories_per_minute = models.FloatField(
        validators=[MinValueValidator(0.1), MaxValueValidator(50.0)]
    )
    points_multiplier = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.1), MaxValueValidator(10.0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Activity Type'
        verbose_name_plural = 'Activity Types'


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(720)]  # Max 12 hours
    )
    intensity = models.CharField(
        max_length=10,
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
        ],
        default='moderate'
    )
    calories_burned = models.PositiveIntegerField(default=0)
    distance_km = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.01), MaxValueValidator(1000.0)]
    )
    notes = models.TextField(blank=True)
    date_recorded = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.date_recorded.date()})"

    @property
    def points_earned(self):
        base_points = self.duration_minutes * self.activity_type.points_multiplier
        intensity_multiplier = {'low': 0.8, 'moderate': 1.0, 'high': 1.2}
        return int(base_points * intensity_multiplier.get(self.intensity, 1.0))

    def save(self, *args, **kwargs):
        if not self.calories_burned:
            intensity_multiplier = {'low': 0.8, 'moderate': 1.0, 'high': 1.2}
            self.calories_burned = int(
                self.duration_minutes * 
                self.activity_type.calories_per_minute * 
                intensity_multiplier.get(self.intensity, 1.0)
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
        ordering = ['-date_recorded']


class WorkoutPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_workout_plans')
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ]
    )
    duration_weeks = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(52)]
    )
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Workout Plan'
        verbose_name_plural = 'Workout Plans'


class WorkoutExercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='exercises')
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    sets = models.PositiveIntegerField(default=1)
    reps = models.PositiveIntegerField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    rest_seconds = models.PositiveIntegerField(default=60)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.workout_plan.name} - {self.activity_type.name}"

    class Meta:
        verbose_name = 'Workout Exercise'
        verbose_name_plural = 'Workout Exercises'
        ordering = ['order']
