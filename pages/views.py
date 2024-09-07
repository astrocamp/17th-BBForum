from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from articles.forms import ArticleForm
from articles.models import Article


# Create your views here.
def index(req):
    if req.method == "POST":
        content = req.POST.get("content")
        if content:
            articles = Article(content=content)
            articles.user = req.user
            articles.save()

            articles = Article.objects.order_by("-id")
            return render(req, "pages/main_page/index.html", {"articles": articles})

    articles = Article.objects.order_by("-id")
    return render(req, "pages/main_page/index.html", {"articles": articles})


def my_watchlist(req):
    return render(req, "pages/my_watchlist/my_watchlist.html")


def my_favorites(req):
    return render(req, "pages/my_favorites/my_favorites.html")


def news_feed(req):
    return render(req, "pages/news_feed/news_feed.html")


def market_index(req):
    return render(req, "pages/market_index/market_index.html")


def taiwan_index(req):
    return render(req, "pages/taiwan_index/taiwan_index.html")


def member_profile(req):
    return render(req, "pages/nav_page/member_profile.html")


def popular_stocks(request):
    return render(request, "popular_pages/popular_stocks.html")


def popular_students(request):
    return render(request, "popular_pages/popular_students.html")


def popular_answers(request):
    return render(request, "popular_pages/popular_answers.html")


def points(request):
    return render(request, "layouts/base.html")
