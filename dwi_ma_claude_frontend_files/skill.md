# skill.md — Skills and Implementation Guidance for dwi.ma Frontend

This file describes the skills, techniques, and implementation patterns Claude should use when improving the dwi.ma PWA frontend.

---

## 1. Core Frontend Skills Required

Claude should apply the following skills:

- Django template architecture
- Bootstrap 5 responsive layouts
- Mobile-first SaaS design
- HTMX progressive enhancement
- Alpine.js micro-interactions
- Form UX and validation states
- PWA fundamentals
- Accessibility basics
- Privacy-first UI design
- Darija-first product copy
- SaaS dashboard design
- Payment UI design
- AI result-page UX
- File upload UX
- Empty/loading/error states

---

## 2. Django Template Skills

Use Django templates cleanly.

Recommended patterns:

```text
templates/
  base.html
  components/
    _navbar.html
    _bottom_nav.html
    _flash_messages.html
    _action_card.html
    _result_section.html
  pages/
    home.html
    privacy.html
    terms.html
    support.html
  dashboard/
    index.html
  documents/
    upload.html
    processing.html
    analysis_result.html
  assistant/
    explain_text_form.html
    text_result.html
    generate_message_form.html
    message_result.html
  payments/
    products.html
    success.html
    failed.html
  wallet/
    balance.html
```

Use template inheritance:

```django
{% extends "base.html" %}
{% block title %}شرح ليا وثيقة{% endblock %}
{% block content %}
...
{% endblock %}
```

Use reusable partials:

```django
{% include "components/_action_card.html" with title="شرح ليا وثيقة" %}
```

Avoid duplicating layout logic.

---

## 3. Bootstrap 5 Skills

Use Bootstrap for:

- Grid layout
- Cards
- Buttons
- Forms
- Alerts
- Badges
- Modals
- Utility classes
- Responsive spacing

Recommended class style:

```html
<div class="container py-4">
  <div class="row g-3">
    <div class="col-12 col-lg-4">
      <div class="card app-card h-100">
        ...
      </div>
    </div>
  </div>
</div>
```

Avoid custom CSS when Bootstrap utilities are enough.

Use custom CSS only for product-specific identity.

---

## 4. HTMX Skills

Use HTMX for simple progressive enhancement.

Good use cases:

- Processing page polling
- Job status refresh
- Partial result loading
- Form fragments
- Inline validation feedback

Example:

```html
<div
  hx-get="{% url 'assistant:job_status_partial' job.id %}"
  hx-trigger="load, every 3s"
  hx-swap="outerHTML">
  {% include "components/_loading_state.html" %}
</div>
```

Rules:

- Polling must stop when job is completed or failed.
- Always provide non-HTMX fallback where practical.
- Do not build complex frontend state with HTMX.
- Do not use HTMX to hide backend errors.

---

## 5. Alpine.js Skills

Use Alpine.js only for small interactions.

Good use cases:

- Copy to clipboard
- Toggle text/voice input mode
- Show selected filename
- Character counter
- Delete confirmation
- Collapsible result sections
- Install PWA prompt UI

Example:

```html
<div x-data="{ copied: false }">
  <button
    type="button"
    @click="navigator.clipboard.writeText($refs.result.innerText); copied = true">
    نسخ النتيجة
  </button>
  <span x-show="copied">تنسخات ✅</span>
</div>
```

Avoid using Alpine.js for:

- App-wide routing
- Payment state
- Authentication
- AI workflow orchestration
- Complex data fetching

---

## 6. Mobile-First Design Skills

Design for a Moroccan smartphone user first.

Rules:

- Use large buttons.
- Keep primary actions above the fold.
- Avoid dense tables on mobile.
- Prefer cards over tables.
- Use bottom navigation for authenticated users.
- Use clear page titles.
- Keep forms short.
- Show next step clearly.

Minimum tap target height:

```css
min-height: 44px;
```

Use responsive layout:

```html
<div class="row g-3">
  <div class="col-12 col-md-6 col-xl-4">
    ...
  </div>
</div>
```

