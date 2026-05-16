# design-system.md — dwi.ma PWA Design System

This file defines the visual and UI design system for the dwi.ma PWA.

---

## 1. Design Personality

dwi.ma should feel:

- Helpful
- Moroccan
- Simple
- Trustworthy
- Modern
- Mobile-first
- Professional
- Friendly

It should not feel:

- Like a generic chatbot
- Like a government form
- Like a complex enterprise dashboard
- Like a technical AI demo
- Like a cheap SMS/VAS landing page

---

## 2. Brand Essence

### Product sentence

```text
dwi.ma kayشرح ليك الوثائق والنصوص، وكيعاونك تكتب رسائل مهنية بدارجة بسيطة.
```

### Core user emotion

Relief.

The user should feel:

```text
وأخيرا فهمت شنو مكتوب.
```

---

## 3. Color System

Use CSS variables.

```css
:root {
  --dwi-primary: #2447f9;
  --dwi-primary-dark: #1833b8;
  --dwi-primary-soft: #eef2ff;

  --dwi-accent: #10b981;
  --dwi-accent-dark: #047857;
  --dwi-accent-soft: #ecfdf5;

  --dwi-bg: #f8fafc;
  --dwi-surface: #ffffff;
  --dwi-surface-soft: #f1f5f9;

  --dwi-text: #0f172a;
  --dwi-text-muted: #64748b;
  --dwi-border: #e2e8f0;

  --dwi-warning: #f59e0b;
  --dwi-warning-soft: #fffbeb;

  --dwi-danger: #ef4444;
  --dwi-danger-soft: #fef2f2;

  --dwi-success: #22c55e;
  --dwi-success-soft: #f0fdf4;

  --dwi-radius-sm: 0.5rem;
  --dwi-radius-md: 0.875rem;
  --dwi-radius-lg: 1.25rem;
  --dwi-radius-xl: 1.5rem;

  --dwi-shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.06);
  --dwi-shadow-md: 0 8px 24px rgba(15, 23, 42, 0.08);
  --dwi-shadow-lg: 0 20px 40px rgba(15, 23, 42, 0.12);
}
```

### Usage

Primary blue:

- Main CTAs
- Active navigation
- Important icons
- Links

Accent green:

- Success
- Completed jobs
- Positive wallet states
- Confirmation indicators

Warning amber:

- Disclaimers
- Consent hints
- Pending states

Danger red:

- Delete actions
- Failed jobs
- Payment failure

Neutral backgrounds:

- App shell
- Cards
- Form areas
- Result sections

---

## 4. Typography

Use fast system fonts.

```css
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: var(--dwi-text);
  background: var(--dwi-bg);
}
```

### Type scale

```css
.dwi-title-xl {
  font-size: clamp(2rem, 6vw, 4rem);
  line-height: 1.05;
  font-weight: 800;
}

.dwi-title-lg {
  font-size: clamp(1.6rem, 4vw, 2.5rem);
  line-height: 1.15;
  font-weight: 750;
}

.dwi-title-md {
  font-size: 1.35rem;
  line-height: 1.25;
  font-weight: 700;
}

.dwi-body {
  font-size: 1rem;
  line-height: 1.7;
}

.dwi-small {
  font-size: 0.875rem;
  line-height: 1.5;
}
```

### Text rules

- Use short headings.
- Use clear descriptions.
- Avoid long paragraphs in forms.
- Use bullets for results.
- Use larger text for Darija explanations.

---

## 5. Layout System

### Page container

```css
.dwi-page {
  min-height: 100vh;
  background: var(--dwi-bg);
}

.dwi-container {
  width: min(100% - 1.25rem, 1120px);
  margin-inline: auto;
}
```

### Authenticated app shell

```css
.dwi-app-shell {
  padding-bottom: 5rem;
}

@media (min-width: 992px) {
  .dwi-app-shell {
    padding-bottom: 0;
  }
}
```

### Section spacing

```css
.dwi-section {
  padding-block: 2rem;
}

@media (min-width: 768px) {
  .dwi-section {
    padding-block: 4rem;
  }
}
```

---

## 6. Card System

### Standard card

```css
.dwi-card {
  background: var(--dwi-surface);
  border: 1px solid var(--dwi-border);
  border-radius: var(--dwi-radius-lg);
  box-shadow: var(--dwi-shadow-sm);
  padding: 1rem;
}

@media (min-width: 768px) {
  .dwi-card {
    padding: 1.25rem;
  }
}
```

### Action card

