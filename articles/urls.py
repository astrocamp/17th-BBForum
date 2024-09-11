from django.urls import path

from pages import views as pages_views

from . import views
from .views import (
    collect_article,
    collect_comment,
    remove_collect_article,
    remove_collect_comment,
)

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
    path(
        "api/collect_article/<int:article_id>/", collect_article, name="collect_article"
    ),
    path(
        "api/remove_collect_article/<int:article_id>/",
        remove_collect_article,
        name="remove_collect_article",
    ),
    path(
        "api/collect_comment/<int:comment_id>/", collect_comment, name="collect_comment"
    ),
    path(
        "api/remove_collect_comment/<int:comment_id>/",
        remove_collect_comment,
        name="remove_collect_comment",
    ),
]
