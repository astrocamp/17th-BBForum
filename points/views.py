import json
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from articles.models import Article
from userprofiles.models import Profile


#  顯示用戶的點數
def show_profile(request):
    user = request.user
    tot_point = 0
    if user.is_authenticated:
        profile = Profile.objects.get(user=user)  # 獲取當前用戶的 Profile
        tot_point = profile.tot_point  # 獲取點數

    # 將點數傳遞到模板中
    return render(
        request, "pages/main_page/_left_nav_bar.html", {"tot_point": tot_point}
    )


@login_required
def register_points(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    tot_point = profile.tot_point
    return render(
        request, "pages/main_page/_left_nav_bar.html", {"tot_point": tot_point}
    )


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def register_points_pipeline(strategy, details, user=None, *args, **kwargs):
    if user:
        request = strategy.request
        today = timezone.now().date()
        profile, created = Profile.objects.get_or_create(user=user)

        if profile.last_login_date != today:
            profile.tot_point += 1
            profile.last_login_date = today
            profile.save()

        request.session["points"] = json.dumps(profile.tot_point, cls=CustomJSONEncoder)


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
                profile.tot_point += 2  # 增加點數
                profile.save()  # 確保保存更新

                request.session["points"] = json.dumps(
                    profile.tot_point, cls=DjangoJSONEncoder
                )

                return JsonResponse({"success": True, "tot_point": profile.tot_point})
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "今天已經發佈了五篇文章，無法再獲得點數。",
                    }
                )

    return JsonResponse({"success": False, "error": "Invalid request."})
