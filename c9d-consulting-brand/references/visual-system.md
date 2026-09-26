# Visual System

The Dossier aesthetic translates to four locked subsystems: color, typography, logo, spatial. Each subsystem has tokens, rules, and a list of refused patterns. Apply all four together; partial application reads as decoration.

This file is reconstructed from the locked §9 Visual Identity Doc artifact. Items marked **[locked]** are verified against source. Items marked **[derived]** are reasonable extrapolations flagged for review. The companion HTML design system (`c9d-design-system-vol-01.html`) is the executable instance.

**[locked]** **Federated architecture (Posture B):** The Dossier visual system spans three properties as a federated system:
- **c9d.consulting** — the AI Strategy Advisory practice (primary surface for this skill)
- **brandonwilburn.pro** — operator candidacy (federated sibling, same design tokens, different content density)
- **TechieBrandon.com** — publication (federated sibling)

The master brand is Brandon Wilburn; the visual system is the visible tissue that holds the three properties together.

---

## Color

**[locked]** Ten tokens. Six chromatic plus four neutral. Composition ratio 70/22/6/2.

### Ground (4 tokens)

Layered dark surfaces with warm undertone. The ground is the page; cards lift off it.

| Token | Hex | Use |
|---|---|---|
| `--bg` | `#0c0b08` | Page ground, deepest layer |
| `--bg-2` | `#131210` | Card and panel backgrounds, elevated surfaces |
| `--bg-3` | `#1a1815` | Inset blocks within cards |
| `--paper` | `#161410` | Reserved for stamps and signed-off artifact moments |

### Rule (2 tokens)

Hairlines and emphasized borders. The system is heavily ruled; rules carry weight that whitespace alone cannot.

| Token | Hex | Use |
|---|---|---|
| `--rule` | `#2a2620` | Standard hairlines between sections, cells, rows |
| `--rule-bright` | `#3d362c` | Emphasized borders, active, hover, schematic lines |

### Ink (4 tokens, warm parchment undertone)

The type sits on the page with a warm cast. Pure white is refused; the off-white reads as document.

| Token | Hex | Contrast vs `--bg` | Use |
|---|---|---|---|
| `--ink-bright` | `#f0e6d0` | 14.1:1 (AAA) | Headlines, key data, hero copy, important emphasis |
| `--ink` | `#d8cdb8` | 11.5:1 (AAA) | Default body text |
| `--ink-mute` | `#8a7e6a` | 5.2:1 (AA) | Supporting copy, sidebar notes, descriptions |
| `--ink-dim` | `#5a5042` | 3.1:1 (AA Large) | Tertiary metadata, page numbers, faint annotations |

### Signal — sodium amber (2 tokens)

The single chromatic accent. Tied to the proof spine; never decorative.

| Token | Hex | Contrast vs `--bg` | Use |
|---|---|---|---|
| `--stamp` | `#d6743a` | 6.4:1 (AA) | Primary signal: case IDs, section markers, key emphasis, classification labels, the wordmark |
| `--stamp-dim` | `#8a4824` | 3.2:1 (AA Large) | Reserved/aged secondary signal: footer text, stamp interiors |

### Crit — classified red (1 token)

The refusal color. Rare by design; rationed by rule.

| Token | Hex | Contrast vs `--bg` | Use |
|---|---|---|---|
| `--classified` | `#c0392b` | 5.0:1 (AA) | Refusal markers, declined-engagement signals, crit-vulnerability moments |

### Composition ratio (load-bearing)

The visible composition of any page sits at:

- 70% ground (the four `--bg` tokens)
- 22% ink (the four ink tokens)
- 6% signal (sodium amber)
- 2% crit (classified red) or interior text on stamps

These ratios are descriptive of the locked system, not arbitrary. They are what gives the document its dignity. A page that drifts to 15% signal reads as a poster, not a dossier.

### Five color usage rules

1. **Surface ratios are non-negotiable.** Eyeball test: cover the type. If the chromatic balance reads as document, pass. If it reads as poster, fail.
2. **Signal indexes the proof.** Sodium amber marks case IDs, section markers, measured metrics, framework names, and the wordmark. Nothing else.
3. **Crit red is rare.** Reserved for declared refusals and rare crisis moments. The two warm colors must not compete.
4. **Ink hierarchy is enforced.** Body text is `--ink`; `--ink-bright` is reserved for things the reader should remember. Roughly 15 / 65 / 15 / 5 distribution across `--ink-bright` / `--ink` / `--ink-mute` / `--ink-dim`.
5. **No additional colors without re-opening the system.** No blue. No green. No purple. Charts requiring additional encoding use shades of the existing palette (amber at 100%, 60%, 30% opacity) rather than new hues.

