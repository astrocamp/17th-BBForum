from django.urls import path

from . import views

app_name = "points"

urlpatterns = [
    path("show_profile/", views.show_profile, name="show_profile"),
    path("get-user-points/", views.get_user_points, name="get_user_points"),
]
