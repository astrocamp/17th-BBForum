import json

from django.db.models import Count, Exists, OuterRef, Value
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Case, Count, Exists, OuterRef, Subquery, Value, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from articles.models import Article, IndustryTag
from follows.models import FollowRelation
from lib.auth.group import update_user_group
from picks.models import UserStock
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
            # 發文更新使用者階級
            update_user_group(req.user)
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

            group_name_subquery = Group.objects.filter(
                user__id=OuterRef("user_id")
            ).values("name")[:1]
            articles = Article.objects.annotate(
                user_liked=Exists(subquery),
                like_count=Count("liked"),
                group_name=Subquery(group_name_subquery),
            ).order_by("-id")

            # 更新所有使用者階級
            users = User.objects.all()
            for user in users:
                update_user_group(user)

            if req.headers.get("HX-Request"):
                return render(
                    req,
                    "pages/main_page/_articles_list.html",
                    {
                        "articles": articles,
                    },
                )

        else:
            articles = Article.objects.order_by("-id")
            return render(
                req, "pages/main_page/_articles_list.html", {"articles": articles}
            )

    subquery = Article.objects.filter(liked=req.user.pk, id=OuterRef("pk")).values("pk")
    collect = Article.objects.filter(collectors=req.user.pk, id=OuterRef("pk")).values(
        "pk"
    )
    group_name_subquery = Group.objects.filter(user__id=OuterRef("user_id")).values(
        "name"
    )[:1]
    articles = (
        Article.objects.annotate(
            user_liked=Exists(subquery),
            like_count=Count("liked"),
            collect=Exists(collect),
            group_name=Subquery(group_name_subquery),
        )
        .select_related("user__profile")
        .order_by("-id")
        .prefetch_related("stock")
    )
    stocks = IndustryTag.objects.all()

    if req.user.is_authenticated:
        update_user_group(req.user)
        users = User.objects.all()
        for user in users:
            update_user_group(user)

    if req.user.is_authenticated:
        profile = get_object_or_404(Profile, user=req.user)
        user_img = profile.user_img
    else:
        user_img = None

    return render(
        req,
        "pages/main_page/index.html",
        {
            "articles": articles,
            "stocks": stocks,
            "user_img": user_img,
        },
    )


def my_watchlist(req):
    stock_all_id = UserStock.objects.filter(user=req.user).values_list(
        "stock_id", flat=True
    )
    group_name_subquery = Group.objects.filter(user__id=OuterRef("user_id")).values(
        "name"
    )[:1]
    articles = (
        Article.objects.filter(stock__in=stock_all_id)
        .distinct()
        .order_by("-id")
        .annotate(group_name=Subquery(group_name_subquery))
    )

    if req.user.is_authenticated:
        profile = get_object_or_404(Profile, user=req.user)
        user_img = profile.user_img
    else:
        user_img = None

    return render(
        req,
        "pages/my_watchlist/my_watchlist.html",
        {
            "articles": articles,
            "user_img": user_img,
        },
    )


def my_favorites(req):
    user = req.user
    subquery = Article.objects.filter(liked=req.user.pk, id=OuterRef("pk")).values("pk")

    group_name_subquery = Group.objects.filter(user__id=OuterRef("user_id")).values(
        "name"
    )[:1]
    favorite_articles = Article.objects.filter(collectors=user).annotate(
        collect=Value(True),
        user_liked=Exists(subquery),
        like_count=Count("liked"),
        group_name=Subquery(group_name_subquery),
    )
    if req.user.is_authenticated:
        profile = get_object_or_404(Profile, user=req.user)
        user_img = profile.user_img
    else:
        user_img = None

    return render(
        req,
        "pages/my_favorites/my_favorites.html",
        {
            "favorite_articles": favorite_articles,
            "user_img": user_img,
        },
    )


def news_feed(req):
    following_all_id = FollowRelation.objects.filter(follower=req.user).values_list(
        "following_id", flat=True
    )

    group_name_subquery = Group.objects.filter(user__id=OuterRef("user_id")).values(
        "name"
    )[:1]
    articles = (
        Article.objects.filter(user_id__in=following_all_id)
        .order_by("-id")
        .annotate(group_name=Subquery(group_name_subquery))
    )

    if req.user.is_authenticated:
        profile = get_object_or_404(Profile, user=req.user)
        user_img = profile.user_img
    else:
        user_img = None

    return render(
        req,
        "pages/news_feed/news_feed.html",
        {
            "articles": articles,
            "user_img": user_img,
        },
    )


def market_index(req):

    if req.user.is_authenticated:
        profile = get_object_or_404(Profile, user=req.user)
        user_img = profile.user_img
    else:
        user_img = None

    return render(
        req,
        "pages/market_index/market_index.html",
        {"user_img": user_img},
    )


def taiwan_index(req):
    if req.user.is_authenticated:
        profile = get_object_or_404(Profile, user=req.user)
        user_img = profile.user_img
    else:
        user_img = None

    return render(
        req,
        "pages/taiwan_index/taiwan_index.html",
        {"user_img": user_img},
    )


def member_profile(req):
    return render(req, "pages/nav_page/member_profile.html")


def popular_stocks(req):
    if req.user.is_authenticated:
        profile = get_object_or_404(Profile, user=req.user)
        user_img = profile.user_img
    else:
        user_img = None
    return render(req, "popular_pages/popular_stocks.html", {"user_img": user_img})


def popular_students(req):
    if req.user.is_authenticated:
        profile = get_object_or_404(Profile, user=req.user)
        user_img = profile.user_img
    else:
        user_img = None

    return render(req, "popular_pages/popular_students.html", {"user_img": user_img})


def popular_answers(req):
    if req.user.is_authenticated:
        profile = get_object_or_404(Profile, user=req.user)
        user_img = profile.user_img
    else:
        user_img = None

    return render(req, "popular_pages/popular_answers.html", {"user_img": user_img})


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
def points(request):
    return render(request, "layouts/base.html")


def update_left_nav_bar(req):
    current_user_groups = list(req.user.groups.values_list("name", flat=True))

    return JsonResponse(
        {
            "current_user_groups": current_user_groups,
        }
    )
