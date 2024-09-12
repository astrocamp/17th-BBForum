from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


def is_dev():
    return settings.DEBUG


urlpatterns = [
    path("", include("pages.urls"), name="pages"),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("users/", include("users.urls"), name="users"),
    path("userprofiles/", include("userprofiles.urls"), name="userprofiles"),
    path("articles/", include("articles.urls")),
    path("points/", include("points.urls"), name="points"),
    path(
        "populars/", include(("populars.urls", "populars"), namespace="popular_pages")
    ),
    path("follows/", include(("follows.urls"), namespace="follows")),
    path("picks/", include(("picks.urls"), namespace="picks")),
]

if is_dev():
    urlpatterns += debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
