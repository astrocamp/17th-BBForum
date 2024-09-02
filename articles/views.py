from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate
from .forms import ArticleForm
from .models import Article
from django.contrib.auth.models import User
from django.utils import timezone

# Create your views here.


def index(req):
    if req.method == "POST":
       form = ArticleForm(req.POST, req.FILES)  
       # 注意如果表單中有文件上傳，應該使用 req.FILES
       if form.is_valid():
            user = get_object_or_404(User, id=1)            
            # 避免不必要的數據庫操作：保存表單數據但不提交到數據庫
            article = form.save(commit=False)
            article.userID = user  # 設置 user 字段
            article.post_at = timezone.now()  # 設置創建時間            
            article.save()  # 保存到數據庫
            
            return redirect(reverse("articles:index"))
    else:
        return render(req, "articles/new.html", {"form": form})
    posts = Article.objects.order_by("-id")
    return render(req, "articles/index.html", {"posts": posts})


def show(req, id):
    post = get_object_or_404(Article, pk=id)
    if req.method == "POST":
        form = ArticleForm(req.POST, instance=post)
        if form.is_valid():
            form.save()
        else:
            return render(req, "articles/edit.html", {"form": form, "post": post})
    return render(req, "articles/show.html", {"post": post})


def new(req):
    form = ArticleForm()
    return render(req, "articles/new.html", {"form": form})


def edit(req, id):
    post = get_object_or_404(Article, pk=id)
    form = ArticleForm(instance=post)
    return render(req, "articles/edit.html", {"form": form, "post": post})


def delete(req, id):
    post = get_object_or_404(Article, pk=id)
    post.delete()
    return redirect("articles:index")
