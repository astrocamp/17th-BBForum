from django.urls import path

from . import views

app_name = "userprofiles"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>", views.show, name="show"),
    path("<int:id>/edit", views.edit, name="edit"),
]
