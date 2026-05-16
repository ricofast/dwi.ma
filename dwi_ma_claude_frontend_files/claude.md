# claude.md — dwi.ma Frontend Development Instructions

You are Claude Code working on **dwi.ma**, a Moroccan Darija AI SaaS/PWA.

Your role is to help build a professional, modern, mobile-first frontend using the existing Django backend. Work incrementally, safely, and with strong product discipline.

---

## 1. Product Context

dwi.ma helps Moroccan users:

1. Upload a document and get a simple Moroccan Darija explanation.
2. Paste French/Arabic/formal text and get a simple Darija explanation.
3. Give Darija instructions by text or voice and receive a professional message.
4. Receive results through WhatsApp.
5. Buy credits and manage usage.

The product is **not** a generic chatbot. It is a focused Moroccan AI utility.

Core positioning:

> شرح الوثائق والرسائل بدارجة بسيطة.

---

## 2. Technical Stack

Use the existing stack:

- Django templates
- Bootstrap 5.3+
- HTMX for progressive enhancement and polling
- Alpine.js only for small local interactions
- Plain CSS with reusable variables/components
- PWA manifest and service worker
- Django static files
- Django URL/view/template structure

Do **not** convert the project into:

- React
- Next.js
- Vue
- A single-page app
- Tailwind rewrite
- Heavy JavaScript frontend

---

## 3. Development Principles

### Build step by step

Do not implement large frontend changes in one massive pass. Work page by page and component by component.

Recommended order:

1. Base layout and design system
2. Dashboard
3. Document upload flow
4. Document result page
5. Pasted text explanation flow
6. Message generation / voice upload flow
7. Wallet and payment UI
8. History and settings
9. Landing page
10. Privacy, terms, support pages
11. PWA installability
12. QA and polish

### Protect backend logic

Do not change backend business logic unless explicitly necessary for template context.

Avoid altering:

- AI processing logic
- Wallet charging logic
- Payment logic
- WhatsApp webhook logic
- Celery task behavior
- Authentication flows

### Prefer server-rendered pages

Use Django templates as the primary rendering layer.

HTMX is allowed for:

- Job status polling
- Partial refresh
- Inline form feedback
- Loading states

Alpine.js is allowed for:

- Copy-to-clipboard
- Toggle sections
- Upload preview labels
- Character counters
- Confirmation modals

---

## 4. UX Philosophy

Design dwi.ma like a focused, trustworthy Moroccan SaaS tool.

The user should feel:

> I know what to do, I trust this service, and I can get my answer quickly.

The interface must be:

- Mobile-first
- Darija-friendly
- Simple
- Trustworthy
- Fast
- Accessible
- Clear about credits
- Clear about privacy
- Clear about AI limitations

Avoid:

- Generic chatbot UI as the primary interface
- Long complicated menus
- Technical AI terminology
- Hidden pricing
- Unclear credit usage
- Raw JSON or stack traces in user-facing pages

---

## 5. Language Rules

Primary UI language should be simple Moroccan Darija in Arabic script.

Use short, practical labels:

- شرح ليا وثيقة
- شرح ليا نص
- كتب ليا رسالة
- الرصيد ديالي
- شحن الرصيد
- صيفط للواتساب
- نسخ النتيجة
- مسح الوثيقة
- رجع للداشبورد

Avoid heavy formal Arabic unless necessary.

Do not use unclear or overly formal labels like:

- معالجة المستندات الذكية
- الاستفادة من القدرات المعرفية
- تحليل لغوي متعدد الوسائط

Keep the copy human and practical.

---

## 6. Main Pages to Support

### Public pages

- Home
- How it works
- Pricing preview
- Login/signup
- Privacy policy
- Terms of service
- Support/FAQ

### Authenticated PWA pages

- Dashboard
- Explain document
- Document processing
- Document result
- Explain text
- Text result
- Write message
- Voice upload
- Message result
- Wallet/credits
- Payment status
- History
- WhatsApp settings/linking
- Account settings

---

## 7. Reusable Components

Create reusable Django partials whenever possible.

Recommended partials:

