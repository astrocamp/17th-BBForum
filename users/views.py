from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ProfileForm, UserForm
from .models import Profile

# Create your views here.


def index(req):

    if req.method == "POST":
        form = ProfileForm(req.POST)
        # user = authenticate(User.id=2,username=username)
        if form.is_valid():
            user = User.objects.get(id=1)
            # 避免不必要的數據庫操作：如果表單中包含許多字段，並且你只想更新部分字段或添加額外的邏輯，這樣可以避免不必要的數據庫操作。
            profile = form.save(commit=False)
            profile.user = user  # 設置 user 字段
            # 使用 update_or_create 來創建或更新 profile
            profile, created = Profile.objects.update_or_create(
                user=user,  # 查找的條件
                defaults={
                    "nickname": profile.nickname,
                    "gender": profile.gender,
                    "birthday": profile.birthday,
                    "location": profile.location,
                    "education": profile.education,
                    "investment_experience": profile.investment_experience,
                    "investment_tool": profile.investment_tool,
                    "investment_attributes": profile.investment_attributes,
                },
            )
            profile.save()
            return redirect(reverse("users:index"))
        else:
            print(form.errors)
            # return render(req, "users/new.html", {"form": form})
    posts = Profile.objects.all()
    return render(req, "users/index.html", {"posts": posts})


def show(req, id):
    post = get_object_or_404(Profile, pk=id)
    if req.method == "POST":
        form = ProfileForm(req.POST, instance=post)
        if form.is_valid():
            form.save()
        else:
            return render(req, "users/edit.html", {"form": form, "post": post})
    return render(req, "users/show.html", {"post": post})


def new(req):
    form = ProfileForm()
    return render(req, "users/new.html", {"form": form})


def edit(req, id):
    post = get_object_or_404(Profile, pk=id)
    form = ProfileForm(instance=post)
    return render(req, "users/edit.html", {"form": form, "post": post})


def delete(req, id):
    post = get_object_or_404(User, pk=id)
    post.delete()
    return redirect("users:index")
