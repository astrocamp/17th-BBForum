import json
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from articles.models import Article
from userprofiles.models import Profile


@login_required
def show_profile(request):
    profile = request.user.profile
    return render(
        request, "pages/main_page/_left_nav_bar.html", {"tot_point": profile.tot_point}
    )


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


@login_required
def give_initial_points(sender, request, user, **kwargs):
    profile, created = Profile.objects.get_or_create(user=user)
    if created:
        profile.add_points()


@login_required
def create_article(request):
    user = request.user
    if request.method == "POST":
        article_content = request.POST.get("article_content")
        if article_content:
            today = timezone.now().date()
            article_count_today = Article.objects.filter(
                user=user, created_at__date=today
            ).count()

            if article_count_today < 5:
                article = Article(content=article_content, user=user)
                article.save()

                profile, created = Profile.objects.get_or_create(user=user)
                profile.add_points()
                profile.save()

                return JsonResponse({"success": True, "tot_point": profile.tot_point})

            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "今天已經發佈了五篇文章，無法再獲得點數。",
                    }
                )

    return JsonResponse({"success": False, "error": "Invalid request."})


@login_required
def get_user_points(request):
    if request.user.is_authenticated:
        points = request.user.profile.tot_point
        return JsonResponse({"tot_point": points})
    return JsonResponse({"tot_point": 0})
