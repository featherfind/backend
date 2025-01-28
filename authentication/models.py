from django.contrib.auth.models import User
from django.db import models

class UserTier(models.Model):
    TIER_CHOICES = [
        (0, 'Tier 0'),
        (1, 'Tier 1'),
        (2, 'Tier 2'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tier')
    tier = models.PositiveSmallIntegerField(choices=TIER_CHOICES, default=0)

    def __str__(self):
        return f"{self.user.username} - Tier {self.tier}"
