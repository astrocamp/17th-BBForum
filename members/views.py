from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import PointsDetails
from .signals import add_points

@login_required
def points_log_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    logs = PointsDetails.objects.filter(userID=user_profile)
    return render(request, 'members/points_log.html', {'logs': logs})

@login_required
def login_view(request):
    add_points(request.user, 'login', 1)
    return redirect('home')
@login_required
def post_view(request):
    add_points(request.user, 'post', 2)
    return render(request, 'members/post.html')

@login_required
def like_view(request):
    likes_count = 15000000
    if likes_count > 100:  
        add_points(request.user, 'like', 10)
    return redirect('home')


# 課金和被檢舉

@login_required
def payment_view(request):
    amount = 100  
    points = amount
    add_points(request.user, 'payment', points)
    return render(request, 'members/payment.html')

@login_required
def report_view(request):
    add_points(request.user, 'report', -2)
    return redirect('home')

def add_points(user, action_type, points):
    # 获取或创建用户的用户资料
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    # 更新积分
    user_profile.points += points
    user_profile.save()

    # 记录积分变化
    PointsDetails.objects.create(user=user, action_type=action_type, point_number=points)
