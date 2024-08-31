from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import logout
from django.shortcuts import redirect, render





urlpatterns = [
    path("users/", include("users.urls")),
    path("userprofiles/", include("userprofiles.urls")),
    path("admin@bbforum.17th/", admin.site.urls),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("", include("pages.urls"), name="pages"),
    path("users/", include("users.urls"), name="users"),
    path("articles/", include("articles.urls")),
] 
+ debug_toolbar_urls()
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
