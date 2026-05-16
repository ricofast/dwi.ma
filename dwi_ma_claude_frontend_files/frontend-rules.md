# frontend-rules.md — Non-Negotiable Frontend Rules for dwi.ma

These rules must guide all frontend work on the dwi.ma PWA.

---

## 1. Product Rule

dwi.ma is **not** a generic chatbot.

The UI must focus on three main jobs:

1. Explain my document.
2. Explain my text.
3. Write my message.

Every major page should support one of these jobs clearly.

---

## 2. Stack Rule

Use:

- Django templates
- Bootstrap 5
- HTMX
- Alpine.js only for small interactions
- Plain CSS

Do not introduce:

- React
- Next.js
- Vue
- Tailwind rewrite
- SPA routing
- Heavy frontend state management
- Large animation libraries

---

## 3. Mobile-First Rule

Design for mobile first.

Every screen must work well on:

- Small Android phones
- iPhones
- Mobile Chrome
- Mobile Safari
- Slow connections

Rules:

- Primary buttons must be large.
- Forms must be easy to fill.
- Important actions must be visible.
- Avoid wide tables.
- Avoid tiny text.
- Avoid dense layouts.

---

## 4. Darija-First Rule

Use simple Moroccan Darija in Arabic script for core UI labels.

Preferred labels:

```text
شرح ليا وثيقة
شرح ليا نص
كتب ليا رسالة
الرصيد ديالي
شحن الرصيد
صيفط للواتساب
نسخ النتيجة
مسح الوثيقة
رجع للداشبورد
```

Avoid heavy formal Arabic and technical AI language.

---

## 5. Clarity Rule

Every page must clearly answer:

1. What is this page for?
2. What should the user do?
3. How many credits will it use?
4. What happens after submission?
5. Can the user delete sensitive files?

---

## 6. Credit Transparency Rule

Before any credit-consuming action, show:

```text
هاد العملية غادي تستعمل 1 كريدي إلا خرجات النتيجة بنجاح.
```

Do not hide credit consumption.

Do not imply credits are charged if the backend only charges on success.

---

## 7. Consent Rule

Show required consent before:

- Document upload
- Audio upload
- WhatsApp sending/linking
- Payment start

Consent text must be visible near the action.

Document consent:

```text
كنوافق أن dwi.ma يعالج هاد الوثيقة باش يشرحها ليا. نقدر نمسحها من بعد.
```

Audio consent:

```text
كنوافق أن dwi.ma يعالج هاد التسجيل الصوتي باش يحولو لنص ويكتب ليا الرسالة.
```

WhatsApp consent:

```text
كنوافق نتوصل بالنتائج والتنبيهات فواتساب.
```

Payment consent:

```text
كنوافق على شروط الأداء واستعمال الكريديات.
```

---

## 8. Privacy Rule

Privacy reassurance must appear near sensitive actions.

Use copy like:

```text
تقدر تمسح الوثيقة من بعد.
```

```text
ما كنستعملوش وثائقك باش ندربو AI بلا موافقة منك.
```

Do not make unsupported promises.

Do not claim legal compliance beyond what is implemented.

---

## 9. Error Safety Rule

Never show technical errors to users.

Do not show:

- Stack traces
- JSON parser errors
- API provider raw errors
- Payment provider payloads
- WhatsApp payloads
- Database errors
- Python exception names

Use safe messages:

```text
وقع مشكل تقني. ما نقصناش ليك الكريدي.
```

```text
ما قدرناش نقراو هاد الوثيقة. جرب نسخة أوضح.
```

```text
ما تكملش الأداء. جرب مرة أخرى.
```

---

## 10. Result Page Rule

AI results must be structured.

Document/text result pages should show:

1. Type
2. Summary
3. Important points
4. Extracted entities
5. Unclear points
6. Next steps
7. Disclaimer
8. Full answer
9. Actions
10. Feedback

Generated-message result pages should show:

1. Original instruction/transcript
2. Detected intent
3. Missing information
4. Suggested subject
5. Generated message
6. Notes
7. Actions
8. Feedback

Never show raw JSON to normal users.

---

## 11. Copy Button Rule

Every final result page must include a copy button.

Button labels:

```text
نسخ النتيجة
نسخ الرسالة
```

After copy, show feedback:

```text
تنسخات ✅
```

---

## 12. WhatsApp Rule

WhatsApp is a companion channel, not the whole product.

Frontend should use WhatsApp for:

- Sending results
- Linking account
- Notifications
- Companion workflows

Do not design the PWA as if WhatsApp replaces the app.

Do not present dwi.ma as “ask anything on WhatsApp.”

---

## 13. Delete Rule

Sensitive items must have delete actions where backend supports deletion.

Delete actions:

- Must require confirmation.
- Must use clear warning copy.
- Must not be visually hidden.
- Must not be the primary CTA.

Delete confirmation copy:

```text
واش متأكد بغيتي تمسح هاد الوثيقة؟
```

```text
واش متأكد بغيتي تمسح هاد التسجيل؟
```

---

## 14. PWA Cache Rule

Never cache sensitive data.

Do not cache:

- Documents
- Audio
- AI results
- Payment pages
- Authenticated API responses
- User profile pages
- WhatsApp data

Allowed cache:

- Static CSS
- Static JS
- Icons
- Logo
- Offline fallback page
- Safe public assets

---

## 15. Loading State Rule

Every long-running action must have a loading/processing state.

Use copy like:

```text
كنوجدو الشرح ديالك…
```

```text
هاد العملية ممكن تاخذ شوية الوقت.
```

For HTMX polling:

- Stop polling on success.
- Stop polling on failure.
- Show friendly failure message.

---

## 16. Empty State Rule

Every list needs an empty state.

Examples:

```text
مازال ما عندك حتى نتيجة.
```

```text
مازال ما استعملتي حتى كريدي.
```

```text
طلع أول وثيقة وغادي نشرحوها ليك بدارجة.
```

---

## 17. Accessibility Rule

Use accessible markup.

Requirements:

- Form labels
- Clear focus states
- Sufficient contrast
- Semantic HTML
- aria-label for icon-only buttons
- Keyboard-accessible controls
- Large tap targets

Minimum tap target:

```css
min-height: 44px;
```

---

## 18. Backend Respect Rule

Frontend work must not break backend workflows.

Do not modify:

- Wallet charging rules
- AI processing rules
- Payment callback idempotency
- WhatsApp webhook logic
- Authentication security
- Celery task behavior

Unless specifically requested.

---

## 19. No Fake Claims Rule

Do not add:

- Fake testimonials
- Fake company logos
- Fake security certifications
- Fake Inwi partnership claims
- Fake user counts
- Unsupported “100% secure” claims
- Unsupported legal/compliance promises

Use honest, modest trust copy.

---

## 20. Final Frontend Standard

Every page must be:

- Understandable in 5 seconds
- Usable on mobile
- Clear about credits
- Clear about privacy
- Friendly in Darija
- Professional enough for a SaaS product
