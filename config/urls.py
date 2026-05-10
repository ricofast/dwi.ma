from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("apps.core.urls")),
    path("api/", include("apps.core.api_urls")),
]
