# C9D Consulting — Gamma Reference Spec

A design and visualization spec for use with Gamma (gamma.app) when generating decks, documents, or web pages for C9D Consulting. Built to be copy-pasted into Gamma's additional-instructions field, used as a URL reference, or read alongside the Gamma generation tool.

The Dossier aesthetic fights every Gamma default. This spec exists to keep the brand on rails when Gamma's templates pull it off.

A practice of Brandon Wilburn.

---

## Quick reference card

Paste this card into Gamma's additional-instructions field as the minimum-viable brand application. The full spec below expands every line.

```
BRAND: C9D Consulting — AI Strategy Advisory for Series B-to-D companies. A practice of Brandon Wilburn.

AESTHETIC: The Dossier. Declassified document, not marketing site. Dark by default. Document-grade composition, not slide-deck decoration.

COLORS: warm near-black ground (#0c0b08, #131210, #1a1815), warm parchment ink (#f0e6d0, #d8cdb8, #8a7e6a), sodium amber as the only chromatic accent (#d6743a), classified red rationed for refusals only (#c0392b). Composition ratio: 70% ground / 22% ink / 6% amber / 2% red. No blue. No green. No purple.

TYPOGRAPHY: Inter Tight (display + body, weights 200–400, tight letter-spacing at large sizes). Instrument Serif italic (accent only, never body). JetBrains Mono (metadata, file IDs, classifications, page numbers, eyebrows above titles — roughly 40% of visible type surface).

EVERY SLIDE: top chrome (file ID, classification stamp, section marker, page number — all in JetBrains Mono or uppercase Inter Tight). Bottom chrome (wordmark, "A practice of Brandon Wilburn." attribution, c9d.consulting). Hairline rule separators. No card shadows. No rounded corners above 4px.

WORDMARK: "C9D" in sodium amber, "Consulting" in bright ink, weight 400, letter-spacing -0.04em. Never "C9D" alone.

TAGLINES: Primary "The playbook, not the deck." Alternate "We've shipped what we recommend." Campaign "AI strategy that survives the next round." These three are separate constructs.

CLOSING LINE (not a tagline, never substituted): "Coordinated, not improvised." Locked on the final slide.

REFUSED: bullet lists 5+ items, title case slide titles, stock photos of people, gradient backgrounds, rounded card corners, soft drop shadows, three-column feature grids, default Office or Google Slides chart colors, animated reveals, the words "transformation / journey / innovative / AI maturity model / AI center of excellence", em-dash overuse.
```

---

## What C9D Consulting is

C9D Consulting is positioned as an **AI Strategy Advisory** for Series B-to-D B2B SaaS, developer infrastructure, AI/ML, fintech, and data infrastructure companies. The differentiator is **post-shipping AI strategy**: every recommendation has been deployed in production at scale before it is offered as advice.

The brand positions explicitly against the AI strategist who has never shipped. In archetype terms, this is the Magician — the figure who turns work into slides. The Dossier visual system is the antagonist of that posture.

A practice of Brandon Wilburn. The endorsed-house architecture means Brandon Wilburn is the master brand; C9D Consulting is the practice. Every major surface carries the attribution.

---

## The aesthetic — The Dossier

The Dossier treats every artifact as a declassified document, not a marketing site. The reference shapes:

- **What it IS:** a board memo, an acquirer-perspective findings report, a write-up to an incoming engineering executive, an operating record that has been signed off.
- **What it IS NOT:** a venture pitch deck, a SaaS landing page, an agency case study, a generic consulting site, a "modern Tailwind / shadcn" interface.

If a slide could appear in a YC pitch deck, an a16z portfolio page, or a Notion marketing tour without modification, it is wrong for C9D Consulting.

### Fighting Gamma's defaults

Gamma's default aesthetic is bright, decorative, marketing-tuned. Every default works against The Dossier. Override:

