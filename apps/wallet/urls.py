from django.urls import path

from .views import WalletBalanceView

app_name = "wallet"

urlpatterns = [
    path("", WalletBalanceView.as_view(), name="balance"),
]
