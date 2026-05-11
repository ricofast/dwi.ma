from django.contrib.auth import login
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views import View

from apps.accounts.services.magic_links import InvalidMagicToken, consume_whatsapp_login_token
from apps.accounts.services.whatsapp_identity import link_whatsapp_identity_to_user


class WhatsAppLoginView(View):
    def get(self, request, token):
        try:
            payload, identity = consume_whatsapp_login_token(token)
        except InvalidMagicToken:
            return HttpResponseBadRequest("Invalid or expired token")

        user = identity.user
        if user is None:
            phone_number = identity.phone_number or f"wa-{identity.wa_id}"
            from django.contrib.auth import get_user_model
            user = get_user_model().objects.create_user(phone_number=phone_number)

        link_whatsapp_identity_to_user(identity, user)
        login(request, user)

        next_url = payload.get("next_url") or "dashboard"
        if next_url == "dashboard":
            return redirect("dashboard")
        return redirect(next_url)