- **Gamma's default backgrounds (light gradients, soft cream, white):** Override to `#0c0b08` (warm near-black). Dark mode is the default.
- **Gamma's default typography (Geist, Inter, generic sans):** Override to Inter Tight + Instrument Serif + JetBrains Mono.
- **Gamma's default chart palettes (vibrant categorical scales, blue–orange, sequential greens):** Override to amber-and-shades only.
- **Gamma's default card chrome (rounded corners, drop shadows, glassmorphism):** Override to crisp 1px hairlines, no shadows, no rounded corners above 4px.
- **Gamma's default imagery direction (vibrant photos, illustrations, gradient backgrounds):** Override to document artifacts, schematic illustration, or operator portraiture only.
- **Gamma's default closing slide ("Thank you" or "Questions?"):** Override to the locked closing slide with "We have shipped what we recommend. / Coordinated, not improvised."

---

## Color tokens

Ten tokens. Six chromatic plus four neutral. Composition ratio 70/22/6/2.

### Ground (4 tokens — 70% of visible surface)

| Token | Hex | Use |
|---|---|---|
| Ground | `#0c0b08` | Page background, slide background, deepest layer |
| Ground 2 | `#131210` | Card backgrounds, elevated surfaces |
| Ground 3 | `#1a1815` | Inset blocks within cards |
| Paper | `#161410` | Stamps and signed-off artifact moments |

### Rule (2 tokens)

| Token | Hex | Use |
|---|---|---|
| Rule | `#2a2620` | Standard hairlines between sections, cells, rows |
| Rule Bright | `#3d362c` | Emphasized borders, active or hover states |

### Ink (4 tokens — 22% of visible surface, warm parchment cast)

| Token | Hex | Use | Contrast |
|---|---|---|---|
| Ink Bright | `#f0e6d0` | Headlines, key data, hero copy, important emphasis | 14.1:1 AAA |
| Ink | `#d8cdb8` | Default body text | 11.5:1 AAA |
| Ink Mute | `#8a7e6a` | Supporting copy, sidebar notes, descriptions | 5.2:1 AA |
| Ink Dim | `#5a5042` | Tertiary metadata, page numbers, faint annotations | 3.1:1 AA Large |

### Signal — sodium amber (2 tokens — 6% of visible surface)

| Token | Hex | Use |
|---|---|---|
| Stamp | `#d6743a` | Primary signal: case IDs, section markers, key emphasis, framework names, wordmark |
| Stamp Dim | `#8a4824` | Reserved secondary signal: footer text, stamp interiors, eyebrow labels |

### Crit — classified red (1 token — 2% of visible surface, rationed)

| Token | Hex | Use |
|---|---|---|
| Classified | `#c0392b` | Refusal markers, declined-engagement signals, crit-vulnerability moments only |

### Five color rules

1. **Surface ratios are non-negotiable.** Cover the type. If chromatic balance reads as document, pass. If poster, fail.
2. **Signal indexes the proof.** Sodium amber marks case IDs, section markers, key metrics, framework names, the wordmark. Never decorative.
3. **Crit red is rare.** Reserved for declared refusals and rare crisis moments. The two warm colors must not compete.
4. **Ink hierarchy is enforced.** Body text is Ink. Ink Bright is reserved for things the reader should remember. Roughly 15/65/15/5 distribution.
5. **No additional colors.** No blue. No green. No purple. Charts use shades of amber (100%, 60%, 30% opacity) rather than new hues.

---

## Typography

### The three faces

| Face | Weights | Role | Share of type surface |
|---|---|---|---|
| **Inter Tight** | 200–400 | Display + body. Tight letter-spacing at display sizes (-0.04em at 56px+, -0.03em at 32–48px). | ~55% |
| **Instrument Serif** | 400 italic only | Inline emphasis (1 word or short phrase) and pullquotes (3–8 words). Never body. Never headlines. Never more than 8 consecutive words. | ~5% |
| **JetBrains Mono** | 400–600 | Metadata, file IDs, classifications, section markers, page numbers, eyebrows above titles, code, structured data. | ~40% |

### Type scale (8 steps)

| Step | Size (slide) | Use |
|---|---|---|
| Display XL | 88–116pt | Hero on cover slide. One per deck max. |
| Display L | 56–72pt | Section divider titles, manifesto opener. |
| Display M | 40–48pt | Major slide claims, section headers. |
| H1 | 22–30pt | Subsection headers, component titles. |
| H2 | 18–22pt | Tertiary headers, panel titles. |
| Body | 15–17pt | Default body text. |
| Small | 12–14pt | UI labels, metadata, footnotes. |
| XS / Mono | 9–11pt | File IDs, page numbers, status indicators, classifications. |

