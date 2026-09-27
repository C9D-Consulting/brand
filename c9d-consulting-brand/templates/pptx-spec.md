# PowerPoint Template Spec

> **STATUS: PROPOSED, NOT LOCKED.**
> 
> This template specification is Claude's structured application of The Dossier system to this output format. It was NOT in the locked §9 Visual Identity Doc or §10 Product/Offering Doc source artifacts. The locked source documented the brand foundation, visual tokens, voice library, and engagement architecture — not format-specific templates.
> 
> Treat this file as a starting point for discussion with Brandon, not as locked system. Specific patterns flagged below as **[proposed]** are derivable from locked tokens and rules; structures flagged as **[invented]** were created for this file and have no source. Review and lock with Brandon before treating as system.


The Dossier system applied to slide decks. Slides are still slides, but the chrome, typography, color, and composition are treated as document, not marketing.

When creating a C9D Consulting deck, use the generic `pptx` skill for mechanics (python-pptx, slide layouts, image insertion) and layer this spec on top for the brand decisions.

---

## When to use which slide type

Five slide types cover every deck. Resist adding more.

| Type | Use | Typical count per deck |
|---|---|---|
| S-01 Cover | Opening slide, identifies the document | 1 |
| S-02 Metadata | Document chrome: file ID, classification, date, prepared-by, audience | 1 |
| S-03 Section divider | Marks a major section transition | 1 per section |
| S-04 Content | The body work: findings, framework, decision register, comparison | varies |
| S-05 Close | Closing slide with the manifesto closer | 1 |

A 15-slide deck typically: 1 cover + 1 metadata + 3 section dividers + 9 content + 1 close.

---

## Slide dimensions

**Aspect ratio:** 16:9 (widescreen 13.333 × 7.5 inches).

**Safe margins:** 0.5 inch from each edge for content area; chrome occupies the outer 0.4 inch.

**Grid:** 12-column grid with 0.25 inch gutters. Content typically uses 8 or 10 of the 12 columns; full-bleed is reserved for diagrams.

---

## Slide chrome (every slide except S-01 cover and S-05 close)

Every working slide carries the same chrome at top and bottom. The chrome is what makes the deck read as document.

### Top chrome (header bar)

A horizontal strip across the top, 0.4 inch tall. From left to right:

- Left: file ID in JetBrains Mono, 9pt, `--ink-mute` color. Format: `FILE-[ENGAGEMENT]-[YEAR]-[NUM]` (e.g., `FILE-E01-2026-014`).
- Center-left: classification stamp. Inter Tight uppercase 8pt with letter-spacing 0.18em, in `--stamp` color. Examples: `OPERATING EVIDENCE`, `CLIENT CONFIDENTIAL`, `INTERNAL DRAFT`.
- Center-right: section marker. JetBrains Mono 9pt, `--ink-mute`. Format: `§ 01 — STRATEGIC FOUNDATION`.
- Right: page number. JetBrains Mono 9pt, `--ink-mute`. Format: `01 / 15` (current of total).

A 0.5pt `--rule` hairline runs below the top chrome.

### Bottom chrome (footer bar)

A horizontal strip across the bottom, 0.4 inch tall. From left to right:

- Left: C9D Consulting wordmark, 12pt. Inter Tight 400 with "C9D" in `--stamp` color and "Consulting" in `--ink`.
- Center: "A practice of Brandon Wilburn" (no terminal period; `naming.founder.attribution` in `tokens.json`). Inter Tight 9pt, `--ink-mute`.
- Right: c9d.consulting in JetBrains Mono 9pt, `--ink-mute`.

A 0.5pt `--rule` hairline runs above the bottom chrome.

---

## S-01 Cover slide

The cover is the only slide without the chrome. It carries the document's full identity.

**Composition:**

