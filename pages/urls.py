from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("my_watchlist/", views.my_watchlist, name="my_watchlist"),
    path("member_profile/", views.member_profile, name="member_profile"),
    path("member_points/", views.member_points, name="member_points"),
    path("my_favorites/", views.my_favorites, name="my_favorites"),
    path("news_feed/", views.news_feed, name="news_feed"),
    path("market_index/", views.market_index, name="market_index"),
    path("taiwan_index/", views.taiwan_index, name="taiwan_index"),
    path("member_profile/", views.member_profile, name="member_profile"),
    path("member_points/", views.member_points, name="member_points"),
    path("popular_stocks/", views.popular_stocks, name="popular_stocks"),
    path("popular_students/", views.popular_students, name="popular_students"),
    path("popular_answers/", views.popular_answers, name="popular_answers"),
]
