from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("apps.core.urls")),
    path("documents/", include("apps.documents.urls")),
    path("documents/", include("apps.documents.urls", namespace="document")),
    path("api/", include("apps.core.api_urls")),
]
