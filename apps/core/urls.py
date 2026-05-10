from django.urls import path

from .views import dashboard, landing

urlpatterns = [
    path("", landing, name="landing"),
    path("dashboard/", dashboard, name="dashboard"),
]
