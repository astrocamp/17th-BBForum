from django.urls import path

from . import views

urlpatterns = [
    path("", views.simulate_login_view, name="simulate_actions"),
    path("login/", views.simulate_login_view, name="simulate_login"),
    path("post/", views.simulate_post_view, name="simulate_post"),
    path("like/", views.simulate_like_view, name='simulate_like'),
    path("reset/", views.reset_points, name="reset_points"),
    path('report/', views.report_user, name='report_user'),
    path('points-log/', views.points_log_view, name='points_log'),
    
]
