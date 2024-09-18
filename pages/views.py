import json

from django.db.models import Count, Exists, OuterRef, Value
from django.shortcuts import render

from articles.models import Article, IndustryTag
from follows.models import FollowRelation
from picks.models import UserStock


def handle_article_tags(article, tags):
    try:
        tags_list = json.loads(tags)
        tag_ids = [tag.get("id") for tag in tags_list]
        industry_tags = IndustryTag.objects.filter(security_code__in=tag_ids)
        article.stock.set(industry_tags)
        article.save()
    except json.JSONDecodeError:
        print("Failed to decode JSON from tags.")


def index(req):
    if req.method == "POST":
        article_content = req.POST.get("article_content")
        photo = req.FILES.get("photo")

        if article_content:
            article = Article(content=article_content)
            article.user = req.user
            article.photo = photo
            article.save()
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
            stocks = IndustryTag.objects.all()

            if req.headers.get("HX-Request"):
                return render(
                    req,
                    "pages/main_page/_articles_list.html",
                    {"articles": articles, "stocks": stocks},
                )
        else:
            articles = Article.objects.order_by("-id")
            return render(
                req, "pages/main_page/_articles_list.html", {"articles": articles}
            )

    pick_stocks = UserStock.objects.filter(user=req.user).values_list(
        "stock__security_code", flat=True
    )

    random_five_tags = (
        IndustryTag.objects.filter(industry="半導體業")
        .exclude(security_code__in=pick_stocks)
        .values_list("security_code", "name")
        .order_by("?")[:5]
    )

    subquery = Article.objects.filter(liked=req.user.pk, id=OuterRef("pk")).values("pk")
    collect = Article.objects.filter(collectors=req.user.pk, id=OuterRef("pk")).values(
        "pk"
    )

    articles = (
        Article.objects.annotate(
            user_liked=Exists(subquery),
            like_count=Count("liked"),
            collect=Exists(collect),
        )
        .order_by("-id")
        .prefetch_related("stock")
    )
    return render(
        req,
        "pages/main_page/index.html",
        {"articles": articles, "random_five_tags": random_five_tags},
    )


def my_watchlist(req):
    stock_all_id = UserStock.objects.filter(user=req.user).values_list(
        "stock_id", flat=True
    )
    articles = Article.objects.filter(stock__in=stock_all_id).distinct().order_by("-id")
    return render(req, "pages/my_watchlist/my_watchlist.html", {"articles": articles})


def my_favorites(req):
    user = req.user
    subquery = Article.objects.filter(liked=req.user.pk, id=OuterRef("pk")).values("pk")
    favorite_articles = Article.objects.filter(collectors=user).annotate(
        collect=Value(True),
        user_liked=Exists(subquery),
        like_count=Count("liked"),
    )

    return render(
        req,
        "pages/my_favorites/my_favorites.html",
        {
            "favorite_articles": favorite_articles,
        },
    )


def news_feed(req):
    following_all_id = FollowRelation.objects.filter(follower=req.user).values_list(
        "following_id", flat=True
    )
    articles = Article.objects.filter(user_id__in=following_all_id).order_by("-id")
    return render(req, "pages/news_feed/news_feed.html", {"articles": articles})


def stock_market(req):
    return render(req, "pages/stock_market/stock_market.html")


def taiwan_futures(req):
    return render(req, "pages/taiwan_futures/taiwan_futures.html")


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
