from django.contrib import admin
from .models import UserProfile, PointLog, PointsDetails

admin.site.register(UserProfile)
admin.site.register(PointLog)
admin.site.register(PointsDetails)