### Mono is load-bearing

JetBrains Mono carries roughly 40% of the visible type surface. It must appear on every slide except the cover and close. It is what makes the deck read as document, not marketing. If a slide has no mono, it is wrong.

Mono usage:
- File IDs (`FILE-E01-2026-014`)
- Section markers (`§ 01 — STRATEGIC FOUNDATION`)
- Page numbers (`14 / 42`)
- Classification stamps (`OPERATING EVIDENCE`, `CLIENT CONFIDENTIAL`, `INTERNAL DRAFT`)
- Eyebrows above section titles (`SECTION 01`, `FINDING 03`, `THE PLAYBOOK`)
- Table headers (uppercase, 0.18em letter-spacing)
- Metadata rows (dates, prepared-by, version)
- Caption text below diagrams

### Italic accent

Instrument Serif italic is the accent. Reserved for:
- A single emphasized word inside a body sentence (in Stamp color when it loads the proof)
- A pullquote slide (3–8 words, Stamp color, no quotation marks)
- The closing line "Coordinated, not improvised." on the final slide

Never used for body type. Never used for headlines. Never used for more than 8 consecutive words.

---

## Composition principles

### The 70/22/6/2 ratio (load-bearing)

The visible composition of any slide should sit at:
- 70% ground (the four ground tokens)
- 22% ink (the four ink tokens)
- 6% signal (sodium amber)
- 2% crit (classified red) or stamp interior

These ratios are descriptive of the locked system, not arbitrary. A slide that drifts to 15% signal reads as a poster, not a dossier.

### Hairlines do the work of whitespace

Sections are separated by 1px Rule lines rather than additional whitespace. The Dossier is heavily ruled; rules carry the document texture. Where another aesthetic might use generous padding to separate ideas, The Dossier uses a hairline.

### Asymmetric columns

Two-column layouts use a 5:7 ratio rather than 1:1. The narrower column carries metadata or mono. The wider carries the prose.

### Maximum measure

Body text never exceeds 65 characters per line at body size. If a slide wants more than that, narrow the column or split into a second slide.

### Eyebrow above title

Every section title (and most content slide claims) is preceded by a mono eyebrow in Stamp Dim:
- 11pt JetBrains Mono
- Uppercase
- Letter-spacing 0.18em
- Format: `SECTION 01` or `FINDING 03` or `THE PLAYBOOK` or `DECISION POINT`

---

## Slide patterns

Five slide types cover every deck. Resist adding more.

### S-01 Cover slide

The only slide without chrome. Carries the document's full identity.

**Composition:**
- Background: solid ground (`#0c0b08`)
- Top-left: file ID in mono (`FILE-E01-2026-014`) and classification stamp (uppercase Inter Tight, 0.18em tracking, Stamp color)
- Vertical center, left-aligned: document title in Inter Tight 56–88pt weight 300, color Ink Bright, letter-spacing -0.04em, maximum 2 lines
- Below title: 1px Rule Bright line spanning 4 columns
- Below the line: subtitle in Inter Tight 18–22pt, color Ink Mute, 1 line
- Bottom-left: prepared-by block (3 lines)
  - "Prepared by" in Ink Mute
  - "Brandon Wilburn" in Ink Bright
  - "C9D Consulting" in Ink Bright with "C9D" in Stamp
- Bottom-right: date and version in mono

### S-02 Section divider

Marks a transition into a major section.

**Composition:**
- Background: Ground 2 (`#131210`) — slightly elevated from content slides
- Standard chrome at top and bottom
- Center-left:
  - Eyebrow: `SECTION 01` in JetBrains Mono uppercase 12pt, letter-spacing 0.18em, Stamp Dim color
  - 0.3" gap
  - Section title in Inter Tight 48pt weight 300, Ink Bright, letter-spacing -0.04em
  - 0.4" gap
  - 1px Rule Bright line, 3 columns wide
  - Section description in Inter Tight 18pt weight 400, Ink Mute, max 3 lines

### S-03 Content slide (default — single claim with body)