- Background: `--bg` solid.
- Top-left, 0.6 inch from each edge: file ID and classification stamp on two lines. JetBrains Mono 11pt for the file ID in `--ink-mute`; Inter Tight uppercase 9pt with letter-spacing 0.18em in `--stamp` for the classification.
- Vertical center, left-aligned starting 0.6 inch from left: the document title in Inter Tight 56pt weight 300, color `--ink-bright`. Maximum two lines, tight letter-spacing -0.04em.
- Below the title, 0.4 inch gap: a 1pt `--rule-bright` line spanning 4 columns.
- Below the line, 0.3 inch gap: the document subtitle or descriptor in Inter Tight 22pt weight 350, color `--ink-mute`. One line.
- Bottom-left, 0.6 inch from each edge: prepared-by block. Three lines in Inter Tight 12pt. Line 1: "Prepared by" in `--ink-mute`. Line 2: "Brandon Wilburn" in `--ink-bright`. Line 3: "C9D Consulting" in `--ink-bright` with "C9D" in `--stamp`.
- Bottom-right, 0.6 inch from each edge: date and version block. JetBrains Mono 10pt. Two lines: date (`2026.06.17`) in `--ink-mute`, version (`v1.0`) in `--ink-mute`.

---

## S-02 Metadata slide

Always slide 2. Carries the document's structural metadata so the reader knows what they're holding before reading the work.

**Composition:**

- Standard top/bottom chrome.
- Centered, occupying 8 of 12 columns: a five-row metadata table. Each row is a `--rule` hairline separated cell pair. Inter Tight 14pt for body, JetBrains Mono 11pt for keys.

**Rows:**

| Key (mono) | Value (Inter Tight) |
|---|---|
| `DOCUMENT` | The full title |
| `PREPARED FOR` | Client name or audience |
| `PREPARED BY` | Brandon Wilburn, C9D Consulting |
| `CLASSIFICATION` | Operating Evidence / Client Confidential / etc. |
| `VERSION` | Version number and date |

---

## S-03 Section divider

Marks a transition into a major section. Should appear before every multi-slide section.

**Composition:**

- Background: `--bg-2` solid (slightly elevated from the `--bg` of content slides).
- Standard top/bottom chrome.
- Center-left, occupying columns 2–8:
  - Eyebrow: JetBrains Mono uppercase 12pt with letter-spacing 0.18em, in `--stamp-dim`. Format: `SECTION 01`.
  - Below the eyebrow, 0.3 inch gap: section title in Inter Tight 48pt weight 300, color `--ink-bright`. Letter-spacing -0.04em.
  - Below the title, 0.4 inch gap: a 1pt `--rule-bright` line spanning 3 columns.
  - Below the line, 0.3 inch gap: section description in Inter Tight 18pt weight 400, color `--ink-mute`. Maximum three lines.

---

## S-04 Content slides

The body slides. Five sub-types cover almost every content situation.

### S-04a — Single-claim slide

One headline claim, supporting body, optional pullquote. The default content slide.

**Composition:**

- Standard chrome.
- Top of content area: a JetBrains Mono eyebrow tag in `--stamp-dim`, 10pt, letter-spacing 0.18em. Example: `FINDING 01` or `THE PLAYBOOK` or `DECISION POINT`.
- Below: the claim in Inter Tight 32pt weight 300, color `--ink-bright`. Maximum two lines. Letter-spacing -0.03em.
- Below the claim, 0.6 inch gap: body copy in Inter Tight 16pt weight 400, color `--ink`. Maximum 65 characters per line. Multiple paragraphs separated by 0.2 inch.
- Optional pullquote at right (columns 9–12): Instrument Serif italic 22pt in `--stamp`. Maximum 8 words.

### S-04b — Two-column comparison

Use when the slide compares two postures, two options, or two states (before/after).

**Composition:**

- Standard chrome.
- Title row at top: Inter Tight 24pt weight 300, color `--ink-bright`. One line.
- Two columns separated by a vertical `--rule` hairline. Each column has a JetBrains Mono uppercase header in `--stamp` (10pt, letter-spacing 0.18em), then the content in Inter Tight 14pt weight 400 `--ink`.

Refuse: side-by-side cards with rounded corners. Use hairlines, not cards.

### S-04c — Decision register / risk register / table

Tables are first-class citizens in The Dossier. They appear often. Use the format.

**Composition:**

