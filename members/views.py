import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import PointsDetails, UserProfile

logger = logging.getLogger(__name__)
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


@login_required
def home_view(request):
    user = request.user
    return render(request, "members/home.html", {"user": user})


@login_required
def points_log_view(request):
    user = request.user
    logs = PointsDetails.objects.filter(user=user).order_by("-actioned_at")
    return render(request, "members/points_log.html", {"user": user, "logs": logs})


@login_required
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # 或者重定向到其他頁面
    return render(request, "registration/login.html")


@login_required
def post_view(request):
    user = request.user
    today = timezone.localdate(timezone.now())
    post_count_today = PointsDetails.objects.filter(
        user=user, action_type="post", actioned_at__date=today
    ).count()

    logger.info(f"Post count today for user {user.username}: {post_count_today}")

    if post_count_today >= 5:
        logger.info(
            f"User {user.username} has reached the daily post limit. No points will be awarded."
        )
        # 不進行任何操作
        return render(request, "members/post.html")

    # 每篇文章獲得 2 點積分
    add_points(user, "post", 2)
    return redirect("points_log")


@login_required
def like_view(request):
    user = request.user
    # 這裡的 likes_count 應該從實際情況來獲取，這裡只是示例
    likes_count = 15000000
    if likes_count > 100:
        add_points(user, "like", 10)
    return redirect("home")


@login_required
def payment_view(request):
    user = request.user
    amount = 100  # 假設金額等於積分數量
    add_points(user, "payment", amount)
    return render(request, "members/payment.html")


@login_required
def report_view(request):
    user = request.user
    add_points(user, "report", -2)
    return redirect("home")


def add_points(user, action_type, points):
    # 记录积分变化
    PointsDetails.objects.create(
        user=user, action_type=action_type, point_number=points
    )
    # 更新用戶資料中的積分
    user_profile, _ = UserProfile.objects.get_or_create(user=user)
    user_profile.points += points
    user_profile.save()
    logger.info(
        f"User {user.username} has been awarded {points} points for action {action_type}. Total points: {user_profile.points}"
    )


def simulate_login_view(request):
    if request.method == "POST":
        # 獲取或創建 id 為 1 的用戶
        user, _ = User.objects.get_or_create(id=1, defaults={"username": "testuser"})

        # 獲取或創建用戶檔案
        profile, _ = UserProfile.objects.get_or_create(user=user)

        today = timezone.now().date()

        if profile.last_login_date != today:
            # 如果今天還沒登入，增加一個點數
            profile.points += 1
            profile.last_login_date = today
            profile.save()
            message = "登入成功！獲得1點。"
        else:
            message = "今天已經登入過了，不再獲得積分。"

        return render(
            request,
            "members/result.html",
            {"message": message, "points": profile.points},
        )

    return render(request, "members/simulate_actions.html")


def simulate_post_view(request):
    if request.method == "POST":
        user = User.objects.get(id=1)
        profile = UserProfile.objects.get(user=user)

        today = timezone.now().date()

        if profile.last_post_date != today:
            profile.post_count_today = 0

        if profile.post_count_today < 5:
            points_to_add = min(2, 10 - (profile.points % 10))
            profile.points += points_to_add
            profile.post_count_today += 1
            profile.last_post_date = today
            profile.save()
            message = f"發文成功！獲得{points_to_add}點。"
        else:
            message = "今天已達到發文積分上限，不再獲得積分。"

        return render(
            request,
            "members/result.html",
            {"message": message, "points": profile.points},
        )

    return redirect("simulate_actions")
