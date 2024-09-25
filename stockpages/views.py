from datetime import datetime

from django.db.models import Count, Exists, OuterRef
from django.shortcuts import get_object_or_404, render

from articles.models import Article, IndustryTag
from userprofiles.models import Profile

from .stockdash import get_stock_data


def stock_data_twii(req):
    latest_price, percent_change, price_change, trading_units = get_stock_data("^TWII")
    current_time = datetime.now().strftime("%m/%d %H:%M")

    if req.user.is_authenticated:
        profile = get_object_or_404(Profile, user=req.user)
        user_img = profile.user_img
    else:
        user_img = None

    subquery = Article.objects.filter(liked=req.user.pk, id=OuterRef("pk")).values("pk")

    articles = (
        Article.objects.filter(stock__isnull=False)
        .distinct()
        .annotate(user_liked=Exists(subquery), like_count=Count("liked"))
        .distinct()
        .order_by("-id")
        .prefetch_related("stock")
    )

    for article in articles:
        article.follower_count = article.user.followers.count()

    return render(
        req,
        "pages/market_index/market_index.html",
        {
            "stock": "加權指數",
            "security_code": "TWA00",
            "latest_price": latest_price,
            "percent_change": percent_change,
            "current_time": current_time,
            "twii": True,
            "user_img": user_img,
            "articles": articles,
        },
    )


def stock_data(req, id):
    stock = get_object_or_404(IndustryTag, security_code=id)
    subquery = Article.objects.filter(liked=req.user.pk, id=OuterRef("pk")).values("pk")

    articles = (
        Article.objects.filter(stock=id)
        .distinct()
        .annotate(user_liked=Exists(subquery), like_count=Count("liked"))
        .distinct()
        .order_by("-id")
        .prefetch_related("stock")
    )

    latest_price, percent_change, price_change, trading_units = get_stock_data(id)
    current_time = datetime.now().strftime("%m/%d %H:%M")

    for article in articles:
        article.follower_count = article.user.followers.count()

    return render(
        req,
        "pages/market_index/market_index.html",
        {
            "stock": stock,
            "articles": articles,
            "latest_price": latest_price,
            "percent_change": percent_change,
            "current_time": current_time,
        },
    )
