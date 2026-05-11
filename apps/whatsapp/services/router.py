from apps.assistant.tasks import explain_text_task
from apps.wallet.services import get_balance
from .messages import send_account_link_message, send_credit_balance, send_document_upload_link, send_main_menu, send_processing_message, send_text_explanation_prompt
from apps.whatsapp.models import WhatsAppConversationState

MENU_TRIGGERS = {"menu", "salam", "السلام", "hi"}

def route_inbound_message(inbound_message):
    state, _ = WhatsAppConversationState.objects.get_or_create(wa_id=inbound_message.wa_id, defaults={"user": inbound_message.user, "current_state": WhatsAppConversationState.State.UNKNOWN})
    text = (inbound_message.text_body or "").strip().lower()
    if text in MENU_TRIGGERS or state.current_state == WhatsAppConversationState.State.UNKNOWN:
        state.current_state = WhatsAppConversationState.State.MAIN_MENU; state.save(update_fields=["current_state", "updated_at", "last_seen_at"])
        return send_main_menu(inbound_message.wa_id)
    if "شرح نص" in (inbound_message.text_body or ""):
        state.current_state = WhatsAppConversationState.State.WAITING_FOR_TEXT; state.save(update_fields=["current_state", "updated_at", "last_seen_at"])
        return send_text_explanation_prompt(inbound_message.wa_id)
    if "شرح وثيقة" in (inbound_message.text_body or ""):
        return send_document_upload_link(inbound_message.wa_id, "http://localhost:8000/document/upload/")
    if "الرصيد" in (inbound_message.text_body or ""):
        if not inbound_message.user:
            return send_account_link_message(inbound_message.wa_id)
        return send_credit_balance(inbound_message.wa_id, get_balance(inbound_message.user))
    if state.current_state == WhatsAppConversationState.State.WAITING_FOR_TEXT and inbound_message.text_body:
        if not inbound_message.user:
            return send_account_link_message(inbound_message.wa_id)
        send_processing_message(inbound_message.wa_id)
        explain_text_task.delay(str(inbound_message.user_id), inbound_message.text_body, {"output_language": "darija_arabic"})
        state.current_state = WhatsAppConversationState.State.WAITING_FOR_ACTION; state.save(update_fields=["current_state", "updated_at", "last_seen_at"])
        return None
    return send_main_menu(inbound_message.wa_id)
