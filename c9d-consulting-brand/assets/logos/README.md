# C9D Consulting — Logo Usage Guide

Production lockup set. Ten wordmark variants plus favicon exports. Drop-in ready for websites, materials, and social channels.

A practice of Brandon Wilburn.

---

## Which lockup to use

| If the context is… | Use |
|---|---|
| Website header on dark background | `c9d-consulting-wordmark-horizontal-dark.svg` |
| Website header on light background | `c9d-consulting-wordmark-horizontal-light.svg` |
| App icon, social avatar, square context (dark) | `c9d-consulting-wordmark-stacked-dark.svg` |
| App icon, social avatar, square context (light) | `c9d-consulting-wordmark-stacked-light.svg` |
| Single-color print, watermark, subtle contexts (dark) | `c9d-consulting-wordmark-mono-dark.svg` |
| Single-color print, letterhead engraving (light) | `c9d-consulting-wordmark-mono-light.svg` |
| Engagement letter, signed SOW cover, formal proposal (dark) | `c9d-consulting-endorsed-dark.svg` |
| Same, for printed formal deliverables | `c9d-consulting-endorsed-light.svg` |
| Campaign banner, hero image, opening slide with tagline | `c9d-consulting-with-tagline-dark.svg` |
| Favicon, browser tab, app icon at small sizes | `c9d-monogram-stamp.svg` |

**Default:** if in doubt, use the primary horizontal in the appropriate dark/light variant. That mark carries most contexts.

---

## Files in this directory

### SVG source files (scalable, use for web and design software)

- `c9d-consulting-wordmark-horizontal-dark.svg` — primary horizontal, dark bg
- `c9d-consulting-wordmark-horizontal-light.svg` — primary horizontal, light bg
- `c9d-consulting-wordmark-stacked-dark.svg` — stacked, dark bg
- `c9d-consulting-wordmark-stacked-light.svg` — stacked, light bg
- `c9d-consulting-wordmark-mono-dark.svg` — single-color mono, dark bg
- `c9d-consulting-wordmark-mono-light.svg` — single-color mono, light bg
- `c9d-consulting-endorsed-dark.svg` — with attribution, dark bg
- `c9d-consulting-endorsed-light.svg` — with attribution, light bg
- `c9d-consulting-with-tagline-dark.svg` — with primary tagline, dark bg
- `c9d-monogram-stamp.svg` — square monogram, sodium amber block

### PNG exports (raster, for platforms that don't accept SVG)

Primary wordmark exports at multiple sizes:
- `c9d-consulting-wordmark-horizontal-dark-600.png` — 600×133, dark bg baked in
- `c9d-consulting-wordmark-horizontal-dark-1200.png` — 1200×267, dark bg baked in
- `c9d-consulting-wordmark-horizontal-dark-transparent.png` — 900×200, transparent bg
- `c9d-consulting-wordmark-horizontal-light-600.png` — 600×133, cream bg baked in
- `c9d-consulting-wordmark-horizontal-light-1200.png` — 1200×267, cream bg baked in
- `c9d-consulting-wordmark-horizontal-light-transparent.png` — 900×200, transparent bg
- `c9d-consulting-wordmark-stacked-dark-800.png` — 400×267, dark bg baked in

Favicons and app icons:
- `c9d-favicon-16.png` — 16×16 (browser tab)
- `c9d-favicon-32.png` — 32×32 (browser tab)
- `c9d-favicon-48.png` — 48×48 (Windows tile)
- `c9d-favicon-64.png` — 64×64 (Android)
- `c9d-favicon-180.png` — 180×180 (Apple touch icon)
- `c9d-favicon-512.png` — 512×512 (PWA icon, high-DPI use)

### Reference

- `logo-showcase.html` — interactive showcase of all lockups with usage context
- `logo-showcase.png` — rendered preview of the showcase

---

## Font requirement

The wordmarks use **Inter Tight** (weight 400). Where the tagline lockup appears, it uses **Instrument Serif** italic (weight 400). Both are free from Google Fonts.

