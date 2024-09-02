from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import ArticleForm
from .models import Article

# Create your views here.


def index(req):
    if req.method == "POST":
        form = ArticleForm(req.POST, req.FILES)
        # 注意如果表單中有文件上傳，應該使用 req.FILES
        if form.is_valid():
            # 使用 request.user 來獲取當前登入的使用者
            user = req.user
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


@login_required
def show(req, id):
    post = get_object_or_404(Article, pk=id)

    if req.method == "POST":
        form = ArticleForm(req.POST, req.FILES, instance=post)  # 確保包含 req.FILES
        if form.is_valid():
            form.save()
            return redirect(
                reverse("articles:show", kwargs={"id": post.id})
            )  # 更新後重定向
        else:
            return render(
                req, "articles/edit.html", {"form": form, "post": post}
            )  # 如果表單無效，重新顯示編輯頁面

    return render(req, "articles/show.html", {"post": post})


@login_required
def new(req):
    form = ArticleForm()
    return render(req, "articles/new.html", {"form": form})


@login_required
def edit(req, id):
    post = get_object_or_404(Article, pk=id)
    if req.method == "POST":
        form = ArticleForm(req.POST, req.FILES, instance=post)
        if form.is_valid():
            form.save()
            # 使用 reverse 生成 URL 並傳遞 id 參數
            return redirect(reverse("articles:show", args=[post.id]))
    else:
        form = ArticleForm(instance=post)
    return render(req, "articles/edit.html", {"form": form, "post": post})


@login_required
def delete(req, id):
    post = get_object_or_404(Article, pk=id)
    post.delete()
    return redirect("articles:index")