```css
.dwi-action-card {
  display: block;
  height: 100%;
  background: var(--dwi-surface);
  border: 1px solid var(--dwi-border);
  border-radius: var(--dwi-radius-xl);
  padding: 1.25rem;
  text-decoration: none;
  color: var(--dwi-text);
  transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
}

.dwi-action-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--dwi-shadow-md);
  border-color: rgba(36, 71, 249, 0.35);
}
```

### Result card

```css
.dwi-result-card {
  background: var(--dwi-surface);
  border: 1px solid var(--dwi-border);
  border-radius: var(--dwi-radius-xl);
  box-shadow: var(--dwi-shadow-sm);
  overflow: hidden;
}

.dwi-result-section {
  padding: 1rem;
  border-bottom: 1px solid var(--dwi-border);
}

.dwi-result-section:last-child {
  border-bottom: 0;
}
```

---

## 7. Button System

### Primary button

```css
.btn-dwi-primary {
  background: var(--dwi-primary);
  border-color: var(--dwi-primary);
  color: #fff;
  border-radius: 999px;
  min-height: 44px;
  padding-inline: 1.25rem;
  font-weight: 700;
}

.btn-dwi-primary:hover {
  background: var(--dwi-primary-dark);
  border-color: var(--dwi-primary-dark);
  color: #fff;
}
```

### Secondary button

```css
.btn-dwi-secondary {
  background: var(--dwi-primary-soft);
  border-color: transparent;
  color: var(--dwi-primary-dark);
  border-radius: 999px;
  min-height: 44px;
  padding-inline: 1.25rem;
  font-weight: 700;
}
```

### Danger button

```css
.btn-dwi-danger {
  background: var(--dwi-danger-soft);
  border-color: transparent;
  color: var(--dwi-danger);
  border-radius: 999px;
  min-height: 44px;
  padding-inline: 1.25rem;
  font-weight: 700;
}
```

---

## 8. Form System

### Input styling

```css
.dwi-form-control {
  border-radius: var(--dwi-radius-md);
  border: 1px solid var(--dwi-border);
  min-height: 48px;
  padding: 0.75rem 1rem;
}

.dwi-form-control:focus {
  border-color: var(--dwi-primary);
  box-shadow: 0 0 0 0.2rem rgba(36, 71, 249, 0.12);
}
```

### Textarea

```css
.dwi-textarea {
  min-height: 180px;
  resize: vertical;
  line-height: 1.7;
}
```

### Upload box

```css
.dwi-upload-box {
  border: 2px dashed var(--dwi-border);
  border-radius: var(--dwi-radius-xl);
  background: var(--dwi-surface);
  padding: 1.5rem;
  text-align: center;
}

.dwi-upload-box:hover {
  border-color: var(--dwi-primary);
  background: var(--dwi-primary-soft);
}
```

---

## 9. Navigation System

### Top navbar

Requirements:

- Show dwi.ma logo/name.
- Show credit balance pill for authenticated user.
- Show login/pricing links for public user.

### Bottom nav

Authenticated mobile users should see bottom nav.

Items:

1. الرئيسية
2. وثيقة
3. نص
4. رسالة
5. الرصيد

CSS:

```css
.dwi-bottom-nav {
  position: fixed;
  z-index: 1030;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.96);
  border-top: 1px solid var(--dwi-border);
  backdrop-filter: blur(12px);
}

.dwi-bottom-nav a {
  min-height: 56px;
  color: var(--dwi-text-muted);
  text-decoration: none;
  font-size: 0.78rem;
  font-weight: 650;
}

.dwi-bottom-nav a.active {
  color: var(--dwi-primary);
}
```

---

## 10. Badge System

```css
.dwi-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  border-radius: 999px;
  padding: 0.35rem 0.65rem;
  font-size: 0.8rem;
  font-weight: 700;
}

.dwi-badge-success {
  background: var(--dwi-success-soft);
  color: var(--dwi-accent-dark);
}

.dwi-badge-warning {
  background: var(--dwi-warning-soft);
  color: #92400e;
}

.dwi-badge-danger {
  background: var(--dwi-danger-soft);
  color: var(--dwi-danger);
}

.dwi-badge-neutral {
  background: var(--dwi-surface-soft);
  color: var(--dwi-text-muted);
}
```

---

## 11. Alerts and Trust Notes

### Consent box

```css
.dwi-consent-box {
  background: var(--dwi-warning-soft);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: var(--dwi-radius-lg);
  padding: 1rem;
}
```

### Privacy note

