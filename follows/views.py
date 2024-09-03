from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserFollowing
from django.contrib.auth.models import User




@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    is_following = UserFollowing.objects.filter(user=request.user, following_user=user).exists() if request.user.is_authenticated else False
    return render(request, 'user_profile.html', {'user': user, 'is_following': is_following})

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    
    if request.user == user_to_follow:
        return render(request, 'error.html', {'message': 'You cannot follow yourself.'})
    
    if not UserFollowing.objects.filter(user=request.user, following_user=user_to_follow).exists():
        UserFollowing.objects.create(user=request.user, following_user=user_to_follow)
    
    return redirect('user_profile', user_id=user_id)