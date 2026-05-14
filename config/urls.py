from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("apps.core.urls")),
    path("document/", include("apps.documents.urls", namespace="document")),
    path("api/", include("apps.core.api_urls")),
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("whatsapp/", include("apps.whatsapp.urls")),
    path("assistant/", include("apps.assistant.urls", namespace="assistant")),
    path("wallet/", include("apps.wallet.urls", namespace="wallet")),
    path("payments/", include("apps.payments.urls", namespace="payments")),
]
