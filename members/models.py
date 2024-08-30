import logging

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    last_login_date = models.DateField(null=True, blank=True)
    last_post_date = models.DateField(null=True, blank=True)
    post_count_today = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s profile"


class PointLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    points_change = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user.user.username} - {self.action} - {self.points_change} points"
        )


class PointsDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50)
    point_number = models.IntegerField()
    actioned_at = models.DateTimeField(auto_now_add=True)
    point_number = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.action_type} - {self.point_number} points"
