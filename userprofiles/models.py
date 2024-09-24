import io

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from PIL import Image
from storages.backends.s3boto3 import S3Boto3Storage

from .choice import (
    Education_level,
    Gender,
    Inves_attributes,
    Investment_experience_choices,
    Profession,
    Taiwan_regions,
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=Gender.choices, default="")
    birthday = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, choices=Taiwan_regions, default="TP")
    education = models.CharField(
        max_length=200,
        choices=Education_level.choices,
        default=Education_level.MIDDLE_SCHOOL_OR_BELOW,
    )
    profession = models.CharField(
        max_length=30,
        choices=Profession,
        default="other",
    )

    investment_experience = models.CharField(
        max_length=20, choices=Investment_experience_choices, default="0-1"
    )
    investment_tool = models.JSONField(default=list)
    investment_attributes = models.CharField(
        max_length=200, choices=Inves_attributes.choices, default=""
    )
    tot_point = models.IntegerField(default=0)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)
    last_point_date = models.DateField(null=True, blank=True)
    user_img = models.ImageField(
        upload_to="user_images/", null=True, blank=True, storage=S3Boto3Storage()
    )

    def __str__(self):
        return self.user.username

    def add_points(self):
        from articles.models import Article

        today = timezone.now().date()

        # 獲取今天發佈的前五篇文章
        articles_today = Article.objects.filter(
            user=self.user, post_at__date=today
        ).order_by("post_at")

        points_to_add = 0
        for article in articles_today[:5]:
            if article.points_awarded == 0:  # 確保每篇文章只獲得一次點數
                points_to_add += 2  # 每篇文章增加2點
                article.points_awarded = 2
                article.save()

        # 如果今天有計算點數，就更新總點數和日期
        if points_to_add > 0:
            self.tot_point += points_to_add
            self.save()
            self.last_point_date = today
            self.save()

            print(f"用戶 {self.user.username} 的新總點數: {self.tot_point}")
        else:
            print(f"今天沒有為用戶 {self.user.username} 發放點數。")

    def clean(self):
        super().clean()
        if self.birthday and self.birthday > timezone.now().date():
            raise ValidationError("生日不能選擇未來的日期。")

    def save(self, *args, **kwargs):
        if self.user_img:
            img = Image.open(self.user_img)
            img_io = io.BytesIO()
            img.seek(0)
            img_size = self.user_img.size
            if img_size > 200 * 1024:
                img.save(img_io, format="WEBP", quality=80)
                img_io.seek(0)
                self.user_img.save(
                    self.user_img.name, ContentFile(img_io.read()), save=False
                )

        super().save(*args, **kwargs)
