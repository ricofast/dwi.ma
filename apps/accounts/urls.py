from django.contrib.auth import views as auth_views
from django.urls import path

from .views import WhatsAppLoginView, PhoneRegisterView
from .forms import PhoneLoginForm

app_name = "accounts"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html", next_page='dashboard'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='landing'), name="logout"),
    path("register/", PhoneRegisterView.as_view(), name="register"),
    path("whatsapp-login/<str:token>/", WhatsAppLoginView.as_view(), name="whatsapp-login"),
]
