from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .models import UserFollowing


@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    is_following = UserFollowing.objects.filter(
        user=request.user, following_user=user
    ).exists()
    return render(
        request,
        "pages/main_page/index.html",
        {
            "user": user,
            "target_user": user,
            "is_following": is_following,
        },
    )


@login_required
def follow_user(request):
    if request.method == "POST":
        target_id = 1
        target_user = get_object_or_404(User, id=target_id)
        if not UserFollowing.objects.filter(
            user=request.user, following_user=target_user
        ).exists():
            UserFollowing.objects.create(user=request.user, following_user=target_user)
        else:
            UserFollowing.objects.filter(
                user=request.user, following_user=target_user
            ).delete()
        return redirect("http://127.0.0.1:8000/")
