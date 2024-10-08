from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from storages.backends.s3boto3 import S3Boto3Storage
from taggit.managers import TaggableManager

from lib.models.image_save import ImageSaveMixin
from lib.models.soft_delete import SoftDeleteable, SoftDeleteManager
from userprofiles.models import Profile


class IndustryTag(models.Model):
    security_code = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)

    class Meta:
        db_table = "twse_industry_data"

    def __str__(self):
        return self.name


class Article(SoftDeleteable, ImageSaveMixin, models.Model):
    title = models.CharField(max_length=200)
    stockID = models.CharField(max_length=10)
    content = models.TextField()
    post_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    photo = models.ImageField(
        upload_to="images/",
        null=True,
        blank=True,
        storage=S3Boto3Storage,
    )
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tags = TaggableManager()
    stock = models.ManyToManyField(IndustryTag, blank=True)
    liked = models.ManyToManyField(User, related_name="liked")
    points_awarded = models.IntegerField(default=0)
    collectors = models.ManyToManyField(User, related_name="collected")

    objects = SoftDeleteManager()

    def liked_by(self, user):
        return self.liked.filter(id=user.id).exists()

    def collected_by(self, user):
        return self.collectors.filter(id=user.id).exists()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.user:
            profile, created = Profile.objects.get_or_create(user=self.user)
            profile.add_points()
            profile.save()


class Comment(SoftDeleteable, models.Model):
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    photo = models.ImageField(upload_to="images/", null=True, blank=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    objects = SoftDeleteManager()

    class Meta:
        indexes = [
            models.Index(fields=["deleted_at"]),
        ]
