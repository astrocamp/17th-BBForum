from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import include, path

def is_dev():
    return settings.DEBUG
urlpatterns = (
    [
        path("social-auth/", include("social_django.urls", namespace="social")),
        path("", include("pages.urls"), name="pages"),
        path("users/", include("users.urls"), name="users"),
        path("userprofiles/", include("userprofiles.urls"), name="userprofiles"),
        path("articles/", include("articles.urls")),
        path("points/", include("points.urls"), name="points"),
    ]
)
if is_dev():
    urlpatterns += debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



