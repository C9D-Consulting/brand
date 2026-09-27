# Web Template Spec

> **STATUS: PROPOSED, NOT LOCKED.**
> 
> This template specification is Claude's structured application of The Dossier system to this output format. It was NOT in the locked §9 Visual Identity Doc or §10 Product/Offering Doc source artifacts. The locked source documented the brand foundation, visual tokens, voice library, and engagement architecture — not format-specific templates.
> 
> Treat this file as a starting point for discussion with Brandon, not as locked system. Specific patterns flagged below as **[proposed]** are derivable from locked tokens and rules; structures flagged as **[invented]** were created for this file and have no source. Review and lock with Brandon before treating as system.


The Dossier system applied to web surfaces. The external marketing site (c9d.consulting) and internal tooling (engagement workspaces, status pages, client portals). Dark mode default; light mode for print-only artifacts served from the web.

When building a C9D Consulting web surface, this spec carries the design decisions. Tokens are available in `assets/tokens.css` (drop-in stylesheet) and `assets/tokens.json` (for design tooling).

---

## Surface types

| Type | Use | Mode |
|---|---|---|
| W-01 External marketing site | c9d.consulting — public surface | Dark |
| W-02 Internal status page | Engagement status, client-facing tracker | Dark |
| W-03 Engagement workspace | Internal Brandon-only operating surface | Dark |
| W-04 Print artifact (HTML to PDF) | Engagement letters, signed SOWs | Light |
| W-05 Email-as-web (rendered HTML emails) | HTML emails styled as document fragments | Dark |

---

## Foundational HTML head

Every C9D Consulting HTML page includes the same head setup:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Page title] · C9D Consulting</title>
  <meta name="description" content="[Page-specific description]">
  
  <!-- Open Graph -->
  <meta property="og:title" content="[Page title] · C9D Consulting">
  <meta property="og:description" content="[Description]">
  <meta property="og:image" content="https://c9d.consulting/og-image.jpg">
  <meta property="og:type" content="website">
  
  <!-- Font preloads -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@200;300;350;400;450;500&family=Instrument+Serif:ital@1&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <!-- Brand tokens -->
  <link rel="stylesheet" href="/css/tokens.css">
  <link rel="stylesheet" href="/css/base.css">
</head>
```

---

## CSS base layer

Drop-in base stylesheet that establishes the document-grade defaults.

```css
* { box-sizing: border-box; margin: 0; padding: 0; }

html {
  background: var(--bg);
  color: var(--ink);
  font-family: 'Inter Tight', Inter, -apple-system, system-ui, sans-serif;
  font-size: 16px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  background: var(--bg);
  color: var(--ink);
  font-feature-settings: 'ss01', 'cv11';
  min-height: 100vh;
}

h1, h2, h3, h4 {
  font-family: 'Inter Tight', sans-serif;
  font-weight: 300;
  letter-spacing: -0.03em;
  color: var(--ink-bright);
  line-height: 1.1;
}

p { color: var(--ink); max-width: 65ch; }

a { color: var(--stamp); text-decoration: none; border-bottom: 1px solid var(--stamp-dim); }
a:hover { border-bottom-color: var(--stamp); }

code, pre, .mono {
  font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;
  font-size: 0.85em;
  letter-spacing: 0.02em;
}

em, .italic-accent {
  font-family: 'Instrument Serif', serif;
  font-style: italic;
  font-weight: 400;
}
```

---

## Layout primitives

### The page

```html
<div class="page">
  <header class="chrome chrome--top">...</header>
  <main class="content">...</main>
  <footer class="chrome chrome--bottom">...</footer>
</div>
```

```css
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1;
  max-width: 1280px;
  margin: 0 auto;
  padding: var(--space-7) var(--space-6);
  width: 100%;
}
```

### The chrome (top and bottom)

The chrome carries the document framing on every page except the cover/landing.

**Top chrome (header):**

```html
<header class="chrome chrome--top">
  <div class="chrome__cell chrome__cell--left">
    <span class="mono">FILE-E01-2026-014</span>
  </div>
  <div class="chrome__cell chrome__cell--center">
    <span class="stamp">OPERATING EVIDENCE</span>
  </div>
  <div class="chrome__cell chrome__cell--right">
    <span class="mono">§ 04 · 14 / 42</span>
  </div>
</header>
```

```css
.chrome {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  padding: var(--space-3) var(--space-6);
  border-bottom: 1px solid var(--rule);
  font-size: 11px;
}

.chrome--bottom { border-bottom: 0; border-top: 1px solid var(--rule); }

.chrome__cell--center { text-align: center; }
.chrome__cell--right { text-align: right; }

.mono { font-family: 'JetBrains Mono', monospace; color: var(--ink-mute); font-size: 11px; }

