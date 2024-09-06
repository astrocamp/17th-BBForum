import logging
import random

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F, Sum
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from .models import PointsDetails, Post, UserProfile

logger = logging.getLogger(__name__)
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


@login_required
def simulate_login_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    today = timezone.now().date()

    # 檢查是否是當天第一次登入
    if profile.last_login_date != today:
        profile.points += 1  # 每天第一次登入加1點
        profile.last_login_date = today
        profile.save()
        PointsDetails.objects.create(user=user, action_type="每日登入", point_number=1)
        message = "今天第一次登入，獲得1點登入獎勵。"
    else:
        message = "今天已經獲得過登入獎勵。"

    # 確保用戶已登入
    if not request.user.is_authenticated:
        login(request, user)

    # 重定向到首頁
    return redirect("home")


@login_required
def home_view(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    return render(
        request, "layouts/base.html", {"user": user, "points": profile.points}
    )


@login_required
def points_log_view(request):
    user = request.user
    logs = PointsDetails.objects.filter(user=user).order_by("-actioned_at")
    return render(request, "layouts/points_log.html", {"user": user, "logs": logs})


@login_required
def simulate_post_view(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    today = timezone.now().date()

    # 檢查是否是當天第一次發文
    if profile.last_post_date != today:
        profile.post_count_today = 0
        profile.last_post_date = today

    if profile.post_count_today < 5:
        profile.points += 2  # 每次發文加2點
        profile.post_count_today += 1
        profile.save()
        PointsDetails.objects.create(user=user, action_type="發文", point_number=2)
        message = "發文成功，獲得2點獎勵。"
    else:
        message = "今天的發文點數已達上限。"

    return redirect("home")


@login_required
def simulate_like_view(request, post_id):
    post = Post.objects.get(id=post_id)
    post.likes += 1
    post.save()

    user = post.user
    profile = UserProfile.objects.get(user=user)

    if post.likes % 100 == 0:
        profile.points += 10  # 每100個讚加10點
        profile.save()
        PointsDetails.objects.create(user=user, action_type="點讚", point_number=10)

    return redirect("home")


@login_required
def report_user(request, post_id):
    post = Post.objects.get(id=post_id)
    user = post.user
    profile = UserProfile.objects.get(user=user)

    profile.points -= 2  # 被檢舉扣2點
    profile.is_reported = True
    profile.save()
    PointsDetails.objects.create(user=user, action_type="被檢舉", point_number=-2)

    return redirect("home")


@login_required
def reset_points(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    profile.points = 0
    profile.is_reported = False
    profile.save()

    return redirect("home")


def index(request):
    return render(request, "points/index.html")


def points_view(request):
    return render(request, "points/points.html")
