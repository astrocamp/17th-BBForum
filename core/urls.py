"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import path, include


def index(req):
    return render(req, "layout/base.html")


def custom_logout(req):
    logout(req)
    return render(req, "layout/base.html")


urlpatterns = [
    path("admin@bbforum.17th/", admin.site.urls),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("logout/", custom_logout, name="logout"),
    path("", index),
] + debug_toolbar_urls()
