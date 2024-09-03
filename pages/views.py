from django.shortcuts import render


# Create your views here.
def index(req):
    return render(req, "pages/main_page/index.html")


def my_watchlist(req):
    return render(req, "pages/my_watchlist/my_watchlist.html")


def member_profile(req):
    return render(req, "pages/nav_page/member_profile.html")
