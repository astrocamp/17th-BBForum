from django.urls import path

from . import views

app_name = "users"


urlpatterns = [
    path("", views.index, name="index"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("sign_out", views.sign_out, name="sign_out"),
    path("register", views.register, name="register"),
    path("auth_denied", views.auth_denied, name="auth_denied"),
    path("forget_password", views.forget_password, name="forget_password"),
]
