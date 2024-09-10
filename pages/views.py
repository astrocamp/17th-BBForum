import json

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Exists, OuterRef
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from articles.models import Article, IndustryTag


def index(req):
    if req.method == "POST":
        article_content = req.POST.get("article_content")
        if article_content:
            # 創建並保存新的文章
            article = Article(content=article_content)
            article.user = req.user
            article.save()

            # 處理標籤
            tags = req.POST.get("tags")
            if tags:
                try:
                    tags_list = json.loads(tags)
                    tag_ids = [tag.get("id") for tag in tags_list]
                    industry_tags = IndustryTag.objects.filter(
                        security_code__in=tag_ids
                    )
                    article.stock.set(industry_tags)
                    article.save()
                except json.JSONDecodeError:
                    print("Failed to decode JSON from tags.")

            subquery = Article.objects.filter(
                liked=req.user.pk, id=OuterRef("pk")
            ).values("pk")

            articles = Article.objects.annotate(
                user_liked=Exists(subquery), like_count=Count("liked")
            ).order_by("-id")

            if req.headers.get("HX-Request"):
                return render(
                    req, "pages/main_page/_articles_list.html", {"articles": articles}
                )

    subquery = Article.objects.filter(liked=req.user.pk, id=OuterRef("pk")).values("pk")

    articles = (
        Article.objects.annotate(user_liked=Exists(subquery), like_count=Count("liked"))
        .order_by("-id")
        .prefetch_related("stock")
    )

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