---

## 7. AI Result UX Skills

AI results should feel structured, not like a raw chat response.

For document/text explanations, show:

1. Type
2. Summary
3. Important points
4. Extracted names/dates/amounts/deadlines
5. Unclear points
6. What to do next
7. Disclaimer
8. Full answer

Use sections:

```html
<section class="result-section">
  <h2>الخلاصة</h2>
  <p>{{ analysis.summary_darija }}</p>
</section>
```

For generated messages, show:

1. Original instruction/transcript
2. Missing information
3. Suggested subject
4. Generated message
5. Notes
6. Copy action

Never show raw JSON to normal users.

---

## 8. File Upload UX Skills

File upload pages must be simple and reassuring.

Show:

- Supported file types
- Max file size
- Consent text
- Credit note
- Privacy reassurance
- Selected filename
- Clear submit button

Recommended copy:

```text
طلع PDF ولا صورة، وغادي نشرحوها ليك بدارجة بسيطة.
```

Consent copy:

```text
كنوافق أن dwi.ma يعالج هاد الوثيقة باش يشرحها ليا. نقدر نمسحها من بعد.
```

---

## 9. Payment UI Skills

Payment UI must be transparent.

Show:

- Package name
- Price in MAD
- Number of credits
- What credits can be used for
- Payment status
- Success/failure state
- Updated balance after success

Never show raw provider payloads.

Use friendly payment states:

- تم الأداء بنجاح
- ما تكملش الأداء
- العملية مازال كتسنى
- رجع للداشبورد

---

## 10. Privacy and Trust UI Skills

Privacy must be visible, not hidden.

Add trust notes near sensitive actions:

- Uploading documents
- Uploading audio
- Sending to WhatsApp
- Payment

Examples:

```text
تقدر تمسح الوثيقة من بعد.
```

```text
ما كنستعملوش وثائقك باش ندربو AI بلا موافقة منك.
```

```text
هاد الشرح غير للمساعدة، وماشي استشارة مهنية.
```

---

## 11. Error State Skills

Every important workflow needs safe error states.

Create reusable error component:

```django
{% include "components/_error_state.html" with message=safe_error_message %}
```

Good error copy:

- ما قدرناش نقراو هاد الوثيقة. جرب نسخة أوضح.
- وقع مشكل تقني. ما نقصناش ليك الكريدي.
- ما تكملش الأداء. جرب مرة أخرى.
- ما قدرناش نصيفطو النتيجة للواتساب دابا.

Bad error copy:

- KeyError at /documents/...
- Provider returned 500
- JSONDecodeError
- Digital Virgo raw error
- Stack traces

---

## 12. Empty State Skills

Use friendly empty states.

Examples:

History empty state:

```text
مازال ما عندك حتى نتيجة.
جرب تشرح وثيقة ولا نص باش تبان هنا.
```

Wallet empty usage state:

```text
مازال ما استعملتي حتى كريدي.
```

Documents empty state:

```text
طلع أول وثيقة وغادي نشرحوها ليك بدارجة.
```

---

## 13. Accessibility Skills

Every form field needs:

- Label
- Help text if needed
- Error display
- Focus state
- Keyboard support

Every icon-only button needs:

```html
aria-label="..."
```

Use semantic HTML:

- `<main>`
- `<section>`
- `<nav>`
- `<header>`
- `<footer>`

---

## 14. QA Skills

After changes, Claude should check:

- Mobile layout
- Desktop layout
- Navigation
- Forms
- Validation messages
- Loading states
- Empty states
- Error states
- Copy buttons
- Delete confirmations
- Payment status pages
- PWA manifest
- Service worker cache rules
- Accessibility basics

---

## 15. What Good Looks Like

The frontend is successful when:

- A first-time mobile user knows what to do immediately.
- The dashboard has only a few clear actions.
- The result pages are easy to scan.
- Credits and privacy are always clear.
- The app feels modern without feeling complicated.
- The frontend does not introduce backend risk.
