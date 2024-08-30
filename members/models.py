from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return self.user.username

class PointLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    points_change = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class PointsDetails(models.Model):
    action_type = models.CharField(max_length=50)
    actioned_at = models.DateTimeField(auto_now_add=True)
    point_number = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)




