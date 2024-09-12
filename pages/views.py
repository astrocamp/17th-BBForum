import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Exists, OuterRef
from django.shortcuts import render
from django.utils import timezone

from articles.models import Article, IndustryTag
from follows.models import FollowRelation
from userprofiles.models import Profile


def get_or_create_profile(user):
    """Helper function to get or create user profile and update login points."""
    profile, created = Profile.objects.get_or_create(user=user)
    today = timezone.now().date()
    if profile.last_login_date != today:
        profile.tot_point += 1
        profile.last_login_date = today
        profile.save()
    return profile


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
    user = req.user
    if user.is_authenticated:
        # 確保 Profile 對象存在並更新點數
        profile = get_or_create_profile(user)
        # 將點數存儲在 session 中
        req.session["points"] = json.dumps(profile.tot_point, cls=DjangoJSONEncoder)

    if req.method == "POST":
        article_content = req.POST.get("article_content")
        if article_content:
            # 創建並保存新的文章
            article = Article(content=article_content, user=user)
            article.save()

            # 處理標籤
            tags = req.POST.get("tags")
            if tags:
                handle_article_tags(article, tags)

            # 更新並返回文章列表 (for HTMX requests)
            articles = get_articles_with_like_info(req.user)
            if req.headers.get("HX-Request"):
                return render(
                    req, "pages/main_page/_articles_list.html", {"articles": articles}
                )
        else:
            # 沒有提交文章內容，返回現有的文章列表
            articles = Article.objects.order_by("-id")
            return render(
                req, "pages/main_page/_articles_list.html", {"articles": articles}
            )

    # Get articles with like and stock information
    articles = get_articles_with_like_info(req.user)

    return render(req, "pages/main_page/index.html", {"articles": articles})


def get_articles_with_like_info(user):
    """Helper function to get articles annotated with like info."""
    subquery = Article.objects.filter(liked=user.pk, id=OuterRef("pk")).values("pk")
    articles = (
        Article.objects.annotate(user_liked=Exists(subquery), like_count=Count("liked"))
        .order_by("-id")
        .prefetch_related("stock")
    )
    return articles


def my_watchlist(req):
    return render(req, "pages/my_watchlist/my_watchlist.html")


def my_favorites(req):
    return render(req, "pages/my_favorites/my_favorites.html")


def news_feed(req):
    following_all_id = FollowRelation.objects.filter(follower=req.user).values_list(
        "following_id", flat=True
    )
    articles = Article.objects.filter(user_id__in=following_all_id).order_by("-id")
    return render(req, "pages/news_feed/news_feed.html", {"articles": articles})


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
