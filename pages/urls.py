from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("my_watchlist/", views.my_watchlist, name="my_watchlist"),
    path("my_favorites/", views.my_favorites, name="my_favorites"),
    path("news_feed/", views.news_feed, name="news_feed"),
    path("market_index/", views.market_index, name="market_index"),
    path("taiwan_index/", views.taiwan_index, name="taiwan_index"),
]
