from django.urls import path
from ninja import NinjaAPI

from apps.wallet.api import router as wallet_router

api = NinjaAPI(title="dwi.ma API")


@api.get("/health")
def health(request):
    return {"status": "ok"}


api.add_router("", wallet_router)

urlpatterns = [
    path("", api.urls),
]