- Standard chrome.
- Title row at top: Inter Tight 22pt weight 300 `--ink-bright`. One line.
- Below title, 0.4 inch gap: optional subtitle in Inter Tight 13pt weight 400 `--ink-mute`.
- Below subtitle, 0.5 inch gap: the table. Header row in JetBrains Mono uppercase 10pt with letter-spacing 0.18em, color `--stamp-dim`. Body rows in Inter Tight 13pt weight 400 `--ink`. Row separator: 0.5pt `--rule` hairline. No vertical lines. No alternating row backgrounds.
- Status cells use the color system: open = `--stamp`, resolved = `--ink-mute`, refused = `--classified`, critical = `--classified`.

### S-04d — Diagram / framework

Schematic illustration of a framework, decision tree, or system. Composition is illustration-specific, but the typography rules apply: labels in JetBrains Mono uppercase 9pt with letter-spacing 0.18em in `--ink-mute`, key concepts in Inter Tight 14pt weight 400 in `--ink-bright`, the load-bearing element in `--stamp`.

### S-04e — Pullquote / manifesto excerpt

Used sparingly: one or two pullquote slides per deck. The slide carries a 1–3 sentence excerpt from the manifesto or a load-bearing claim.

**Composition:**

- Standard chrome.
- Centered, columns 3–10: a single open quotation mark in Instrument Serif italic 88pt, color `--stamp-dim`, positioned at the top-left of the text block.
- Quote text in Inter Tight 28pt weight 300 color `--ink-bright`. Maximum three lines.
- Below the quote, 0.4 inch gap: attribution in JetBrains Mono uppercase 10pt with letter-spacing 0.18em in `--stamp-dim`. Format: `FROM THE MANIFESTO` or `BRANDON WILBURN, FOUNDER`.

---

## S-05 Close slide

The closing slide always carries the same closer. The phrase is locked.

**Composition:**

- Background: `--bg` solid (no chrome).
- Vertical center, left-aligned starting 0.6 inch from left:
  - Inter Tight 32pt weight 300 color `--ink-bright`: "We have shipped what we recommend."
  - 0.3 inch gap.
  - Inter Tight 32pt weight 300 color `--stamp`: "Coordinated, not improvised."
- Bottom-left, 0.6 inch from each edge: the wordmark and attribution block (same as the cover but inverted: wordmark first, then "A practice of Brandon Wilburn" in `--ink-mute`).
- Bottom-right, 0.6 inch from each edge: c9d.consulting in JetBrains Mono 10pt `--ink-mute`.

---

## Refused PowerPoint patterns

- Bullet-point slides with 5+ bullets per slide (use prose or a structured pattern)
- Title-case slide titles (sentence-case only)
- Stock photography people or hand-shake imagery
- Animated reveals, slide transitions, or build-by-click sequences in the document version
- The default "Office" theme color accents (blue, orange, green)
- "Thank you" or "Questions?" final slides (the close slide carries the manifesto closer)
- Headers using a serif on body slides; serif is reserved for italic accent and pullquotes only
- Footer page numbers without the JetBrains Mono treatment and `--ink-mute` color
- Charts using the default Office color palette; chart colors derive from the amber-and-shades palette

---

## Production notes

When generating with python-pptx:

```python
# Color tokens
BG = RGBColor(0x0c, 0x0b, 0x08)
BG_2 = RGBColor(0x13, 0x12, 0x10)
BG_3 = RGBColor(0x1a, 0x18, 0x15)
RULE = RGBColor(0x2a, 0x26, 0x20)
RULE_BRIGHT = RGBColor(0x3d, 0x36, 0x2c)
INK_BRIGHT = RGBColor(0xf0, 0xe6, 0xd0)
INK = RGBColor(0xd8, 0xcd, 0xb8)
INK_MUTE = RGBColor(0x8a, 0x7e, 0x6a)
INK_DIM = RGBColor(0x5a, 0x50, 0x42)
STAMP = RGBColor(0xd6, 0x74, 0x3a)
STAMP_DIM = RGBColor(0x8a, 0x48, 0x24)
CLASSIFIED = RGBColor(0xc0, 0x39, 0x2b)
```

Set the slide master background to `BG`. Configure default text frames with the Inter Tight font; document-mono frames with JetBrains Mono. The fonts need to be installed in the rendering environment or referenced as fallbacks; do not assume them present without checking. If Inter Tight is unavailable, fall back to Inter, then Helvetica, then system sans. If JetBrains Mono is unavailable, fall back to IBM Plex Mono, then Menlo, then monospace.