**Composition:**
- Standard chrome
- Eyebrow tag at top: `FINDING 01` or `THE PLAYBOOK` or `DECISION POINT` in JetBrains Mono Stamp Dim, 10pt, 0.18em letter-spacing
- Claim: Inter Tight 32pt weight 300, Ink Bright, max 2 lines, letter-spacing -0.03em
- 0.6" gap
- Body: Inter Tight 16pt weight 400, Ink, max 65 chars per line, paragraphs separated by 0.2"
- Optional pullquote at right (columns 9–12): Instrument Serif italic 22pt in Stamp, max 8 words

### S-04 Content slide — comparison / table / register

For decision registers, risk registers, threads-pulled lists, anything tabular:
- Title row: Inter Tight 22pt weight 300, Ink Bright
- Optional subtitle: Inter Tight 13pt weight 400, Ink Mute
- Table headers: JetBrains Mono uppercase 10pt, letter-spacing 0.18em, color Stamp Dim
- Body rows: Inter Tight 13pt weight 400, Ink
- Row separator: 0.5pt Rule hairline
- No vertical lines. No alternating row backgrounds.
- Status cells use the color system: open = Stamp, resolved = Ink Mute, refused = Classified, critical = Classified bold

### S-05 Close slide

The closing slide carries the locked closer. The phrase is fixed.

**Composition:**
- Background: solid ground, no chrome
- Vertical center, left-aligned:
  - Inter Tight 32pt weight 300 Ink Bright: "We have shipped what we recommend."
  - 0.3" gap
  - Inter Tight 32pt weight 300 Stamp: "Coordinated, not improvised."
- Bottom-left: wordmark + "A practice of Brandon Wilburn." in Ink Mute
- Bottom-right: c9d.consulting in mono, Ink Mute

Never substitute with "Thank you" or "Questions?" or any Gamma default closing slide.

---

## Slide chrome (every slide except S-01 cover and S-05 close)

Every working slide carries the same chrome at top and bottom.

### Top chrome (header strip, 0.4" tall)

Three-cell row across the top, separated by hairlines:
- **Left:** File ID in JetBrains Mono 9pt, Ink Mute. Format `FILE-[ENGAGEMENT]-[YEAR]-[NUM]` (e.g., `FILE-E01-2026-014`)
- **Center-left:** Classification stamp in Inter Tight uppercase 8pt, letter-spacing 0.18em, Stamp color. Examples: `OPERATING EVIDENCE`, `CLIENT CONFIDENTIAL`, `INTERNAL DRAFT`, `REFUSED`
- **Center-right:** Section marker in JetBrains Mono 9pt, Ink Mute. Format `§ 01 — STRATEGIC FOUNDATION`
- **Right:** Page number in JetBrains Mono 9pt, Ink Mute. Format `01 / 15`

A 0.5pt Rule hairline runs below the top chrome.

### Bottom chrome (footer strip, 0.4" tall)

- **Left:** Wordmark in Inter Tight 12pt — "C9D" in Stamp, "Consulting" in Ink
- **Center:** "A practice of Brandon Wilburn." in Inter Tight 9pt, Ink Mute
- **Right:** c9d.consulting in JetBrains Mono 9pt, Ink Mute

A 0.5pt Rule hairline runs above the bottom chrome.

---

## Visualization patterns — charts, diagrams, registers

The Dossier has a constrained visualization language. Apply rigorously.

### Chart styling

- **Background:** Transparent or matches slide ground
- **Plot area:** No background fill
- **Axis lines:** 0.5pt Rule
- **Axis labels:** JetBrains Mono 9pt uppercase, Ink Mute, letter-spacing 0.18em
- **Data labels:** JetBrains Mono 9pt, Ink
- **Legend:** Inter Tight 9pt, Ink Mute, positioned at bottom horizontal
- **Title:** Inter Tight 14pt weight 400, Ink Bright, left-aligned above chart
- **Gridlines:** None on X axis. Light Rule dashed on Y axis only when needed.

### Chart color sequence (for multi-series)

Use only these colors. No others.

1. Stamp `#d6743a`
2. Ink `#d8cdb8`
3. Stamp Dim `#8a4824`
4. Ink Mute `#8a7e6a`
5. Stamp at 60% opacity
6. Ink Dim `#5a5042`

