from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from userprofiles.choice import Investment_tools

from .forms import ProfileForm
from .models import Profile

# Create your views here.


@login_required
def index(req):

    if req.method == "POST":
        form = ProfileForm(req.POST)
        # user = authenticate(User.id=2,username=username)
        if form.is_valid():
            # 使用 request.user 來獲取當前登入的使用者
            user = req.user
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
            return redirect(reverse("userprofiles:index"))
        else:
            print(form.errors)
            # return render(req, "users/new.html", {"form": form})

    try:
        post = Profile.objects.get(user=req.user)
    except Profile.DoesNotExist:
        post = None

    return render(req, "userprofiles/index.html", {"post": post})


@login_required
def show(req, id):
    post = get_object_or_404(Profile, pk=id)

    # 將 Investment_tools 轉換為字典
    Investment_tools_dict = dict(Investment_tools)

    # 根據 post.investment_tool 中的值，找到對應的中文名稱
    investment_tool_names = [
        Investment_tools_dict.get(tool, tool) for tool in post.investment_tool
    ]

    if req.method == "POST":
        form = ProfileForm(req.POST, instance=post)
        if form.is_valid():
            form.save()
        else:
            return render(req, "userprofiles/edit.html", {"form": form, "post": post})

    return render(
        req,
        "userprofiles/show.html",
        {"post": post, "investment_tool_names": investment_tool_names},
    )


@login_required
def new(req):
    form = ProfileForm()
    return render(req, "userprofiles/new.html", {"form": form})


@login_required
def edit(req, id):
    post = get_object_or_404(Profile, pk=id)
    form = ProfileForm(instance=post)
    return render(req, "userprofiles/edit.html", {"form": form, "post": post})
