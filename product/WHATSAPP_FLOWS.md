# dwi.ma WhatsApp Flows

WhatsApp is a companion interface. The PWA remains the main product surface.

The WhatsApp bot should be task-specific, not a generic chatbot.

---

## 1. Main Menu

Message:

```text
Salam 👋 Ana dwi.ma.
شنو بغيتي ندير ليك؟

1. نشرح ليك وثيقة
2. نكتب ليك رسالة مهنية
3. نشرح ليك نص
4. نشوف الرصيد ديالك
```

Interactive options:

- `explain_document`
- `generate_message`
- `explain_text`
- `check_credits`

---

## 2. Explain Document Flow

### Step 1 — User selects document explanation

Bot:

```text
مزيان ✅
صيفط ليا PDF ولا صورة ديال الوثيقة، وغادي نشرحها ليك بدارجة بسيطة.
```

### Step 2 — User sends document/image

Bot:

```text
توصلت بالوثيقة ✅
غادي نحاول نقراها ونشرحها ليك بدارجة بسيطة.
هاد العملية ممكن تاخذ شوية الوقت.
```

Backend:

1. Store inbound WhatsApp message.
2. Download media.
3. Create UploadedDocument.
4. Queue processing job.
5. Send result when complete.

### Step 3 — Success result

Bot:

```text
ها الشرح ديال الوثيقة بدارجة:
```

Then send the result text.

If result is too long:

```text
الشرح طويل شوية. ها الخلاصة، وتقدر تشوف التفاصيل كاملة هنا:
{{result_link}}
```

### Step 4 — Failure

Bot:

```text
سمح ليا، ما قدرتش نقرا هاد الوثيقة مزيان.
جرب تصيفط صورة واضحة أو PDF أوضح.
ما نقصناش ليك الكريدي.
```

---

## 3. Explain Text Flow

### Step 1 — User chooses text explanation

Bot:

```text
صيفط ليا النص اللي بغيتي نشرحو ليك بدارجة.
```

### Step 2 — User sends text

Bot:

```text
توصلت بالنص ✅
غادي نشرحو ليك بدارجة بسيطة.
```

### Step 3 — Result

Bot sends explanation.

---

## 4. Generate Message Flow

### Step 1 — User chooses message generation

Bot:

```text
شنو نوع الرسالة اللي بغيتي؟

1. Email بالفرنسية
2. رسالة بالعربية
3. Message WhatsApp بدارجة مزيانة
4. رد قصير
```

### Step 2 — User chooses format

Bot:

```text
صيفط ليا شنو بغيتي تقول بدارجة، كتابة ولا voice note.
```

### Step 3 — User sends text/audio

Bot:

```text
توصلت ✅
غادي نوجد ليك الرسالة.
```

### Step 4 — Result

Bot:

```text
ها الرسالة واجدة:
```

Then send generated message.

---

## 5. Credits Flow

### User asks for balance

Bot:

```text
الرصيد ديالك هو: {{credits}} كريدي.
```

If low balance:

```text
باقي عندك {{credits}} كريدي.
إلى بغيتي تزيد، اختار واحد العرض:
```

Options:

- One document
- Mini pack
- Pro pack

---

## 6. Payment Prompt

When credits are exhausted:

```text
سالاو الكريديات المجانية ديالك.

باش تكمل، اختار واحد العرض:
- وثيقة وحدة
- باقة صغيرة
- باقة شهرية
```

If payment requires PWA link:

```text
تقدر تكمل الأداء من هنا:
{{payment_link}}
```

After payment success:

```text
تم الأداء بنجاح ✅
تزادو ليك {{credits_added}} كريدي.
الرصيد الحالي ديالك: {{new_balance}}.
```

Payment failure:

```text
ما كملش الأداء.
جرب مرة أخرى أو اختار عرض آخر.
```

---

## 7. Help Flow

Bot:

```text
dwi.ma كيعاونك فـ 3 حوايج:

1. نشرح ليك وثيقة بدارجة
2. نشرح ليك نص صعيب
3. نكتب ليك رسالة مهنية من دارجة

صيفط:
- وثيقة PDF ولا صورة
- نص
- أو voice note
```

---

## 8. Unsupported Request

Bot:

```text
سمح ليا، دابا نقدر نعاونك غير فشرح الوثائق، شرح النصوص، وكتابة الرسائل.
اختار واحد من هاد الاختيارات:
```

Then show main menu.

---

## 9. Disclaimer Message

For sensitive documents:

```text
ملاحظة: هاد الشرح غير باش يعاونك تفهم الوثيقة، وماشي استشارة قانونية أو طبية أو مالية أو إدارية رسمية.
```

---

## 10. WhatsApp Implementation Notes

### Inbound message types to support in MVP

- text
- document
- image
- audio
- interactive reply

### Store

- Raw webhook event.
- WhatsApp message ID.
- wa_id / phone number.
- Message type.
- Media ID.
- Text body.
- Processing status.

### Process asynchronously

Webhook endpoint must:

1. Validate.
2. Store.
3. Return 200.
4. Queue Celery job.

### Outbound messages

Create a service:

```python
send_text_message(to: str, text: str)
send_menu_message(to: str)
send_result_message(to: str, result: str, link: str | None = None)
```

### Avoid

- Open-ended “ask anything” positioning.
- Long answers split randomly.
- Charging user before success.
- Processing files inside webhook request.
