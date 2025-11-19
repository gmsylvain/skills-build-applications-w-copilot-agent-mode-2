from djongo import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    fitness_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )
    height = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.5), MaxValueValidator(3.0)]
    )  # in meters
    weight = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(20), MaxValueValidator(500)]
    )  # in kg
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class FitnessGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fitness_goals')
    goal_type = models.CharField(
        max_length=30,
        choices=[
            ('weight_loss', 'Weight Loss'),
            ('muscle_gain', 'Muscle Gain'),
            ('endurance', 'Endurance'),
            ('strength', 'Strength'),
            ('flexibility', 'Flexibility'),
        ]
    )
    target_value = models.FloatField()
    current_value = models.FloatField(default=0)
    target_date = models.DateField()
    is_achieved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.goal_type}"

    @property
    def progress_percentage(self):
        if self.target_value == 0:
            return 0
        return min(100, (self.current_value / self.target_value) * 100)

    class Meta:
        verbose_name = 'Fitness Goal'
        verbose_name_plural = 'Fitness Goals'
