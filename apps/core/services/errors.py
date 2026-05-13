SAFE_MESSAGES = {
    "DOCUMENT_UNREADABLE": "سمح ليا، ما قدرتش نقرا هاد الوثيقة مزيان. جرب تصيفط نسخة أوضح.",
    "AI_FAILED": "وقع مشكل تقني فاش كنوجد الجواب. ما نقصناش ليك الكريدي.",
    "INSUFFICIENT_CREDITS": "ما بقاوش عندك الكريديات الكافية. شحن الرصيد باش تكمل.",
    "PAYMENT_FAILED": "ما تكملش الأداء. جرب مرة أخرى أو اختار طريقة أخرى.",
    "WHATSAPP_SEND_FAILED": "ما قدرناش نصيفطو النتيجة للواتساب دابا. تقدر تشوفها فالحساب ديالك.",
}

def get_safe_error_message(error_code):
    return SAFE_MESSAGES.get(error_code, "وقع مشكل تقني صغير. عاود المحاولة من فضلك.")

def map_exception_to_safe_message(exception):
    msg = str(exception).lower()
    if "credit" in msg:
        return get_safe_error_message("INSUFFICIENT_CREDITS")
    if "payment" in msg:
        return get_safe_error_message("PAYMENT_FAILED")
    return get_safe_error_message("AI_FAILED")
