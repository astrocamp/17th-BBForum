from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import QueryDict
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render

from .forms import ArticleForm
from .models import Article, Comment


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


@login_required
def show(req, id):
    post = get_object_or_404(Article, pk=id)
    if req.method == "POST":
        forms = ArticleForm(req.POST, instance=post)
        if forms.is_valid():
            forms.save()
            return redirect("pages:index")
        else:
            return render(req, "articles/edit.html", {"forms": forms, "post": post})

    return render(req, "articles/show.html", {"post": post})


@login_required
def new(req):
    form = ArticleForm()
    return render(req, "articles/new.html", {"form": form})


@login_required
def edit(req, id):
    article = get_object_or_404(Article, pk=id)
    if req.method == "POST":
        new_article = req.POST.get("content")
        if new_article:
            article.content = new_article
            article.user = req.user
            article.save()
    return HttpResponse("")


@login_required
def delete_artile(req, id):
    if req.method == "POST":
        artile = get_object_or_404(Article, id=id, user=req.user)
        artile.delete()
    return redirect("pages:index")


@login_required
def comment(req, id):
    if req.method == "POST":
        article = get_object_or_404(Article, pk=id)
        article.comments.create(
            content=req.POST["content"],
            user=req.user,
        )

        if req.headers.get("HX-Request"):
            return render(req, "pages/main_page/_comment.html", {"article": article})

    articles = Article.objects.order_by("-id")
    return render(req, "pages/main_page/index.html", {"articles": articles})


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


@login_required
def liked(req, id):
    if req.method == "POST":
        # 判斷是否收藏過
        article = get_object_or_404(Article, pk=id)
        if article.liked_by(req.user):
            article.liked.remove(req.user)
            article.like_count = article.liked.count()
            return render(
                req,
                "articles/_liked.html",
                {"article": article, "liked": False},
            )
        else:
            article.liked.add(req.user)
            article.like_count = article.liked.count()
            return render(
                req,
                "articles/_liked.html",
                {"article": article, "liked": True},
            )