```text
templates/components/_navbar.html
templates/components/_bottom_nav.html
templates/components/_flash_messages.html
templates/components/_credit_balance_pill.html
templates/components/_action_card.html
templates/components/_status_badge.html
templates/components/_result_section.html
templates/components/_copy_button.html
templates/components/_feedback_buttons.html
templates/components/_consent_box.html
templates/components/_pricing_card.html
templates/components/_empty_state.html
templates/components/_error_state.html
templates/components/_loading_state.html
```

Do not duplicate large blocks of UI across pages.

---

## 8. Critical User Flows

### Flow 1: Explain document

1. User opens dashboard.
2. Taps “شرح ليا وثيقة”.
3. Uploads PDF/image.
4. Accepts consent.
5. Sees credit note.
6. Submits.
7. Sees processing page.
8. Gets structured Darija result.
9. Can copy, send to WhatsApp, delete, or submit feedback.

### Flow 2: Explain text

1. User taps “شرح ليا نص”.
2. Pastes text.
3. Sees 1-credit note.
4. Submits.
5. Gets structured Darija explanation.
6. Can copy, send to WhatsApp, or submit feedback.

### Flow 3: Write message

1. User taps “كتب ليا رسالة”.
2. Chooses text input or voice upload.
3. Enters Darija instruction.
4. Chooses target format.
5. Chooses tone.
6. Submits.
7. Gets generated message.
8. Can copy or send to WhatsApp.

### Flow 4: Wallet

1. User sees current credit balance.
2. Opens wallet/pricing.
3. Chooses credit package.
4. Starts payment.
5. Sees success/failure page.
6. Balance updates after successful payment.

---

## 9. Frontend Safety Rules

Always show required consent before:

- Document upload
- Audio upload
- WhatsApp result delivery
- Payment

Always show clear credit usage before paid actions:

> هاد العملية غادي تستعمل 1 كريدي إلا خرجات النتيجة بنجاح.

Never expose technical errors to users.

Use safe messages:

- وقع مشكل تقني. ما نقصناش ليك الكريدي.
- ما قدرناش نقراو هاد الوثيقة. جرب نسخة أوضح.
- ما تكملش الأداء. جرب مرة أخرى.
- ما قدرناش نصيفطو النتيجة للواتساب دابا.

Delete actions must require confirmation.

Do not cache sensitive user data in the service worker.

Sensitive data includes:

- Uploaded documents
- Audio files
- AI results
- Payment data
- WhatsApp payloads
- Authenticated API responses

---

## 10. Accessibility Rules

- Use real labels for form fields.
- Do not rely only on placeholders.
- Buttons must have clear text or aria-label.
- Use readable contrast.
- Tap targets should be at least 44px high.
- Form errors should appear near the relevant field.
- Loading states should be visible.
- Pages should remain usable without heavy JavaScript.

---

## 11. PWA Rules

The PWA should be installable but safe.

Allowed to cache:

- CSS
- JS
- logo/icons
- offline fallback page
- safe public static assets

Never cache:

- Documents
- Audio
- AI results
- Payment pages
- Authenticated API responses
- WhatsApp data
- User account pages

The service worker must degrade gracefully if unsupported.

---

## 12. Claude Workflow

Before coding, always:

1. Inspect existing files.
2. Identify templates/static files already present.
3. Explain intended changes briefly.
4. Modify only files needed for the current task.
5. Keep changes small and reviewable.
6. Do not invent backend routes that do not exist.
7. If a route or context variable is missing, add a minimal safe placeholder or state the required backend change.

After coding, always report:

- Files changed
- What was added
- What assumptions were made
- How to test manually
- Any remaining TODOs

---

## 13. Non-Negotiable Constraints

Do not build a generic chatbot UI.

Do not implement new backend product features unless requested.

Do not change wallet charging rules.

Do not change payment callback logic.

Do not change AI prompts unless requested.

Do not expose raw AI/provider/payment/WhatsApp payloads to users.

Do not cache sensitive data in PWA.

Do not overcomplicate the MVP.

---

## 14. Final Product Standard

The PWA is good enough when a Moroccan mobile user can understand the screen in less than 5 seconds and confidently answer:

1. What can I do here?
2. How much will it cost?
3. Is my file/private data safe?
4. What happens next?
