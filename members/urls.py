from django.urls import path

from . import views

urlpatterns = [
    path("", views.simulate_login_view, name="simulate_actions"),
    path("login/", views.simulate_login_view, name="simulate_login"),
    path("post/", views.simulate_post_view, name="simulate_post"),
    path("reset/", views.reset_points, name="reset_points"),
]
