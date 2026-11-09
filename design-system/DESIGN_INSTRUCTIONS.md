# dwi.ma Design System v2 — Instructions

## Identity

dwi.ma is a Moroccan Darija AI utility. The design expresses **trustworthy clarity** — a tool that feels local and approachable, not a Silicon Valley chatbot. Think government kiosk reimagined by a boutique agency: structured, warm, culturally rooted.

## Style: Refined Moroccan Minimalism

Clean geometry inspired by zellige tilework, warm stone-toned neutrals, and generous whitespace. Not brutalist, not glassmorphic — **calm and grounded** with moments of color that feel intentional.

---

## Typography

| Role    | Font                | Weight    | Fallback              |
|---------|---------------------|-----------|------------------------|
| Display | Noto Naskh Arabic   | 700       | IBM Plex Sans Arabic, serif |
| Body    | Noto Sans Arabic    | 400–600   | IBM Plex Sans Arabic, system-ui |
| Mono    | IBM Plex Mono       | 400       | Fira Code, monospace   |

**Rules:**
- Body: 15px (0.9375rem), line-height 1.6
- Display headings use `--dw-font-display` (Naskh serif) for warmth
- Body text uses `--dw-font-body` (Sans) for readability
- Never set body text below 13px
- Use `clamp()` for responsive heading sizes

## Colors

### Primary: Teal (trust, institutional, Moroccan green)
`--dw-teal-500: #0d7963` — primary actions, active states
`--dw-teal-600: #0b6b58` — buttons, links
`--dw-teal-50: #eef8f6` — subtle backgrounds

### Accent: Amber (warmth, energy, Moroccan craft)
`--dw-amber-500: #f59e0b` — CTA buttons, credit badges
`--dw-amber-50: #fffbeb` — subtle backgrounds

### Neutrals: Warm Stone
From `--dw-gray-50: #fafaf9` to `--dw-gray-900: #1c1917`
These are stone-toned, not blue-gray — they feel warm and human.

### Semantic
- Success: `#16a34a` / bg `#f0fdf4`
- Warning: `#ea580c` / bg `#fff7ed`
- Danger: `#dc2626` / bg `#fef2f2`
- Info: `#0284c7` / bg `#f0f9ff`

**Rules:**
- Always use CSS custom properties, never raw hex in templates
- The `dw-card-icon-*` classes provide consistent icon backgrounds
- Error states use `var(--dw-danger-bg)` background, not raw `#fef2f2`

## Spacing & Layout

- 8px base grid: all spacing is multiples of 4px/8px
- `--dw-radius-sm: 6px` — inputs, small chips
- `--dw-radius-md: 10px` — cards, buttons
- `--dw-radius-lg: 14px` — cards
- `--dw-radius-xl: 20px` — modals, hero cards
- Max content width: 600px (`dw-app-container`)
- Padding: 16px mobile, 24px desktop

## Shadows

Five levels, all warm-toned (stone rgba, not black):
- `--dw-shadow-xs` — resting cards
- `--dw-shadow-sm` — elevated cards
- `--dw-shadow-md` — hover states
- `--dw-shadow-lg` — modals, toasts
- `--dw-shadow-glow` — focus rings (teal)

## Components

### Cards (`dw-card`)
- White surface, 1px border `var(--dw-border)`, `dw-shadow-xs`
- Interactive cards (`dw-card-interactive`) get `cursor: pointer`, hover shadow + teal border, press scale 0.98
- Card icons: 44×44px rounded square, subtle tinted background

### Buttons (`dw-btn`)
- Min height 44px (touch target)
- Variants: `primary` (teal), `secondary` (gray), `amber`, `outline`, `ghost`, `danger`
- Sizes: `sm` (36px), default (44px), `lg` (52px)
- All buttons get `active` scale, `focus-visible` ring, `disabled` opacity
- Never use a button without a variant class

### Badges (`dw-badge`)
- Pill-shaped, semantic colors
- Add `dw-badge-dot` for status dot prefix
- Processing badge has animated pulsing dot

### Toasts (`dw-toast`)
- Left/start border color indicates type
- Auto-dismiss in 5s
- Enter from top with scale+opacity animation
- `aria-live="polite"` on container

### Forms
- Inputs: 1.5px border, 10px radius, teal focus glow
- Labels above inputs, always visible (never placeholder-only)
- Error hint below field in danger color
- Checkboxes/radios use `accent-color: teal`

## Animation

### Timings
- Micro-interactions: 150–200ms ease
- Page entrance: 450ms cubic-bezier(0.16, 1, 0.3, 1)
- Stagger: 80ms between items (not 50ms — it needs to be perceptible)

### Motion
- `dw-fade-in` + `dw-stagger-N` for page load sequences
- Card hover: shadow + border transition (200ms ease)
- Button press: scale(0.97) on active
- Spinner: 650ms linear rotation

### Reduced Motion
All animations respect `prefers-reduced-motion: reduce` — durations collapse to 0.01ms.

## Zellige Pattern

The `.dw-pattern-bg` class adds a geometric zellige-inspired overlay at 4.5% opacity. Use it on:
- Public pages (landing, login, register) via `base_public.html`
- The dashboard credit card

Do NOT use it on every card — it's a background treatment, not a texture.

## RTL & Darija

- All layouts are `dir="rtl"` by default
- Use `padding-inline-start/end`, not `padding-left/right`
- Bootstrap RTL handles grid/flex direction
- `dw-select` dropdown arrow is positioned for RTL via `background-position: left`
- Font loading includes Arabic-specific optical sizes

## Accessibility

- Focus rings: 2px solid teal, 2px offset on all interactive elements
- Color contrast: minimum 4.5:1 for body text
- Touch targets: minimum 44×44px
- `::selection` styled with teal tint
- Screen reader utilities: `dw-sr-only`
- Toast container uses `aria-live="polite"`
- All icon-only buttons need `aria-label`

## Anti-Patterns (Never Do)

1. **No raw hex colors in templates** — always use `var(--dw-*)` tokens
2. **No emoji as icons** — use Lucide-style inline SVGs
3. **No text below 12px** except legal fine print
4. **No hover-only interactions** — everything must work on tap
5. **No blocking animations** — UI stays interactive during motion
6. **No identical stagger delays** on sequential items — use 80ms+ gaps
7. **No generic fonts** (Inter, Arial, Roboto) — the Arabic fonts ARE the personality
8. **No Material Design shadows** — use the warm stone-toned shadow scale
9. **No color-only status indicators** — always pair with icon or text
10. **No inline JavaScript for hover effects** — use CSS transitions
