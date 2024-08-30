from django.contrib import admin

from .models import PointLog, PointsDetails, UserProfile

admin.site.register(UserProfile)
admin.site.register(PointLog)
admin.site.register(PointsDetails)
