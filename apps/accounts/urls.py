from django.contrib.auth import views as auth_views
from django.urls import path

from .views import OnboardingView, PhoneLoginView, PhoneRegisterView, WhatsAppLoginView

app_name = "accounts"

urlpatterns = [
    path("login/", PhoneLoginView.as_view(), name="login"),
    path("register/", PhoneRegisterView.as_view(), name="register"),
    path("onboarding/", OnboardingView.as_view(), name="onboarding"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("whatsapp-login/<str:token>/", WhatsAppLoginView.as_view(), name="whatsapp-login"),
]