Five series maximum per chart. If more are needed, split the chart.

### Refused chart types

- 3D charts of any kind
- Pie charts with more than 5 slices
- Donut charts
- Stacked area charts with more than 3 series
- Charts using the default Gamma / Office / Google Slides theme colors
- Bubble charts
- Radar / spider charts
- Word clouds

### Refused chart embellishments

- Glow effects, gradients, drop shadows on bars or lines
- Colored backgrounds behind the chart
- Cartoon icons inside chart segments
- Photographic textures
- Animation in the static deck

### Schematic illustrations and diagrams

System diagrams, decision trees, framework illustrations:
- Lines: 1px Ink on Ground
- Boxes: 1px Rule outline, no fill, or Ground 2 fill with 1px Rule outline
- Labels: JetBrains Mono uppercase 9pt, Ink Mute, letter-spacing 0.18em
- Load-bearing element (the one thing the diagram is about): Stamp color
- Arrows: thin (1px) Ink Mute with simple terminator (no curved or 3D arrowheads)

Refused: 3D renders, isometric illustration, generic flat-illustration stock packs (Storyset, unDraw, Notion-style), gradient backgrounds behind diagrams.

### Registers (decision register, risk register, threads-pulled register)

These are first-class slide types. Use the table convention with these columns where applicable:

**Decision Register:** ID, DECISION, OWNER, OPENED, STATUS, RATIONALE
**Risk Register:** ID, RISK, CATEGORY, LIKELIHOOD, IMPACT, MITIGATION, OWNER
**Threads Register (E-03):** ID, THREAD, PROBABILITY OF PULL, EXPOSURE, MITIGATION

Always assign IDs in mono with zero-padded numbers (`DEC-014`, `RSK-008`, `THR-022`).

---

## Imagery direction

Three categories. No others. No Gamma stock imagery.

### Category 1 — Document artifacts

Screenshots, redacted document scans, framework diagrams, schematic illustrations, operating-evidence captures. The visual rule: it should look like something pulled from an engagement file, not generated for marketing. Sodium amber annotations and JetBrains Mono labels are welcome.

### Category 2 — Schematic illustration

Hand-drawn or vector schematic illustrations in Ink line on Ground, with sodium amber accents on the load-bearing element. Used for system diagrams, decision trees, framework illustrations.

### Category 3 — Operator portraiture

Brandon photographed in a working context. Office, whiteboard, working desk. Not corporate-portrait posing. Warm cast that complements the ink palette. No retouching to glass-skin smoothness.

### Refused imagery

- Stock photography of people (handshakes, laptops, conference rooms)
- Photographic backgrounds
- Gradient backgrounds
- 3D renders
- Isometric illustrations
- Generic flat-illustration stock (Storyset, unDraw, Notion-style)
- Cartoon icons
- Any Gamma default illustration template
- Decorative photography of any kind

---

## Voice — what every slide says

### Voice posture (Sage anchor + Creator secondary)

Reference patterns: Patrick Collison on progress studies, Stripe's writing voice, parts of Ben Horowitz's a16z writing (less the combative pieces). Measured contrarian analysis, not combat.

Four principles:
1. **Evidence-first.** Claims are followed by proof artifacts. No claim without an RTB.
2. **Plain-named-precision.** Name things specifically (Windsurf, Devin, DORA, Keysight, Viavi). Not abstractly.
3. **Concede-first.** Acknowledge what's true in the opposing position before naming what's wrong.
4. **Diagnose-not-moralize.** Describe patterns and costs. Don't moralize about failures or the industry.

### Taglines (three constructs, separate roles)

- **Primary:** *"The playbook, not the deck."* — default tagline; hero copy, sign-offs
- **Alternate:** *"We've shipped what we recommend."* — sub-hero variant
- **Campaign:** *"AI strategy that survives the next round."* — diligence-focused materials only

### Closing line (NOT a tagline)

> **"Coordinated, not improvised."**

Locked. Never substituted. Appears on the close slide, in footers of formal deliverables, and at the end of major documents. This is the line that quietly enables discovery of the C9D = Coordinated numeronym.

### Owned vocabulary (defended)

- **post-shipping** — voice posture
- **operator** — founder-level qualifier
- **the playbook** — the methodology
- **coordinated-not-improvised** — the closer

