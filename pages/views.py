import json
from datetime import datetime

from django.contrib.auth.models import AnonymousUser
from django.db.models import Count, Exists, OuterRef, Value
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from articles.models import Article, IndustryTag
from follows.models import FollowRelation
from picks.models import UserStock
from stockpages.stockdash import get_stock_data
from userprofiles.models import Profile


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

    if isinstance(req.user, AnonymousUser):
        pick_stocks = []
    else:
        pick_stocks = UserStock.objects.filter(user=req.user).values_list(
            "stock__security_code", flat=True
        )

    if isinstance(req.user, AnonymousUser):
        pick_stocks = []
    else:
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
        .select_related("user__profile")
        .order_by("-id")
        .prefetch_related("stock")
    )

    stocks = IndustryTag.objects.all()

    for article in articles:
        article.follower_count = article.user.followers.count()

    return render(
        req,
        "pages/main_page/index.html",
        {"articles": articles, "stocks": stocks, "random_five_tags": random_five_tags},
    )


def my_watchlist(req):
    if isinstance(req.user, AnonymousUser):
        pick_stocks = []
    else:
        pick_stocks = UserStock.objects.filter(user=req.user).values_list(
            "stock__security_code", flat=True
        )

    random_five_tags = (
        IndustryTag.objects.filter(industry="半導體業")
        .exclude(security_code__in=pick_stocks)
        .values_list("security_code", "name")
        .order_by("?")[:5]
    )

    stock_all_id = UserStock.objects.filter(user=req.user).values_list(
        "stock_id", flat=True
    )

    stock_data_list = []

    for stock_id in stock_all_id:
        latest_price, percent_change, price_change, trading_units = get_stock_data(
            stock_id
        )
        stock_name = (
            IndustryTag.objects.filter(security_code=stock_id)
            .values_list("name", flat=True)
            .first()
        )
        stock_data_list.append(
            {
                "stock_id": stock_id,
                "stock_name": stock_name,
                "latest_price": latest_price,
                "percent_change": percent_change,
                "price_change": price_change,
                "trading_units": trading_units,
            }
        )

    current_time = datetime.now().strftime("%m/%d %H:%M")

    subquery = Article.objects.filter(liked=req.user.pk, id=OuterRef("pk")).values("pk")

    articles = (
        Article.objects.filter(stock__in=stock_all_id)
        .annotate(user_liked=Exists(subquery), like_count=Count("liked"))
        .distinct()
        .order_by("-id")
        .prefetch_related("stock")
    )

    for article in articles:
        article.follower_count = article.user.followers.count()

    return render(
        req,
        "pages/my_watchlist/my_watchlist.html",
        {
            "articles": articles,
            "random_five_tags": random_five_tags,
            "current_time": current_time,
            "stock_data_list": stock_data_list,
        },
    )


def my_favorites(req):
    user = req.user
    subquery = Article.objects.filter(liked=req.user.pk, id=OuterRef("pk")).values("pk")
    favorite_articles = Article.objects.filter(collectors=user).annotate(
        collect=Value(True),
        user_liked=Exists(subquery),
        like_count=Count("liked"),
    )

    follower_count = user.followers.count()
    following_count = user.following.count()

    for favorite_article in favorite_articles:
        favorite_article.follower_count = favorite_article.user.followers.count()

    return render(
        req,
        "pages/my_favorites/my_favorites.html",
        {
            "favorite_articles": favorite_articles,
            "follower_count": follower_count,
            "following_count": following_count,
        },
    )


def news_feed(req):
    following_all_id = FollowRelation.objects.filter(follower=req.user).values_list(
        "following_id", flat=True
    )
    articles = Article.objects.filter(user_id__in=following_all_id).order_by("-id")

    if req.user.is_authenticated:
        profile = get_object_or_404(Profile, user=req.user)
        user_img = profile.user_img
    else:
        user_img = None

    subquery = Article.objects.filter(liked=req.user.pk, id=OuterRef("pk")).values("pk")

    articles = (
        Article.objects.filter(user_id__in=following_all_id)
        .annotate(user_liked=Exists(subquery), like_count=Count("liked"))
        .order_by("-id")
    )

    for article in articles:
        article.follower_count = article.user.followers.count()

    return render(
        req,
        "pages/news_feed/news_feed.html",
        {"articles": articles, "user_img": user_img},
    )


def market_index(req):

    if isinstance(req.user, AnonymousUser):
        pick_stocks = []
    else:
        pick_stocks = UserStock.objects.filter(user=req.user).values_list(
            "stock__security_code", flat=True
        )

    random_five_tags = (
        IndustryTag.objects.filter(industry="半導體業")
        .exclude(security_code__in=pick_stocks)
        .values_list("security_code", "name")
        .order_by("?")[:5]
    )

    return render(
        req,
        "pages/market_index/market_index.html",
        {"random_five_tags": random_five_tags},
    )


def taiwan_index(req):

    if isinstance(req.user, AnonymousUser):
        pick_stocks = []
    else:
        pick_stocks = UserStock.objects.filter(user=req.user).values_list(
            "stock__security_code", flat=True
        )

    random_five_tags = (
        IndustryTag.objects.filter(industry="半導體業")
        .exclude(security_code__in=pick_stocks)
        .values_list("security_code", "name")
        .order_by("?")[:5]
    )

    return render(
        req,
        "pages/taiwan_index/taiwan_index.html",
        {"random_five_tags": random_five_tags},
    )


def member_profile(req):
    return render(req, "pages/nav_page/member_profile.html")


def popular_stocks(req):
    return render(req, "popular_pages/popular_stocks.html")


def popular_students(request):
    return render(request, "popular_pages/popular_students.html")


def popular_answers(req):
    return render(req, "popular_pages/popular_answers.html")


def points(req):
    return render(req, "layouts/base.html")


def search_stocks(req):
    query = req.GET.get("q", "")
    results = IndustryTag.objects.filter(
        name__icontains=query
    ) | IndustryTag.objects.filter(security_code__icontains=query)
    suggestions = [
        {"security_code": stock.security_code, "name": stock.name} for stock in results
    ]
    return JsonResponse(suggestions, safe=False)


def stock_notfound(req):
    return render(req, "pages/taiwan_index/stock_notfound.html")
