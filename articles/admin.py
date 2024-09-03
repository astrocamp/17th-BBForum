from django.contrib import admin

from django.contrib.auth.models import Group

# 创建组
for i in range(50):
    group_name = f"LV.{i}"
    Group.objects.get_or_create(name=group_name)
