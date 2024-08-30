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
            return redirect("home")
    return render(request, "registration/login.html")

def simulate_login_view(request):
    if request.method == "POST":
        user, _ = User.objects.get_or_create(id=1, defaults={"username": "testuser"})
        profile, _ = UserProfile.objects.get_or_create(user=user)
        
        today = timezone.now().date()
        
        if profile.last_login_date != today:
            profile.points += 1
            profile.last_login_date = today
            profile.save()
            message = "登入成功！獲得1點。"
        else:
            message = "今天已經登入過了，不能再獲得積分。"
        
        return render(request, "members/result.html", {"message": message, "points": profile.points})
    
    return render(request, "members/simulate_actions.html")

# 新增重置功能
def reset_points(request):
    if request.method == "POST":
        user = User.objects.get(id=1)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.points = 0
        profile.last_login_date = None
        profile.last_post_date = None
        profile.post_count_today = 0
        profile.save()
        
        PointsDetails.objects.filter(user=user).delete()
        
        return render(request, "members/result.html", {"message": "積分已重置", "points": 0})
    
    return render(request, "members/reset_confirm.html")


def simulate_post_view(request):
    if request.method == "POST":
        user = User.objects.get(id=1)
        profile = UserProfile.objects.get(user=user)

        today = timezone.now().date()

        if profile.last_post_date != today:
            profile.post_count_today = 0

        if profile.post_count_today < 5:
            points_to_add = 2  # 每次發文固定獲得2分
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

def reset_points(request):
    if request.method == "POST":
        user = User.objects.get(id=1)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.points = 0
        profile.last_login_date = None
        profile.last_post_date = None
        profile.post_count_today = 0
        profile.save()
        
        PointsDetails.objects.filter(user=user).delete()
        
        return render(request, "members/result.html", {"message": "積分已重置", "points": 0})
    
    return render(request, "members/reset_confirm.html")
