from django.db import models
from django.contrib.auth.models import User
from .choice import Gender, Inves_attributes,TAIWAN_REGIONS,EducationLevel,INVESTMENT_TOOLS,INVESTMENT_EXPERIENCE_CHOICES

# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname=models.CharField(max_length=200)
    gender=models.CharField(max_length=2,choices=Gender.choices,default="")
    birthday=models.DateField()
    location = models.CharField(max_length=10, choices=TAIWAN_REGIONS, default="TP")
    education=models.CharField(max_length=2, choices=EducationLevel.choices, default=EducationLevel.MIDDLE_SCHOOL_OR_BELOW)
    Investment_experience=models.CharField(max_length=10, choices=INVESTMENT_EXPERIENCE_CHOICES, default='0-1')
    Investment_tool=models.JSONField(default=list) #JSONField 可以存儲列表，適合用於處理多選值
    investment_attributes=models.CharField(max_length=50,choices=Inves_attributes.choices,default="")
    tot_point=models.DecimalField(max_digits=10, decimal_places=0, default=None, null=True,blank=True)
    deleted_at=models.DateTimeField(default=None, null=True,blank=True)

    def __str__(self):
        return self.user.username
