from django.conf import settings
from .providers import get_whatsapp_provider

MENU = "Salam 👋 Ana dwi.ma.\nشنو بغيتي ندير ليك؟\n\n1. نشرح ليك وثيقة\n2. نشرح ليك نص\n3. نكتب ليك رسالة\n4. نشوف الرصيد ديالك"

def send_main_menu(wa_id):
    return get_whatsapp_provider().send_text(wa_id, MENU)
def send_account_link_message(wa_id):
    return get_whatsapp_provider().send_text(wa_id, f"باش تكمل، ربط الحساب ديالك من هنا: {getattr(settings,'SITE_URL','http://localhost:8000')}/accounts/login/")
def send_document_upload_link(wa_id, signed_url): return get_whatsapp_provider().send_text(wa_id, f"صيفط الوثيقة من هنا: {signed_url}")
def send_text_explanation_prompt(wa_id): return get_whatsapp_provider().send_text(wa_id, "صيفط ليا النص اللي بغيتي نشرحو ليك بدارجة.")
def send_credit_balance(wa_id, balance): return get_whatsapp_provider().send_text(wa_id, f"الرصيد ديالك هو: {balance} كريدي.")
def send_processing_message(wa_id): return get_whatsapp_provider().send_text(wa_id, "توصلت ✅ غادي نخدم عليها دابا.")
def send_error_message(wa_id, safe_message): return get_whatsapp_provider().send_text(wa_id, safe_message)
def send_result_message(wa_id, result_text): return get_whatsapp_provider().send_text(wa_id, result_text)
