from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from userprofiles.choice import Investment_tools

from .forms import ProfileForm
from .models import Profile


@login_required
def index(req):
    try:
        profile = Profile.objects.get(user=req.user)
        return redirect(reverse("userprofiles:show", args=[profile.id]))
    except Profile.DoesNotExist:
        return redirect(reverse("userprofiles:new"))


@login_required
def new_save(req):
    if req.method == "POST":
        form = ProfileForm(req.POST)
        if form.is_valid():
            user = req.user
            profile = form.save(commit=False)
            profile.user = user

            profile, created = Profile.objects.update_or_create(
                user=user,
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
            return redirect(reverse("userprofiles:show", kwargs={"id": profile.id}))
        else:
            print(form.errors)

    return render(req, "userprofiles/new.html", {"form": ProfileForm()})


@login_required
def show(req, id):
    post = get_object_or_404(Profile, pk=id)

    Investment_tools_dict = dict(Investment_tools)
    investment_tool_names = [
        Investment_tools_dict.get(tool, tool) for tool in post.investment_tool
    ]

    if req.method == "POST":
        form = ProfileForm(req.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(
                reverse("userprofiles:show", kwargs={"id": form.instance.id})
            )
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
    if req.method == "POST":
        form = ProfileForm(req.POST, instance=post)
        if form.is_valid():
            form.save()

            return redirect(reverse("userprofiles:show", kwargs={"id": post.id}))

        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=post)

    return render(req, "userprofiles/edit.html", {"form": form, "post": post})
