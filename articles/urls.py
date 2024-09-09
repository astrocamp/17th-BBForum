from django.urls import path

from pages import views as pages_views

from . import views

app_name = "articles"

urlpatterns = [
    path("", pages_views.index, name="index"),
    path("new", views.new, name="new"),
    path("<int:id>", views.show, name="show"),
    path("<int:id>/edit", views.edit, name="edit"),
    path("<int:id>/delete", views.delete, name="delete"),
    path("<int:id>/comments", views.comment, name="comment"),
    path("comments/<int:id>/delete/", views.delete_comment, name="delete_comment"),
    path("comments/<int:id>/update/", views.update_comment, name="update_comment"),
    path("<int:id>/liked", views.liked, name="liked"),
]
