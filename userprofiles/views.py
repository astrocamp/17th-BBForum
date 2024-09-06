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
    try:
        # 嘗試獲取當前登入用戶的 Profile 資料
        profile = Profile.objects.get(user=req.user)
        # 如果有資料，重定向到 show 頁面
        return redirect(reverse("userprofiles:show", args=[profile.id]))
    except Profile.DoesNotExist:
        # 如果沒有資料，重定向到 new 頁面
        return redirect(reverse("userprofiles:new"))


@login_required
def new_save(req):
    if req.method == "POST":
        form = ProfileForm(req.POST)
        if form.is_valid():
            user = req.user
            profile = form.save(commit=False)
            profile.user = user

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

            # 如果成功保存，則 profile 已經存在並且有一個有效的 id
            return redirect(reverse("userprofiles:show", kwargs={"id": profile.id}))
        else:
            print(form.errors)

    # 如果請求不是 POST 或表單無效
    return render(req, "userprofiles/new.html", {"form": ProfileForm()})


@login_required
def show(req, id):
    post = get_object_or_404(Profile, pk=id)

    # 將 Investment_tools 轉換為字典
    Investment_tools_dict = dict(Investment_tools)

    # 根據 post.investment_tool 中的值，找到對應的中文名稱
    investment_tool_names = [
        Investment_tools_dict.get(tool, tool) for tool in post.investment_tool
    ]

    # 確保重新讀取最新的資料
    if req.method == "POST":
        form = ProfileForm(req.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(
                reverse("userprofiles:show", kwargs={"id": form.instance.id})
            )
        else:
            return render(req, "userprofiles/edit.html", {"form": form, "post": post})

    # 返回顯示頁面，確保使用最新的數據
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
    if req.method == "POST":
        form = ProfileForm(req.POST, instance=post)
        if form.is_valid():
            form.save()

            # 表單保存後，重定向到顯示頁面
            return redirect(reverse("userprofiles:show", kwargs={"id": post.id}))

        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=post)

    return render(req, "userprofiles/edit.html", {"form": form, "post": post})