### Light-mode variant (constrained use only)

The Dossier is dark by default. Light mode exists for print-only artifacts that may be physically printed (signed SOWs, engagement letters going to general counsel, board memos that may be printed for binder distribution).

**[derived, not from source]** The specific light-mode hex values below are reasonable derivations from the dark-mode palette but were NOT specified in locked source. They are proposals for review, not locked decisions. **Action:** verify or replace with values from `c9d-design-system-vol-01.html` before using in any print deliverable.

Light mode token map (proposed):

| Dark | Light equivalent | Hex |
|---|---|---|
| `--bg` | `--bg-light` | `#f5f1e8` |
| `--bg-2` | `--bg-2-light` | `#ebe5d6` |
| `--bg-3` | `--bg-3-light` | `#e0d8c5` |
| `--paper` | `--paper-light` | `#ede7d4` |
| `--rule` | `--rule-light` | `#c8bda5` |
| `--rule-bright` | `--rule-bright-light` | `#a89c82` |
| `--ink-bright` | `--ink-bright-light` | `#1a1612` |
| `--ink` | `--ink-light` | `#2e2820` |
| `--ink-mute` | `--ink-mute-light` | `#5a5042` |
| `--ink-dim` | `--ink-dim-light` | `#8a7e6a` |
| `--stamp` | `--stamp-light` | `#9c4f24` |
| `--stamp-dim` | `--stamp-dim-light` | `#6b3818` |
| `--classified` | `--classified-light` | `#8b2a20` |

Composition ratio is the same: 70 / 22 / 6 / 2.

---

## Typography

### Locked typeface stack

| Role | Typeface | Weights | Notes |
|---|---|---|---|
| Display | Inter Tight | 200–400 | Tight letter-spacing at large sizes (-0.02em at Display M+, -0.04em at Display L+) |
| Body | Inter Tight | 350–450 | Optical sizing via opsz axis |
| Italic accent | Instrument Serif | 400 italic | Reserved for inline emphasis and pullquotes |
| Mono | JetBrains Mono | 400–600 | Roughly 40% of visible type surface, carries metadata weight |

### Eight-step type scale

| Step | Size | Use |
|---|---|---|
| Display XL | 88–116px | Hero on the site and one section opener per long document. One per page maximum. |
| Display L | 56–72px | Section heroes, manifesto opener |
| Display M | 40–48px | Section titles, major page headers |
| H1 | 22–30px | Subsection headers, component titles |
| H2 | 18–22px | Tertiary headers, panel titles |
| Body | 15–17px | Default body text |
| Small | 12–14px | UI labels, metadata, footnotes |
| XS / Mono | 9–11px | File IDs, page numbers, status indicators, classifications |

### Mono is load-bearing

JetBrains Mono carries roughly 40% of the visible type surface across the system. It appears on:

- File IDs and case IDs (e.g., `FILE-E01-2026-014`, `CASE-04`)
- Section markers (`§ 01`, `§ 02`)
- Classification stamps (`OPERATING EVIDENCE`, `CLASSIFIED`, `REFUSED`)
- Page numbers and document chrome
- Metadata rows (dates, prepared-by, version)
- Status indicators
- The eyebrow above section titles

This is the texture that makes the brand read as document. Stripping the mono and substituting Inter Tight reads as a regular consulting site.

### Italic accent (Instrument Serif)

Reserved for inline emphasis (a single word or short phrase) and pullquotes (3–8 words). Used in `--stamp` color when the emphasis is part of the proof spine; otherwise in `--ink-bright`. Never used for body type. Never used for headlines. Never used for more than 8 consecutive words.

### Refused typography patterns

- Default Inter / Roboto / Geist body type without distinctive treatment
- Multiple display faces competing on one page
- Exotic display faces (script, condensed-extra-display)
- All-caps body text
- Italicized blocks of body type (italic reserved for inline emphasis)
- Letterspacing as a primary device for display moments
- The stack "Inter + JetBrains Mono with a quirky display" is refused; it is too default to remain distinctive

---

## Logo system

### The wordmark

The C9D Consulting wordmark uses Inter Tight at weight 400 with tracking -0.04em. The "C9D" is set in `--stamp` (sodium amber). The "Consulting" is set in `--ink-bright`. The two halves are visually weighted at roughly 1:1.5 (C9D : Consulting), reading as "C9D" first then "Consulting" as the categorical clarifier.

### Wordmark variants

**[locked, partial]** Source §9 documents **five named lockups** that govern the wordmark across surfaces, plus **eleven production SVG assets** total (the additional SVGs likely cover format and color variants of the five named lockups). 

