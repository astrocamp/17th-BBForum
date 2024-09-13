from django.urls import path

from pages import views as pages_views

from . import views

app_name = "articles"

urlpatterns = [
    path("", pages_views.index, name="index"),
    path("<int:id>", views.show, name="show"),
    path("<int:id>/edit", views.edit, name="edit"),
    path("<int:id>/delete_artile", views.delete_artile, name="delete_artile"),
    path("<int:id>/comments", views.comment, name="comment"),
    path("comments/<int:id>/delete/", views.delete_comment, name="delete_comment"),
    path("comments/<int:id>/update/", views.update_comment, name="update_comment"),
    path("<int:id>/liked", views.liked, name="liked"),
    path("stocks_list/", views.stocks_list, name="stocks_list"),
]
