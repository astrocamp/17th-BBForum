from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .choice import (
    Education_level,
    Gender,
    Inves_attributes,
    Investment_experience_choices,
    Profession,
    Taiwan_regions,
)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=Gender.choices, default="")
    birthday = models.DateField(null=False, blank=False)
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
    investment_tool = models.JSONField(
        default=list
    )  # JSONField 可以存儲列表，適合用於處理多選值
    investment_attributes = models.CharField(
        max_length=200, choices=Inves_attributes.choices, default=""
    )
    tot_point = models.DecimalField(
        max_digits=10, decimal_places=0, default=0, null=True, blank=True
    )
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def really_delete(self):
        self.user.delete()
        super().delete()
