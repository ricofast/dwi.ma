from django.urls import path

from .views import DashboardView, landing, privacy_policy, terms_of_service

urlpatterns = [
    path("", landing, name="landing"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("privacy/", privacy_policy, name="privacy"),
    path("terms/", terms_of_service, name="terms"),
]
