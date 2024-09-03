# views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

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
    return render(req, "users/register.html", {"form": UserCreationForm()})


def sign_in(req):
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(req, user)
            messages.success(req, "登入成功")
            return redirect("pages:index")
        else:
            messages.error(req, "登入失敗")
            return render(req, "users/login.html")  # 保留用戶輸入
    return render(req, "users/login.html")


def sign_out(req):
    if req.method == "POST":
        logout(req)
        messages.success(req, "登出成功")
        return redirect("pages:index")
    return redirect("pages:index")


def auth_denied(req):
    return render(req, "users/auth_denied.html")
