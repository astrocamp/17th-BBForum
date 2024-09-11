from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.http import JsonResponse
=======
from django.contrib.auth.models import User
<<<<<<< HEAD
from django.db.models import Count
from django.http import JsonResponse, QueryDict
>>>>>>> 4d38ea1 (feat: 增加貼文收藏功能)
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render

from .forms import ArticleForm
from .models import Article, Comment, IndustryTag
=======


from django.urls import reverse
from django.utils import timezone





# Create your views here.
>>>>>>> b2beded (feat: 增加貼文收藏功能)


@login_required
def show(req, id):
    article = get_object_or_404(Article, pk=id)
    if req.method == "POST":
        forms = ArticleForm(req.POST, instance=article)
        if forms.is_valid():
            forms.save()
            return redirect("pages:index")
        else:
            return render(
                req, "articles/edit.html", {"forms": forms, "article": article}
            )

    return render(req, "articles/show.html", {"article": article})


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
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def collect_article(request, article_id):
    try:

        article = Article.objects.get(id=article_id)
        user = request.user

        if user in article.collectors.all():
            return Response(
                {"success": False, "message": "Article already collected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        article.collectors.add(user)
        article.save()

        serializer = ArticleSerializer(article)
        return Response(
            {"success": True, "article": serializer.data}, status=status.HTTP_200_OK
        )

    except Article.DoesNotExist:
        return Response(
            {"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:

        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_collect_article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        user = request.user

        if user in article.collectors.all():
            article.collectors.remove(user)
            article.save()
            serializer = ArticleSerializer(article)
            return Response(
                {"success": True, "article": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"success": False, "message": "Article not collected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Article.DoesNotExist:
        return Response(
            {"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:

        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def collect_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.is_collected = True
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(
            {"success": True, "comment": serializer.data}, status=status.HTTP_200_OK
        )
    except Comment.DoesNotExist:
        return Response(
            {"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_collect_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.is_collected = False
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(
            {"success": True, "comment": serializer.data}, status=status.HTTP_200_OK
        )
    except Comment.DoesNotExist:
        return Response(
            {"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
        )
