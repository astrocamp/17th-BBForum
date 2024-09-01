import logging
import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.db.models import F
from django.db import transaction

from .models import PointsDetails, UserProfile, Post

logger = logging.getLogger(__name__)
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def simulate_login_view(request):
    user = User.objects.get(id=1)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    today = timezone.now().date()
    
    # 檢查是否是當天第一次"操作"（不僅僅是登入）
    if profile.last_login_date != today:
        profile.points += 1  # 每天第一次操作加1點
        profile.last_login_date = today
        profile.save()
        PointsDetails.objects.create(
            user=user,
            action_type="每日登入",
            point_number=1
        )
        message = "今天第一次操作，獲得1點登入獎勵。"
    else:
        message = "今天已經獲得過登入獎勵。"

    # 確保用戶已登入
    if not request.user.is_authenticated:
        login(request, user)
    
    return render(request, "layouts/simulate_actions.html", {
        "message": message,
        "points": profile.points,
        "likes": profile.like_count_today
    })

@login_required
def home_view(request):
    user = request.user
    return render(request, "layouts/base.html", {"user": user})

@login_required
def points_log_view(request):
    user = request.user
    logs = PointsDetails.objects.filter(user=user).order_by("-actioned_at")
    return render(request, "layouts/points_log.html", {"user": user, "logs": logs})

def simulate_post_view(request):
    # 首先確保用戶已登入並獲得登入獎勵
    login_response = simulate_login_view(request)
    if login_response.status_code != 200:
        return login_response

    if request.method == "POST":
        user = User.objects.get(id=1)
        profile = UserProfile.objects.get(user=user)

        if profile.is_reported:
            return render(request, "layouts/simulate_actions.html", {
                "message": "因該帳號被檢舉，無法發文",
                "points": profile.points,
                "likes": profile.like_count_today
            })

        today = timezone.now().date()
        if profile.last_post_date != today:
            profile.post_count_today = 0
            profile.last_post_date = today

        profile.post_count_today += 1
        
        # 創建新的貼文
        Post.objects.create(user=user, content=f"模擬貼文 {profile.post_count_today}")

        if profile.post_count_today <= 5:
            profile.points += 2
            PointsDetails.objects.create(
                user=user,
                action_type="發文獎勵",
                point_number=2
            )
            message = f"發文成功！獲得2點獎勵。今日第{profile.post_count_today}次發文。"
        else:
            message = f"發文成功！今日第{profile.post_count_today}次發文，不再獲得積分。"

        profile.save()

        return render(request, "layouts/simulate_actions.html", {
            "message": message,
            "points": profile.points,
            "likes": profile.like_count_today
        })

    return redirect("simulate_actions")

def simulate_like_view(request):
    # 首先確保用戶已登入並獲得登入獎勵
    login_response = simulate_login_view(request)
    if login_response.status_code != 200:
        return login_response

    if request.method == "POST":
        with transaction.atomic():
            user = User.objects.get(id=1)
            profile = UserProfile.objects.select_for_update().get(user=user)

            if profile.is_reported:
                message = "您的帳號已被檢舉，無法進行按讚操作。"
                return render(request, "layouts/simulate_actions.html", {
                    "message": message,
                    "points": profile.points,
                    "likes": profile.like_count_today
                })

            # 隨機選擇一篇貼文進行按讚
            post = Post.objects.order_by('?').first()
            if post:
                post.likes += 1
                post.save()

                profile.like_count_today += 1

                # 檢查是否達到100次按讚
                if profile.like_count_today % 100 == 0:
                    profile.points += 10
                    PointsDetails.objects.create(
                        user=user,
                        action_type="按讚獎勵",
                        point_number=10,
                    )
                    message = f"模擬按讚成功！您已完成{profile.like_count_today}次按讚，獲得10積分獎勵！"
                else:
                    message = f"模擬按讚成功！貼文現在有{post.likes}個讚。"

                profile.save()

                message += f" 今日按讚次數：{profile.like_count_today}。總積分：{profile.points}"
            else:
                message = "沒有可用的貼文進行按讚。"
        
        return render(request, "layouts/simulate_actions.html", {
            "message": message,
            "points": profile.points,
            "likes": profile.like_count_today
        })

    return redirect("simulate_actions")

def report_user(request):
    if request.method == "POST":
        user = User.objects.get(id=1)
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.is_reported = True
        profile.points -= 2  # 被檢舉扣2點
        profile.save()
        
        PointsDetails.objects.create(
            user=user,
            action_type="被檢舉扣分",
            point_number=-2,
        )
        
        return render(
            request,
            "layouts/simulate_actions.html",
            {
                "message": "用戶已被檢舉，帳號已停用，積分已扣除2點。",
                "points": profile.points,
                "likes": profile.like_count_today
            },
        )
    return render(request, "layouts/report_confirm.html")

def reset_points(request):
    if request.method == "POST":
        user = User.objects.get(id=1)
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.points = 0
        profile.like_count_today = 0
        profile.is_reported = False
        profile.last_login_date = None
        profile.last_post_date = None
        profile.post_count_today = 0
        profile.save()
        
        PointsDetails.objects.filter(user=user).delete()
        Post.objects.all().delete()  # 清除所有貼文
        
        return render(request, "layouts/simulate_actions.html", {
            "message": "積分已重置",
            "points": 0,
            "likes": 0
        })
    
    return render(request, "layouts/reset_confirm.html")


