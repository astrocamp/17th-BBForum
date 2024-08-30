from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('member/', include('members.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [    
        path('__debug__/', include(debug_toolbar.urls)),
    ]