### Refused vocabulary (never used)

**Kill-criteria filler:**
- transformation, transformative, transform
- journey, customer journey
- innovative, innovation
- empower, empowerment
- thought leadership
- best-in-class, world-class
- synergy, leverage (as verb)

**Competitor-territory vocabulary:**
- AI maturity model
- AI center of excellence
- AI strategy roadmap
- digital transformation
- cloud-first strategy

### Em-dash discipline

Em-dash overuse makes copy read as outsourced. Default to commas, parentheses, or full stops. An em-dash should earn its place by carrying weight no other punctuation can.

### Slide title casing

Sentence case only. Not Title Case. Not ALL CAPS. The exception is the eyebrow above the title (always uppercase mono).

---

## Engagement reference (when decks describe services)

Four engagements. Always full-form on first reference.

| ID | Name | Job | From | Duration |
|---|---|---|---|---|
| E-01 | Productization Engagement | Take a working AI capability and ship it to named enterprise customers | $185K | 90–120 days |
| E-02 | Agentic Adoption Engagement | Apply the Seven-Dimension Review to agentic dev tooling adoption | $145K | 90–120 days |
| E-03 | Diligence Posture Review | Stress-test AI diligence posture before acquirer's counterparts pull on threads | $95K | 30–60 days |
| R-01 | Operating Partner Retainer | Ongoing fractional presence — entered only after E-01/E-02/E-03 | $18K/month | 6–12 month minimum |

Published-pricing language: *"from $X. Fixed scope, fixed price. Quoted to the specific scope, complexity, and stakes of the work."*

Never write "Starting at $X" or "$X+".

---

## Reasons to believe (the proof spine)

Three case studies at brandonwilburn.pro. Every claim in a C9D Consulting deck traces back to one of these.

1. **Luma for Landslide** — Spirent's first agentic AI product. Three of five use cases shipped to tier-one operators.
2. **Agentic development adoption** — Seven-Dimension legal/IP review, landed on Windsurf and Devin, 20–40% throughput lift measured via DORA and DX surveys.
3. **Keysight acquisition** — Four-initiative portfolio at Spirent ran the Keysight acquisition to close at a 15% premium over Viavi's bid, October 2025.

NDA flag (unresolved): RTB 3 specifics with Keysight/Viavi names need disclosure verification before public-facing use.

---

## Gamma prompt recipes

Concrete prompts to use with Gamma's `generate` tool. Each combines an `inputText` (the deck content) with an `additionalInstructions` (the brand application).

### Recipe 1 — Engagement findings deck (E-01/E-02/E-03)

**inputText:**
```
A 12-slide findings deck for [client name], an E-[01/02/03] engagement.

Cover slide: [Title]. Classification: OPERATING EVIDENCE. Date: [date].

Section 01 — Executive Summary. The three threads we found and the one to pull first.

Section 02 — Findings. [Finding 1 with evidence]. [Finding 2]. [Finding 3].

Section 03 — The Playbook. The [Productization Roadmap / Adoption Playbook / Remediation Roadmap] in five named stages.

Section 04 — Decision Register and Risk Register. Two slides.

Section 05 — Close. We have shipped what we recommend. Coordinated, not improvised.
```

**additionalInstructions:**
```
Apply the C9D Consulting brand — The Dossier. Dark by default (#0c0b08 ground, #d8cdb8 body ink, #d6743a sodium amber for emphasis only). Inter Tight + JetBrains Mono. Every slide carries top chrome (file ID, classification stamp, section marker, page number in JetBrains Mono) and bottom chrome (wordmark with "C9D" in amber, "Consulting" in bright ink, attribution "A practice of Brandon Wilburn.", c9d.consulting in mono). No bullet lists over 4 items. Sentence case slide titles. No stock photos. No gradient backgrounds. No rounded corners over 4px. Close slide: "We have shipped what we recommend. / Coordinated, not improvised."
```

### Recipe 2 — Proposal / SOW cover deck

