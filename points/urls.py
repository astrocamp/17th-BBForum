from django.urls import path

from . import views

app_name = "points"

urlpatterns = [
    path("", views.register_points, name="register_points"),
]
