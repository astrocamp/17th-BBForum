from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("users/", include("users.urls")),
    path("admin@bbforum.17th/", admin.site.urls),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("", include("pages.urls"), name="pages"),
    path("users/", include("users.urls"), name="users"),
] + debug_toolbar_urls()
