from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from userprofiles.choice import Investment_tools

from .forms import ProfileForm
from .models import Profile


@login_required
def index(req):
    profile = get_object_or_404(Profile, user=req.user)  # 獲取用戶的 Profile
    if not profile.nickname or not profile.gender:
        return redirect(reverse("userprofiles:edit", args=[profile.id]))
    return redirect(reverse("userprofiles:show", args=[profile.id]))


@login_required
def show(req, id):
    post = get_object_or_404(Profile, pk=id)
    Investment_tools_dict = dict(Investment_tools)
    investment_tool_names = [
        Investment_tools_dict.get(tool, tool) for tool in post.investment_tool
    ]

    if req.method == "POST":
        form = ProfileForm(req.POST, req.FILES, instance=post)
        if form.is_valid():
            form.save()

            return redirect(
                reverse("userprofiles:show", kwargs={"id": form.instance.id})
            )
        else:
            return render(req, "userprofiles/edit.html", {"form": form, "post": post})
    profile = get_object_or_404(Profile, pk=id)
    user_img = profile.user_img
    return render(
        req,
        "userprofiles/show.html",
        {
            "post": post,
            "investment_tool_names": investment_tool_names,
            "user_img": user_img,
        },
    )


@login_required
def edit(req, id):
    post = get_object_or_404(Profile, pk=id)
    print(post)

    if req.method == "POST":
        form = ProfileForm(req.POST, req.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse("userprofiles:show", kwargs={"id": post.id}))
        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=post)

    profile = get_object_or_404(Profile, pk=id)
    user_img = profile.user_img

    return render(
        req,
        "userprofiles/edit.html",
        {"form": form, "post": post, "user_img": user_img},
    )
