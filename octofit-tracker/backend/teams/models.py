from djongo import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    captain = models.ForeignKey(User, on_delete=models.CASCADE, related_name='captained_teams')
    members = models.ManyToManyField(User, through='TeamMembership', related_name='teams')
    max_members = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(2), MaxValueValidator(50)]
    )
    is_public = models.BooleanField(default=True)
    join_code = models.CharField(max_length=8, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.teammembership_set.filter(is_active=True).count()

    @property
    def total_points(self):
        return sum(
            membership.user.activities.aggregate(
                total=models.Sum('points_earned')
            )['total'] or 0
            for membership in self.teammembership_set.filter(is_active=True)
        )

    def save(self, *args, **kwargs):
        if not self.join_code:
            import random
            import string
            self.join_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'


class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[
            ('captain', 'Captain'),
            ('co_captain', 'Co-Captain'),
            ('member', 'Member'),
        ],
        default='member'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    points_contributed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} in {self.team.name}"

    class Meta:
        verbose_name = 'Team Membership'
        verbose_name_plural = 'Team Memberships'
        unique_together = ['team', 'user']


class TeamChallenge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    participating_teams = models.ManyToManyField(Team, related_name='challenges')
    challenge_type = models.CharField(
        max_length=30,
        choices=[
            ('total_activities', 'Total Activities'),
            ('total_duration', 'Total Duration'),
            ('total_distance', 'Total Distance'),
            ('total_calories', 'Total Calories'),
            ('consistency', 'Consistency Challenge'),
        ]
    )
    target_value = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    winner_team = models.ForeignKey(
        Team, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='won_challenges'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Team Challenge'
        verbose_name_plural = 'Team Challenges'
        ordering = ['-start_date']


class TeamInvitation(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invitations')
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_invitations')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('declined', 'Declined'),
            ('expired', 'Expired'),
        ],
        default='pending'
    )
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invitation to {self.invited_user.username} for {self.team.name}"

    class Meta:
        verbose_name = 'Team Invitation'
        verbose_name_plural = 'Team Invitations'
        unique_together = ['team', 'invited_user']
