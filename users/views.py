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
            return redirect("users:sign_in")  # 要改
        else:
            return render(req, "users/register.html", {"form": form})
    return render(req, "layouts/base.html")


def register(req):
    return render(req, "users/register.html", {"form": UserCreationForm()})


def sign_in(req):
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(username=username, password=password)  # 用戶驗證
        if user is not None:
            login(req, user)  # 登入
            messages.success(req, "登入成功")
            return redirect("users:index")  # 重定向到主頁或其他頁面
        else:
            messages.error(req, "登入失敗")
            return render(
                req, "users/login.html", {"username": username}
            )  # 保留用戶輸入
    return render(req, "users/login.html")


def sign_out(req):
    if req.method == "POST":
        logout(req)
        messages.success(req, "登出成功")
        return redirect("users:sign_in")  # 登出後重定向到登入頁面
    return redirect("users:index")  # 若不是 POST 請求，重定向到主頁或其他頁面
