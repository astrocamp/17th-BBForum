from django.db.models import Case, Count, Exists, OuterRef, Value, When
from django.shortcuts import get_object_or_404, render

from articles.models import Article
from follows.models import FollowRelation
from userprofiles.models import Profile


def popular_stocks(request):

    return render(request, "popular_pages/popular_stocks/popular_stocks.html")


def popular_students(req):
    follow_counts = (
        FollowRelation.objects.values("following")
        .annotate(follower_count=Count("follower"))
        .order_by("-follower_count")
    )

    unique_counts = []
    for follow in follow_counts:
        if follow["follower_count"] not in unique_counts:
            unique_counts.append(follow["follower_count"])

    top_counts = unique_counts[:5]

    top_users = follow_counts.filter(follower_count__in=top_counts)

    if len(top_counts) > 5:
        sixth_count = top_counts[5]
        additional_users = follow_counts.filter(follower_count=sixth_count)
        top_users = list(top_users) + list(additional_users)

    top_user_data = {user["following"]: user["follower_count"] for user in top_users}
    top_user_ids = list(top_user_data.keys())

    subquery = Article.objects.filter(liked=req.user.pk, id=OuterRef("pk")).values("pk")
    collect = Article.objects.filter(collectors=req.user.pk, id=OuterRef("pk")).values(
        "pk"
    )

    articles = (
        Article.objects.filter(user_id__in=top_user_ids)
        .annotate(
            user_liked=Exists(subquery),
            like_count=Count("liked"),
            collect=Exists(collect),
        )
        .annotate(
            follower_count=Case(
                *[
                    When(user_id=user_id, then=Value(follower_count))
                    for user_id, follower_count in top_user_data.items()
                ],
                default=Value(0)
            )
        )
        .order_by("-follower_count")
    )
    return render(
        req,
        "popular_pages/popular_students/popular_students.html",
        {"articles": articles},
    )


def popular_answers(request):

    return render(request, "popular_pages/popular_answers/popular_answers.html")


def base(request):
    return render(request, "base.html")
