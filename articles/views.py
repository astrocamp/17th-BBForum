from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import QueryDict
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import ArticleForm
from .models import Article, Comment

# Create your views here.


def index(req):
    if req.method == "POST":
        article_content = req.POST.get("content")

        if article_content:
            articles = Article(content=article_content)
            articles.userID = req.user
            articles.save()

            articles = Article.objects.order_by("-id")
            return render(req, "pages/main_page/index.html", {"articles": articles})

    articles = Article.objects.all()
    return render(req, "pages/main_page/index.html", {"articles": articles})

    # article = get_object_or_404(Article, pk=id)
    # article = article.comments.create(
    #     content=req.POST["content"],
    #     user=req.user,
    # )
    # articles = Article.objects.order_by("-id")
    # return render(
    #     req,
    #     "pages/main_page/index.html",
    #     {"articles": articles, "article": article},
    # )

    # form = ArticleForm(req.POST, req.FILES)
    # # 表單中有文件上傳，應該使用 req.FILES
    # if form.is_valid():
    #     # 使用 request.user 來獲取當前登入的使用者
    #     user = req.user
    #     # 避免不必要的數據庫操作：保存表單數據但不提交到數據庫
    #     article = form.save(commit=False)
    #     article.userID = user  # 設置 user 字段
    #     article.post_at = timezone.now()  # 設置創建時間
    #     article.save()  # 保存到數據庫

    #     return redirect(reverse("articles:index"))
    # else:
    #     return render(req, "articles/new.html", {"form": form})
    # posts = Article.objects.order_by("-id")

    # return render(req, "articles/index.html", {"posts": posts})


@login_required
def show(req, id):
    post = get_object_or_404(Article, pk=id)

    if req.method == "POST":
        forms = ArticleForm(req.POST, instance=post)  # 確保包含 req.FILES
        if forms.is_valid():
            forms.save()
            return redirect("pages:index")
            # return redirect(
            #     reverse("articles:show", kwargs={"id": post.id})
            # )  # 更新後重定向
        else:
            return render(
                req, "articles/edit.html", {"forms": forms, "post": post}
            )  # 如果表單無效，重新顯示編輯頁面

    return render(req, "articles/show.html", {"post": post})


@login_required
def new(req):
    form = ArticleForm()
    return render(req, "articles/new.html", {"form": form})


@login_required
def edit(req, id):
    posts = get_object_or_404(Article, pk=id)
    if req.method == "POST":
        forms = ArticleForm(req.POST, instance=posts)
        if forms.is_valid():
            forms.save()
            # 使用 reverse 生成 URL 並傳遞 id 參數
            # return redirect(reverse("articles:edit", args=[post.id]))
            return render(req, "pages/main_page/index.html", {"forms": forms})
    else:
        forms = ArticleForm(instance=posts)
        return render(
            req, "layouts/edit_article.html", {"forms": forms, "posts": posts}
        )


@login_required
def delete(req, id):
    post = get_object_or_404(Article, pk=id)
    post.delete()
    return redirect("pages:index")


@login_required
def comment(req, id):
    if req.method == "POST":
        article = get_object_or_404(Article, pk=id)
        article = article.comments.create(
            content=req.POST["content"],
            user=req.user,
        )
        return redirect("pages:index")


@login_required
def delete_comment(req, id):
    if req.method == "DELETE":
        comment = get_object_or_404(Comment, id=id, user=req.user)
        comment.delete()
        return HttpResponse("")


@login_required
def update_comment(req, id):
    if req.method == "POST":
        comment = get_object_or_404(Comment, id=id, user=req.user)
        new_content = req.POST["content"]
        if new_content:
            comment.content = new_content
            comment.save()
        return HttpResponse("")