The specific lockup names and the eleven-asset inventory were NOT captured in this skill's source extraction. **Action:** pull the locked five lockup names and the eleven SVG asset inventory from `c9d-visual-identity-doc.md` §9.5 and the companion `c9d-design-system-vol-01.html` in the original session before any deliverable references a specific lockup ID.

The locked single exception to the "C9D" naming convention is the favicon (justified by 16/32/48 px space constraint). This favicon was identified in source as U-06; other U-XX IDs in earlier versions of this skill were invented and have been removed.

### Forbidden lockups

- C9D Consulting and Brandon Wilburn as co-equal peers (violates endorsed-house hierarchy)
- TechieBrandon and C9D Consulting directly paired (violates the boundary rule between publication and practice)
- Any wordmark with welded tagline (taglines are typeset adjacent, never integrated)
- Any wordmark variant using "C9D" alone (violates the naming convention)
- C9D Consulting wordmark on a colored background other than `--bg`, `--bg-2`, `--bg-3`, `--paper`, or the locked amber-stamp lockup variant

### Cross-brand attribution rule

Every C9D Consulting page must contain the locked "A practice of Brandon Wilburn" attribution lockup (or equivalent inline attribution) at least once per major page. Footer is the default location. This enforces the endorsed-house architecture.

---

## Spatial system

### Grid

The base grid is 8px. All spacing values are multiples of 8 except for the tightest typographic adjustments (4px allowed for inline-mono-to-ink alignment).

### Spacing scale

| Token | Value | Use |
|---|---|---|
| `--space-1` | 4px | Tight inline adjustments only |
| `--space-2` | 8px | Within-component spacing |
| `--space-3` | 16px | Standard padding inside cards |
| `--space-4` | 24px | Between paragraphs, between rows |
| `--space-5` | 32px | Card padding, generous between-paragraph |
| `--space-6` | 48px | Section internal padding |
| `--space-7` | 64px | Between sections |
| `--space-8` | 96px | Between major page divisions |
| `--space-9` | 128px | Hero / section opener vertical breathing |

### Composition principles

1. **Cards lift off the ground.** `--bg-2` cards on a `--bg` ground, separated by `--space-7` (64px) by default. Cards have `--space-5` (32px) internal padding.

2. **Hairlines do the work of whitespace.** Sections are separated by 1px `--rule` lines rather than by additional whitespace. The system is heavily ruled; rules carry the document texture.

3. **Asymmetric columns.** Two-column layouts use a 5:7 ratio rather than 1:1. The narrower column carries metadata or mono. The wider carries the prose.

4. **Maximum measure.** Body text never exceeds 65 characters per line at the prevailing body size (15–17px). Wider columns are split or constrained.

5. **Eyebrow above title.** Section titles are preceded by a mono eyebrow in `--stamp-dim` containing the section number and short label (`§ 01 — STRATEGIC FOUNDATION`). The eyebrow is set in JetBrains Mono at XS size with letter-spacing 0.18em and uppercase.

6. **Mono metadata row.** Every major document or page carries a top-of-page metadata row in JetBrains Mono XS containing: file ID, classification, date, version. Five-cell layout, separated by `--rule` hairlines.

### Refused spatial patterns

- Centered hero text with a centered CTA button (reads as marketing site)
- Three-column feature grids with icons above titles (reads as SaaS landing page)
- Carousels and animated reveals (reads as marketing)
- Bordered "cards" with rounded corners > 4px (reads as Bootstrap default)
- Soft drop shadows on cards (the system uses crisp rules, not shadows)
- Hero images of stock photography people (the system uses operator portraiture or no imagery)

---

## Imagery direction

Three categories. No others.

### Category 1 — Document artifacts

Screenshots, redacted document scans, framework diagrams, schematic illustrations, operating-evidence captures. The visual rule: it should look like something pulled from an engagement file, not generated for marketing. Sodium amber annotations and JetBrains Mono labels are welcome; gradient overlays and color filters are refused.

### Category 2 — Schematic illustration

Hand-drawn or vector schematic illustrations in `--ink` line on `--bg`, with sodium amber accents on the load-bearing element. Used for system diagrams, decision trees, framework illustrations. Refused: 3D renders, isometric illustrations, generic flat-illustration stock packs (Storyset, unDraw, Notion-style).

### Category 3 — Operator portraiture

Brandon photographed in a working context. Office, whiteboard, working desk. Not corporate-portrait posing. The portrait is shot in available light with warm cast that complements the ink palette. No retouching to glass-skin smoothness. The portrait reads as someone in the middle of the work, not someone presenting themselves for hire.
