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
