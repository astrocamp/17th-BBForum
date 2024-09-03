from django.urls import path
from .views import user_profile, follow_user

urlpatterns = [
    path('user/<int:user_id>/', user_profile, name='user_profile'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
]