.stamp {
  font-family: 'Inter Tight', sans-serif;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--stamp);
  font-size: 10px;
}
```

### Hero (W-01 landing)

The landing hero is the most visible surface. Composition matches the cover of a Word document.

```html
<section class="hero">
  <div class="hero__meta">
    <span class="mono">C9D-PRACTICE-2026</span>
    <span class="stamp">OPERATING EVIDENCE</span>
  </div>
  <h1 class="hero__title">Fractional leadership for the work that gets tested.</h1>
  <hr class="rule rule--bright">
  <p class="hero__subtitle">A practice for Series B-to-D companies navigating the platform-rebuild wall, the AI-adoption decision, and the diligence moment. We have shipped what we recommend.</p>
  <p class="hero__closer italic-accent">Coordinated, not improvised.</p>
</section>
```

```css
.hero {
  padding: var(--space-9) 0 var(--space-8);
  max-width: 900px;
}

.hero__meta {
  display: flex;
  gap: var(--space-5);
  margin-bottom: var(--space-7);
}

.hero__title {
  font-size: clamp(48px, 7vw, 88px);
  font-weight: 300;
  letter-spacing: -0.04em;
  line-height: 1.05;
  color: var(--ink-bright);
}

.hero__subtitle {
  font-size: 22px;
  font-weight: 400;
  color: var(--ink);
  margin-top: var(--space-5);
  max-width: 65ch;
}

.hero__closer {
  font-family: 'Instrument Serif', serif;
  font-style: italic;
  font-size: 28px;
  color: var(--stamp);
  margin-top: var(--space-6);
}

.rule {
  border: none;
  height: 1px;
  background: var(--rule);
  margin: var(--space-5) 0;
  width: 240px;
}

.rule--bright { background: var(--rule-bright); }
```

### Section divider

```html
<section class="section">
  <div class="section__eyebrow mono">SECTION 01</div>
  <h2 class="section__title">Strategic Foundation</h2>
  <hr class="rule rule--bright">
  <p class="section__intro">The work the practice is committed to. Read this before any engagement description.</p>
</section>
```

```css
.section { padding: var(--space-8) 0; border-bottom: 1px solid var(--rule); }

.section__eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--stamp-dim);
  margin-bottom: var(--space-4);
}

.section__title {
  font-size: clamp(36px, 5vw, 56px);
  font-weight: 300;
  letter-spacing: -0.03em;
  color: var(--ink-bright);
}

.section__intro {
  margin-top: var(--space-5);
  font-size: 18px;
  color: var(--ink-mute);
  max-width: 65ch;
}
```

### Content blocks

A content block is the unit of body work on the site. Each block has an eyebrow tag, a claim, and supporting body.

```html
<article class="block">
  <div class="block__eyebrow mono">FINDING 01</div>
  <h3 class="block__claim">The platform rebuild is one decision, not three.</h3>
  <div class="block__body">
    <p>Most platform-rebuild decisions get split into a re-architecture decision, a re-staffing decision, and a re-platforming decision. The split feels analytical; it is the opposite. The three decisions interact, and pretending they don't is the source of most rebuilds that miss.</p>
    <p>The work of E-01 is to surface the interaction explicitly, and decide once.</p>
  </div>
</article>
```

```css
.block { margin-bottom: var(--space-7); max-width: 750px; }

.block__eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--stamp);
  margin-bottom: var(--space-3);
}

.block__claim {
  font-size: 28px;
  font-weight: 300;
  letter-spacing: -0.03em;
  color: var(--ink-bright);
  margin-bottom: var(--space-4);
}

.block__body p { margin-bottom: var(--space-3); color: var(--ink); }
```

### The engagement card

Used to introduce each of E-01, E-02, E-03, R-01. Composition is restrained: no cards with shadows; the hairlines do the framing.

```html
<article class="engagement">
  <div class="engagement__meta">
    <span class="mono">E-01</span>
    <span class="stamp">PRODUCTIZATION ENGAGEMENT</span>
  </div>
  <h3 class="engagement__name">Take a shipped system and prepare it for the next set of conditions.</h3>
  <p class="engagement__body">Multi-tenancy, scaling, security posture, the operational discipline that survives an acquirer's counterparts pulling on the threads.</p>
  <dl class="engagement__detail">
    <div class="engagement__row">
      <dt class="mono">PRICING</dt>
      <dd>From $185,000 · fixed scope · fixed price</dd>
    </div>
    <div class="engagement__row">
      <dt class="mono">LEAD OPERATOR</dt>
      <dd>Brandon Wilburn</dd>
    </div>
    <div class="engagement__row">
      <dt class="mono">TYPICAL DURATION</dt>
      <dd>8–14 weeks</dd>
    </div>
  </dl>
</article>
```

```css
.engagement {
  padding: var(--space-6);
  background: var(--bg-2);
  border: 1px solid var(--rule);
  margin-bottom: var(--space-5);
}

