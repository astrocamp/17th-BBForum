from django.urls import path
from . import views

urlpatterns = [
    
    path('points-log/', views.points_log_view, name='points_log'),
]
