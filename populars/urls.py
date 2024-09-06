from django.urls import path

from . import views

app_name = "populars"

urlpatterns = [
    path("", views.base, name="base"),
    path("popular_stocks/", views.popular_stocks, name="popular_stocks"),
    path("popular_students/", views.popular_students, name="popular_students"),
    path("popular_answers/", views.popular_answers, name="popular_answers"),
]