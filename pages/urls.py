from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("my_watchlist/", views.my_watchlist, name="my_watchlist"),
    path("my_favorites/", views.my_favorites, name="my_favorites"),
    path("news_feed/", views.news_feed, name="news_feed"),
    path("stock_market/", views.stock_market, name="stock_market"),
    path("taiwan_futures/", views.taiwan_futures, name="taiwan_futures"),
]
