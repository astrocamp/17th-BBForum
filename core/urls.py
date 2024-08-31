from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = (
    [
        path("", include("pages.urls")),
        path("userprofiles/", include("userprofiles.urls")),
        path("users/", include("users.urls")),
        path("articles/", include("articles.urls")),
        path("admin@bbforum.17th/", admin.site.urls),
    ]
    + debug_toolbar_urls()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
