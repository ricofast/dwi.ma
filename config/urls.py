from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("settings.ADMIN_URL", admin.site.urls),
    path("", include("apps.core.urls")),
    path("api/", include("apps.core.api_urls")),
]
