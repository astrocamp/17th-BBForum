from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("my_watchlist/", views.my_watchlist, name="my_watchlist"),
    path("my_favorites/", views.my_favorites, name="my_favorites"),
    path("member_profile/", views.member_profile, name="member_profile"),
]
