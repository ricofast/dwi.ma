from django.urls import path

from .views import DashboardView, landing

urlpatterns = [
    path("", landing, name="landing"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
