import json
import logging
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from social_django.utils import load_strategy

from articles.models import Article
from userprofiles.models import Profile


#  顯示用戶的點數
def show_profile(request):
    user = request.user
    tot_point = 0
    if user.is_authenticated:
        profile, created = Profile.objects.all()
        tot_point = profile.tot_point
    return render(
        request, "pages/main_page/_left_nav_bar.html", {"tot_point": tot_point}
    )


# 使用者登錄後，確保點數已經更新
@login_required
def register_points(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    tot_point = profile.tot_point

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

        # 獲取今天的貼文數量
        daily_posts = Article.objects.filter(user=user, created_at__date=today).count()

        # 如果今天還沒有更新過點數，則加 1 點（原有邏輯）
        if profile.last_login_date != today:
            profile.last_login_date = today
            profile.tot_point += 1  # 登入獲得1點
            profile.tot_point += min(
                10 - 1, daily_posts * 2
            )  # 每篇文章2點，最多9點（因為已經獲得1點）
            profile.save()

        # 將更新後的點數存儲在 session 中
        request.session["points"] = json.dumps(profile.tot_point, cls=CustomJSONEncoder)
