from django.urls import path

from . import views
from .views import follow_user, user_profile

urlpatterns = [
    path("profile/<int:user_id>/", views.user_profile, name="user_profile"),
    path("follow/", views.follow_user, name="follow_user"),
]
