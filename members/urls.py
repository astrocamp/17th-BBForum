from django.urls import path
from . import views

urlpatterns = [
    path('member/', views.simulate_login_view, name='simulate_actions'),
    path('member/login/', views.simulate_login_view, name='simulate_login'),
    path('member/post/', views.simulate_post_view, name='simulate_post'),
]