**inputText:**
```
A 6-slide proposal deck for [client name].

Cover: SOW — [Engagement type] for [Client]. Classification: CLIENT CONFIDENTIAL.

Slide 2: The engagement and the scope. [E-XX with one-paragraph framing].

Slide 3: Deliverables. The five named artifacts they will receive.

Slide 4: Timeline and milestones.

Slide 5: Pricing. From $[amount]. Fixed scope, fixed price.

Slide 6: Lead operator (Brandon Wilburn) and acceptance criteria.
```

**additionalInstructions:**
```
[Same as Recipe 1 brand application block]
```

### Recipe 3 — Board / investor update (R-01)

**inputText:**
```
A 10-slide board update from a C9D Consulting R-01 Operating Partner Retainer engagement at [client name]. Cover the quarter's progress against the three pre-stated objectives, the decisions logged in the register, the risks logged in the register, and the one thread worth surfacing to the board.
```

**additionalInstructions:**
```
[Same brand application block.]
Add: include a Decision Register slide and a Risk Register slide using the locked column structures. Headers in JetBrains Mono uppercase, 0.18em tracking, Stamp Dim color. Body rows in Inter Tight 13pt. No vertical column separators. No alternating row backgrounds.
```

### Recipe 4 — TechieBrandon byline article (federated sibling)

**inputText:**
```
A 4-slide companion deck for the TechieBrandon article "[Article title]". Cover, opening claim, the named pattern, the cost, the closer.
```

**additionalInstructions:**
```
TechieBrandon is a federated sibling of C9D Consulting under the same Posture B visual system. Apply The Dossier tokens (same colors, same type stack). DO NOT attribute to C9D Consulting in the byline; attribute to "Brandon Wilburn — TechieBrandon." Boundary is enforced. Closing slide: do not use "Coordinated, not improvised." (that's C9D Consulting's closer); use the article's locked closer or omit.
```

---

## Final must-do / must-not-do checklist

Run every deck against this before treating it as shipped.

### Must do

1. ✅ Dark mode (`#0c0b08` ground) on every slide
2. ✅ Top chrome with file ID, classification, section marker, page number — all in JetBrains Mono or uppercase Inter Tight
3. ✅ Bottom chrome with wordmark, attribution "A practice of Brandon Wilburn.", c9d.consulting in mono
4. ✅ Eyebrow above every section title (JetBrains Mono uppercase, Stamp Dim, 0.18em tracking)
5. ✅ Sodium amber used only to mark proof (case IDs, framework names, key metrics, wordmark)
6. ✅ Sentence case slide titles
7. ✅ JetBrains Mono present on every slide (chrome at minimum)
8. ✅ Closing slide reads "We have shipped what we recommend. / Coordinated, not improvised."
9. ✅ Wordmark uses "C9D" in Stamp + "Consulting" in Ink Bright
10. ✅ Body text never exceeds 65 characters per line

### Must not do

1. ❌ Title Case slide titles
2. ❌ Bullet lists over 4 items
3. ❌ Stock photography of people
4. ❌ Gradient backgrounds
5. ❌ Soft drop shadows on any element
6. ❌ Rounded corners above 4px
7. ❌ Three-column feature grids with icons above titles
8. ❌ Default Gamma / Office / Google Slides chart colors
9. ❌ Default Gamma illustration templates
10. ❌ Animated reveals, slide transitions, or build-by-click sequences
11. ❌ Headers in serif fonts (Instrument Serif is for accent only)
12. ❌ "Thank you" or "Questions?" closing slides
13. ❌ "C9D" alone in body copy (always "C9D Consulting")
14. ❌ Em-dash overuse
15. ❌ The refused vocabulary (transformation, journey, innovative, AI maturity model, AI center of excellence)

---

## Version and provenance

`v1.0 · 2026.06.17 · Gamma Reference Spec · The Dossier`

This spec derives from the C9D Consulting brand skill package v1.1, which itself is reconstructed from the locked source artifacts in the original brand-build session (`c9d-positioning-doc.md`, `c9d-personality-voice-doc.md`, `c9d-architecture-doc.md`, `c9d-verbal-identity-doc.md`, `c9d-visual-identity-doc.md`, `c9d-product-offering-doc.md`).

For full brand foundation and any reference not captured in this Gamma spec, consult the source artifacts or the full brand skill package at `/c9d-consulting-brand/`.

A practice of Brandon Wilburn.

Coordinated, not improvised.
