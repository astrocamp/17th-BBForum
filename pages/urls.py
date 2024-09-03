from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("my_watchlist/", views.my_watchlist, name="my_watchlist"),
]