**For web:** The SVG files include `@import` for Inter Tight via Google Fonts. They will render correctly in any modern browser without additional setup.

**For design software (Figma, Illustrator, Sketch):** Install Inter Tight and Instrument Serif from Google Fonts first. Then open the SVG. If the fonts are missing, the software will substitute; the wordmark will look wrong.

**For print / when the design software's target must not depend on installed fonts:** Convert text to outlines/paths in your design software after opening the SVG. In Illustrator: select the text and Type → Create Outlines. In Figma: right-click text → Outline Stroke or Flatten. In Inkscape: Path → Object to Path.

Fonts:
- Inter Tight — https://fonts.google.com/specimen/Inter+Tight
- Instrument Serif — https://fonts.google.com/specimen/Instrument+Serif

---

## Web integration

### Favicon setup

In the `<head>` of any C9D Consulting page:

```html
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/favicon-180.png">
<link rel="manifest" href="/site.webmanifest">
```

### Header wordmark

The SVG is the right format for the site header — sharp at any DPI, tiny file size, load-once-cache-forever.

```html
<a href="/" class="site-logo">
  <img src="/logo/c9d-consulting-wordmark-horizontal-dark.svg"
       alt="C9D Consulting"
       width="300" height="67">
</a>
```

Set `width` and `height` attributes to prevent layout shift. The aspect ratio is 4.5:1 for the horizontal wordmark and 3:2 for the stacked.

### Open Graph / social share

For LinkedIn, X, and Slack unfurls, use the 1200×630 open-graph image. This directory does not include one; generate it by placing the horizontal wordmark on a `#0c0b08` background at 1200×630 with the wordmark centered vertically at ~600×133. The `logo-showcase.html` file can be adapted for this.

---

## Materials integration

### Letterhead

Use `c9d-consulting-wordmark-horizontal-light.svg` at ~2" (5cm) wide, positioned top-left with a 0.75" (2cm) margin. Below the wordmark, add "A practice of Brandon Wilburn." in Inter Tight 10pt Ink Mute (`#5a5042`). See the endorsed variants for the ready-made lockup.

### Business card

Front: `c9d-consulting-wordmark-stacked-light.svg` centered on the top half of the card. Back: address, engagement code lines (E-01 / E-02 / E-03 / R-01), and c9d.consulting in JetBrains Mono.

### Deck cover

`c9d-consulting-wordmark-horizontal-dark.svg` at the bottom-left corner, sized to about 1/6 of the slide width. See the `pptx-spec.md` template in this brand package for full deck chrome specification.

---

## Naming convention rules that apply to the logo

1. **Full form only in body copy.** "C9D Consulting" always. The wordmark itself is the visual form of the name; do not substitute "C9D" alone anywhere the wordmark isn't in play.

2. **Single exception: the favicon.** Space constraint at 16/32/48 px justifies the monogram. Nowhere else.

3. **Attribution is required on every major surface.** The endorsed lockup (L-07 / L-08) carries the attribution as part of the mark itself; if you're using a non-endorsed lockup, "A practice of Brandon Wilburn." must appear somewhere on the same surface (footer, byline, colophon).

4. **The wordmark colors are locked.** Sodium amber `#d6743a` for "C9D" (dark mode) or `#9c4f24` (light mode). Warm ink `#f0e6d0` for "Consulting" on dark, or `#1a1612` on light. No other color pairings.

5. **The tagline lockup is reserved.** Do not use L-09 as the default; it is a campaign moment. For most contexts, the tagline (or the closing line "Coordinated, not improvised.") appears elsewhere on the surface, not welded to the wordmark.

6. **Do not modify the wordmark.** No shadows, no glows, no outlines, no gradients. No skew or rotation. No monogram inside a hexagon, circle, or shield. The monogram inside the amber square (L-10) is the only sanctioned "mark inside a shape" form.

---

## Version

`v1.0 · 2026.08.01 · Logo System · The Dossier`

Coordinated, not improvised.
