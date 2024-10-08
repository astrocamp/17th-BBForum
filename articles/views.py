from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render

from userprofiles.models import Profile

from .forms import ArticleForm
from .models import Article, Comment, IndustryTag


@login_required
def show(req, id):
    article = get_object_or_404(Article, pk=id)
    article.like_count = article.liked.count()
    user_liked = False
    if req.user.is_authenticated:
        user_liked = article.liked.filter(id=req.user.id).exists()
    article.user_liked = user_liked

    if req.user.is_authenticated:
        profile = get_object_or_404(Profile, user=req.user)
        user_img = profile.user_img
    else:
        user_img = None

    return render(
        req,
        "articles/show.html",
        {"article": article, "user_img": user_img},
    )


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
    if req.method == "DELETE":
        artile = get_object_or_404(Article, id=id, user=req.user)
        print(artile)
        artile.delete()
    return HttpResponse("")


@login_required
def comment(req, id):
    if req.method == "POST":
        article = get_object_or_404(Article, pk=id)
        article.comments.create(
            content=req.POST["content"],
            user=req.user,
        )

        if req.headers.get("HX-Request"):
            return render(
                req,
                "articles/_comment.html",
                {"article": article},
            )

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


def stocks_list(request):

    query = request.GET.get("q", "")

    if query:
        tags = IndustryTag.objects.filter(name__icontains=query).values(
            "security_code", "name"
        )
    else:
        tags = IndustryTag.objects.all().values("security_code", "name")

    tags_list = [{"value": tag["name"], "id": tag["security_code"]} for tag in tags]

    return JsonResponse(tags_list, safe=False)


@login_required
def collectors(req, id):

    article = get_object_or_404(Article, pk=id)

    if req.method == "POST":
        if article.collected_by(req.user):
            article.collectors.remove(req.user)
            collected_status = False
        else:
            article.collectors.add(req.user)
            collected_status = True

        return render(
            req,
            "articles/_collectors.html",
            {"article": article, "collected": collected_status},
        )
