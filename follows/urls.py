from django.urls import path

from .views import CheckFollowStatusAPI, FollowUserAPI

app_name = "follows"

urlpatterns = [
    path("follow/<int:id>/", FollowUserAPI.as_view(), name="follow_api"),
    path("unfollow/<int:id>/", FollowUserAPI.as_view(), name="unfollow_api"),
    path(
        "check_follow/<int:id>/",
        CheckFollowStatusAPI.as_view(),
        name="check_follow_api",
    ),
]