.engagement__meta { display: flex; gap: var(--space-3); margin-bottom: var(--space-4); }

.engagement__name {
  font-size: 24px;
  font-weight: 300;
  letter-spacing: -0.02em;
  color: var(--ink-bright);
  margin-bottom: var(--space-3);
}

.engagement__body { color: var(--ink); margin-bottom: var(--space-5); }

.engagement__detail { display: grid; gap: var(--space-2); }

.engagement__row {
  display: grid;
  grid-template-columns: 180px 1fr;
  gap: var(--space-4);
  padding: var(--space-2) 0;
  border-bottom: 1px solid var(--rule);
}

.engagement__row:last-child { border-bottom: 0; }

.engagement__row dt {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--stamp-dim);
}

.engagement__row dd { color: var(--ink); }
```

### Tables

Tables in the web layer are the same as in Word and Excel: hairlines, no card chrome, header in JetBrains Mono uppercase.

```css
table { width: 100%; border-collapse: collapse; }

th {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--stamp-dim);
  text-align: left;
  font-weight: 600;
  padding: var(--space-3) var(--space-3);
  border-bottom: 1px solid var(--rule-bright);
}

td {
  padding: var(--space-3);
  color: var(--ink);
  font-size: 14px;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}

tr:last-child td { border-bottom: 0; }
```

---

## Buttons / CTAs

The site has minimal CTAs. The primary CTA is restrained, not marketing-loud.

```html
<a href="/contact" class="cta">Open a diagnostic call</a>
```

```css
.cta {
  display: inline-block;
  padding: var(--space-3) var(--space-5);
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-weight: 600;
  background: var(--stamp);
  color: var(--bg);
  border: 1px solid var(--stamp);
  border-radius: 0;
  transition: background 0.15s ease;
}

.cta:hover { background: var(--stamp-dim); border-color: var(--stamp-dim); }

.cta--secondary {
  background: transparent;
  color: var(--ink-bright);
  border: 1px solid var(--rule-bright);
}

.cta--secondary:hover {
  background: var(--bg-2);
  border-color: var(--stamp-dim);
}
```

---

## Footer (every page)

```html
<footer class="site-footer">
  <div class="site-footer__brand">
    <span class="wordmark"><span class="wordmark__c9d">C9D</span> Consulting</span>
    <span class="site-footer__attribution">A practice of Brandon Wilburn</span>
  </div>
  <div class="site-footer__meta">
    <span class="mono">c9d.consulting</span>
    <span class="mono">© 2026 C9D Consulting LLC</span>
  </div>
  <div class="site-footer__closer italic-accent">Coordinated, not improvised.</div>
</footer>
```

```css
.site-footer {
  padding: var(--space-8) var(--space-6) var(--space-7);
  border-top: 1px solid var(--rule);
  max-width: 1280px;
  margin: 0 auto;
}

.wordmark {
  font-family: 'Inter Tight', sans-serif;
  font-weight: 400;
  font-size: 18px;
  letter-spacing: -0.02em;
  color: var(--ink-bright);
}

.wordmark__c9d { color: var(--stamp); }

.site-footer__attribution {
  margin-left: var(--space-3);
  color: var(--ink-mute);
  font-size: 13px;
}

.site-footer__meta {
  display: flex;
  gap: var(--space-5);
  margin-top: var(--space-3);
  color: var(--ink-mute);
  font-size: 11px;
}

.site-footer__closer {
  margin-top: var(--space-5);
  font-family: 'Instrument Serif', serif;
  font-style: italic;
  font-size: 22px;
  color: var(--stamp);
}
```

---

## Refused web patterns

- Centered hero text with a centered CTA button (reads as marketing landing page)
- Three-column feature grids with icons above titles (reads as SaaS landing page)
- Carousels, marquees, animated reveals, or scroll-triggered animations beyond fade-in
- Rounded card corners > 4px
- Soft drop shadows on cards or buttons (use crisp 1px hairlines instead)
- Hero images of stock photography people
- Gradient buttons or gradient backgrounds
- Default browser blue link color (use `--stamp`)
- Underlined links with default underline (use `--stamp-dim` 1px border-bottom)
- The "modern Tailwind / shadcn" look that defaults to neutral grays and blue accents — the system is the opposite of that aesthetic

---

## Responsive notes

The system holds at all viewport widths. The chrome reduces to two cells (left and right) on viewports under 720px, dropping the center cell. The hero scales via `clamp()`. The engagement cards stack at narrow widths but retain the hairline framing.

Mobile-specific:
- Increase touch targets to 44px minimum height
- Increase padding inside cards from `--space-6` to `--space-5` on mobile
- Reduce hero title from `clamp(48px, 7vw, 88px)` to `clamp(36px, 8vw, 56px)` at viewports < 720px
- Replace `flex` chrome layout with `grid` collapsing to single column at < 480px