```css
.dwi-privacy-note {
  background: var(--dwi-accent-soft);
  border: 1px solid rgba(16, 185, 129, 0.24);
  border-radius: var(--dwi-radius-lg);
  padding: 1rem;
  color: var(--dwi-accent-dark);
}
```

### Error state

```css
.dwi-error-state {
  background: var(--dwi-danger-soft);
  border: 1px solid rgba(239, 68, 68, 0.24);
  border-radius: var(--dwi-radius-lg);
  padding: 1rem;
  color: var(--dwi-danger);
}
```

---

## 12. Result Section Design

Use this structure for AI outputs:

```html
<div class="dwi-result-card">
  <section class="dwi-result-section">
    <p class="dwi-small text-muted mb-1">نوع الوثيقة</p>
    <h2 class="dwi-title-md mb-0">{{ document_type }}</h2>
  </section>

  <section class="dwi-result-section">
    <h3 class="h6 fw-bold">الخلاصة</h3>
    <p class="mb-0">{{ summary }}</p>
  </section>
</div>
```

For lists:

```html
<ul class="dwi-clean-list">
  <li>...</li>
</ul>
```

```css
.dwi-clean-list {
  padding-left: 1.2rem;
  margin-bottom: 0;
}

.dwi-clean-list li {
  margin-bottom: 0.5rem;
}
```

---

## 13. Page-Specific Patterns

### Dashboard

Use a top greeting card and three action cards.

```text
سلام 👋 شنو بغيتي ندير ليك اليوم؟
```

Action cards:

- شرح ليا وثيقة
- شرح ليا نص
- كتب ليا رسالة

### Document Upload

Use upload card + consent card + credit note.

### Result Pages

Use structured sections + sticky action area on mobile if useful.

### Wallet

Use balance hero card + pricing cards.

### Payment Status

Use clear success/failure states with icons and next actions.

---

## 14. Icon Guidance

Use simple line icons from Bootstrap Icons or Lucide if available.

Suggested icons:

- Document: file-text
- Text: type
- Message: message-square
- Wallet: wallet
- WhatsApp: message-circle / whatsapp if available
- Upload: upload-cloud
- Copy: copy
- Delete: trash
- Success: check-circle
- Warning: alert-triangle
- Error: x-circle

Do not use too many icons. Icons should support clarity, not decorate everything.

---

## 15. Motion and Interaction

Keep motion subtle.

Allowed:

```css
transition: all 160ms ease;
```

Use for:

- Button hover
- Card hover
- Toast appearance
- Accordion open/close

Avoid:

- Heavy animations
- Long delays
- Distracting motion
- Animation that blocks usage

---

## 16. Responsive Breakpoints

Use Bootstrap breakpoints:

- xs: mobile default
- md: tablets
- lg: desktop
- xl: wide desktop

Patterns:

Mobile:

- Single column
- Bottom nav
- Large cards

Desktop:

- Two/three-column grid
- More spacing
- Optional sidebar later

---

## 17. Empty State Design

Empty state component:

```html
<div class="dwi-empty-state text-center">
  <div class="dwi-empty-icon">...</div>
  <h3>مازال ما كاين والو هنا</h3>
  <p>جرب أول عملية باش تبان النتيجة هنا.</p>
  <a href="..." class="btn btn-dwi-primary">بدا دابا</a>
</div>
```

CSS:

```css
.dwi-empty-state {
  background: var(--dwi-surface);
  border: 1px dashed var(--dwi-border);
  border-radius: var(--dwi-radius-xl);
  padding: 2rem 1rem;
}
```

---

## 18. Loading State Design

```html
<div class="dwi-loading-state text-center">
  <div class="spinner-border text-primary" role="status"></div>
  <h2 class="h5 mt-3">كنوجدو النتيجة ديالك…</h2>
  <p class="text-muted">هاد العملية ممكن تاخذ شوية الوقت.</p>
</div>
```

---

## 19. Feedback Buttons

Use four quick feedback actions:

```text
عاوناتني
ما واضحةش
فيها خطأ
خاصها مراجعة
```

Style:

- Helpful: success soft
- Unclear: warning soft
- Wrong/unsafe: danger soft
- Review: neutral

---

## 20. Final Design Checklist

Before considering frontend complete:

- Mobile layout works.
- Desktop layout works.
- Bottom nav works.
- Credit balance is visible.
- Primary actions are clear.
- Consent is visible.
- Delete is confirmed.
- Results are structured.
- Copy buttons work.
- Empty states exist.
- Loading states exist.
- Error states are safe.
- Payment pages are transparent.
- PWA does not cache sensitive data.
