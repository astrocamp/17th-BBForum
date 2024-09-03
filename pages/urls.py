from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("my_watchlist/", views.my_watchlist, name="my_watchlist"),
    path(
        "member_profile/", views.member_profile, name="member_profile"
    ),  # 确保这一行存在
    path("member_points/", views.member_points, name="member_points"),
]
