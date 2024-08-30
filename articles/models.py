from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    stockID=models.CharField(max_length=10)
    content = models.TextField()
    post_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    photo=models.ImageField(upload_to='images/', null=True, blank=True)
    deleted_at=models.DateTimeField(default=None, null=True,blank=True)
    userID = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

