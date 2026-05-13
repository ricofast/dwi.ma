from django.urls import path
from ninja import NinjaAPI

from apps.documents.api import router as documents_router
from apps.assistant.api import router as assistant_router
from apps.wallet.api import router as wallet_router
from apps.whatsapp.api import router as whatsapp_router
from apps.audio.api import router as audio_router
from apps.payments.api import router as payments_router

api = NinjaAPI(title="dwi.ma API")


@api.get("/health")
def health(request):
    return {"status": "ok"}


api.add_router("", wallet_router)
api.add_router("", documents_router)
api.add_router("", assistant_router)
api.add_router("", whatsapp_router)
api.add_router("", audio_router)
api.add_router("", payments_router)

urlpatterns = [
    path("", api.urls),
]
