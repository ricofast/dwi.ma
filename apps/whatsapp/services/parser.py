def normalize_message_type(raw_message):
    msg_type = (raw_message or {}).get("type", "unknown")
    if msg_type == "interactive":
        itype = (raw_message.get("interactive") or {}).get("type")
        if itype == "button_reply":
            return "button"
        if itype == "list_reply":
            return "list_reply"
        return "interactive"
    return msg_type if msg_type in {"text", "audio", "image", "document"} else "unknown"


def get_text_from_message(raw_message):
    if raw_message.get("type") == "text":
        return (raw_message.get("text") or {}).get("body")
    interactive = raw_message.get("interactive") or {}
    if interactive.get("type") == "button_reply":
        return (interactive.get("button_reply") or {}).get("title")
    if interactive.get("type") == "list_reply":
        return (interactive.get("list_reply") or {}).get("title")
    return None


def get_interactive_reply(raw_message):
    return (raw_message or {}).get("interactive")


def extract_inbound_messages(payload):
    out = []
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            contacts = value.get("contacts", [])
            name = (contacts[0].get("profile") or {}).get("name") if contacts else None
            raw_profile = contacts[0] if contacts else {}
            for message in value.get("messages", []):
                wa_id = message.get("from")
                out.append({
                    "wa_id": wa_id,
                    "phone_number": wa_id,
                    "display_name": name,
                    "raw_profile": raw_profile,
                    "message_id": message.get("id"),
                    "message_type": normalize_message_type(message),
                    "text_body": get_text_from_message(message),
                    "interactive_payload": get_interactive_reply(message),
                    "media_id": ((message.get("document") or message.get("image") or message.get("audio") or {}).get("id")),
                    "raw_payload": message,
                })
    return out


def extract_status_updates(payload):
    statuses = []
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            for s in change.get("value", {}).get("statuses", []):
                statuses.append({"message_id": s.get("id"), "status": s.get("status")})
    return statuses


def parse_webhook_payload(payload):
    return {"messages": extract_inbound_messages(payload), "statuses": extract_status_updates(payload)}
