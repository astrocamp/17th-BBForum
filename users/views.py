import os
import random
import string

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from userprofiles.models import Profile

from .forms import CustomUserCreationForm


def index(req):
    if req.method == "POST":
        form = CustomUserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, "註冊成功")
            return redirect("users:sign_in")
        else:
            return render(req, "users/register.html", {"form": form})
    return render(req, "layouts/base.html")


def register(req):
    return render(req, "users/register.html", {"hide_nav_and_footer": True})


def sign_in(req):
    if req.user.is_authenticated:
        return redirect("pages:index")
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(req, user)
            # 確保用戶有 Profile
            Profile.objects.get_or_create(user=user)  # 確保 Profile 存在
            messages.success(req, "登入成功")
            return redirect("pages:index")
        else:
            messages.error(req, "登入失敗")
            return render(req, "users/login.html", {"hide_nav_and_footer": True})
    return render(req, "users/login.html", {"hide_nav_and_footer": True})


def sign_out(req):
    if req.method == "POST":
        logout(req)
        messages.success(req, "登出成功")
        return redirect("pages:index")
    return redirect("pages:index")


def auth_denied(req):
    return render(req, "users/auth_denied.html")


def forget_password(req):
    if req.method == "GET":
        return render(req, "users/forget_password.html")
    else:
        username = req.POST.get("username")
        try:
            user = User.objects.get(username=username)
            email = user.email
            email_part = email[3:]

            random_password = "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )

            user.set_password(random_password)
            user.save()

            subject = "Password Reset Notification"

            send_mail_via_mailgun(subject, message, email)

            return render(
                req,
                "users/forget_password.html",
                {
                    "forget_password_tips": f"密碼已傳送至 *****{email_part}。 請確認收件夾或垃圾郵件。"
                },
            )
        except User.DoesNotExist:
            return render(
                req,
                "users/forget_password.html",
                {"forget_password_tips": f"帳號 {username} 不存在。"},
            )


def send_mail_via_mailgun(subject, message, recipient_email):
    api_key = os.getenv("MAILGUN_API_KEY")
    domain = os.getenv("MAILGUN_SENDER_DOMAIN")
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": f"Excited User <postmaster@{domain}>",
            "to": recipient_email,
            "subject": subject,
            "text": message,
        },
    )
