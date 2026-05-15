from django.urls import path

from .views import (
    DashboardView,
    landing,
    offline,
    privacy_policy,
    service_worker,
    terms_of_service,
)

urlpatterns = [
    path("", landing, name="landing"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("privacy/", privacy_policy, name="privacy"),
    path("terms/", terms_of_service, name="terms"),
    path("offline/", offline, name="offline"),
    path("sw.js", service_worker, name="service-worker"),
]
