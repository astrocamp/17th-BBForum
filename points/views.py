import json
import logging
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from social_django.utils import load_strategy

from points.models import UserProfile
from userprofiles.models import Profile


#  顯示用戶的點數
def show_profile(request):
    user = request.user
    tot_point = 0
    if user.is_authenticated:
        profile, created = Profile.objects.all()
        tot_point = profile.tot_point  # 獲取點數

    # 將點數傳遞到模板中
    return render(
        request, "pages/main_page/_left_nav_bar.html", {"tot_point": tot_point}
    )


# 使用者登錄後，確保點數已經更新
@login_required
def register_points(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    tot_point = profile.tot_point  # 獲取點數

    # 返回渲染的模板
    return render(
        request, "pages/main_page/_left_nav_bar.html", {"tot_point": tot_point}
    )


# 自訂 JSON 編碼器，用來處理 Decimal 類型
class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


# 用來處理點數更新邏輯的 pipeline
def register_points_pipeline(strategy, details, user=None, *args, **kwargs):
    if user:
        request = strategy.request
        today = timezone.now().date()
        profile, created = Profile.objects.get_or_create(user=user)

        # 如果今天還沒有更新過點數，則加 1 點
        if profile.last_login_date != today:
            profile.tot_point += 1
            profile.last_login_date = today
            profile.save()

        # 將更新後的點數存儲在 session 中
        request.session["points"] = json.dumps(profile.tot_point, cls=CustomJSONEncoder)
