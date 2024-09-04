from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render


# Create your views here.
def index(req):
    return render(req, "pages/main_page/index.html")


def my_watchlist(req):
    return render(req, "pages/my_watchlist/my_watchlist.html")


def my_favorites(req):
    return render(req, "pages/my_favorites/my_favorites.html")


def news_feed(req):
    return render(req, "pages/news_feed/news_feed.html")


def market_index(req):
    return render(req, "pages/market_index/market_index.html")


def taiwan_index(req):
    return render(req, "pages/taiwan_index/taiwan_index.html")


def member_profile(req):
    return render(req, "pages/nav_page/member_profile.html")


@login_required
def member_points(request):
    try:
        points = request.user.userprofile.points
    except ObjectDoesNotExist:
        points = 0  # 或者其他默认值

    return render(request, "nav_page/member_points.html", {"points": points})


def popular_stocks(req):
    return render(req, "pages/popular_stocks/popular_stocks.html")


def popular_students(request):
    return render(request, "pages/popular_students/popular_students.html")


def popular_answers(request):
    return render(request, "pages/popular_answers/popular_answers.html")
