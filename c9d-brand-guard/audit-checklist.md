# C9D Consulting Brand Audit Checklist

Detailed compliance workflow for a full audit. Use when the 60-second check in SKILL.md is not enough, when auditing an artifact you did not produce, or when preparing an artifact for a high-stakes surface (public site, client engagement cover, board deck, investor material).

Run the checks in order. Do not skip a section because the artifact "looks fine." AI slop reads as fine right up until it fails.

## Prerequisites

Load `snapshot.md` before running the full audit. The snapshot carries the inlined tokens, typography specs, logo inventory, compliance invariants, and voice principles that this checklist cites throughout. Load `refuse-patterns.md` for the fourteen categories of banned patterns and AI slop.

Every finding in the audit resolves to a **blocker** (must fix before ship) or an **advisory** (recommendation, producer may override with documented reason). See `audit-report.md` for the standardized output format and severity framework.

When the audit concludes, produce a report using the template in `audit-report.md`. Fill every field. Do not omit sections with no findings; write "None" instead.

## Section 01. Copy audit

### Naming

1. Every prose reference to the firm reads **"C9D Consulting"** in full. Search the artifact for "C9D " (with a trailing space) and verify each hit is followed by "Consulting" or is inside a wordmark, logo, favicon, file slug, or metadata field. If "C9D" appears alone in body copy, fail.

2. Attribution phrase reads **"A practice of Brandon Wilburn"** exactly. Variants to reject: "A Brandon Wilburn practice", "By Brandon Wilburn", "From the practice of Brandon Wilburn", "A boutique practice by Brandon Wilburn".

3. The URL if present reads `c9d.consulting` in lowercase. Never `C9D.Consulting`, never `C9D Consulting.com`, never `www.c9dconsulting.com`.

4. If the master brand is referenced, it reads `brandonwilburn.pro` in lowercase.

### Tagline system

Only the four locked constructs appear as taglines. Every occurrence matches character-for-character.

- **Primary tagline** (deliverable distinction): "The playbook, not the deck."
- **Alternate tagline** (credential distinction, v2.3 lock): "Operator, not observer."
- **Campaign tagline** (multi-cycle claim): "Judgment across cycles."
- **Closing line** (signature, not a tagline): "Coordinated, not improvised."

Reject any variant. Examples of failure:

- "The playbook, not the pitch deck." (adds a word)
- "Operator, not an observer." (adds an article)
- "Judgment across the cycles." (adds an article)
- "Coordinated. Not improvised." (splits into two sentences with a period)

Shelf constructs are allowed only in the specific contexts documented in `c9d-consulting-brand/references/voice-library.md` under "Shelf taglines". These include "We've shipped what we recommend" (v1.x alternate, still deployable in AI-specific contexts) and "Decades in the seat" (v2.0 draft, still available for shelf use).

### Frame language (v2.3)

The frame reads AI-first, operator-second. Every hero, subtitle, or lead surface opens with **"AI Strategy & Enablement"** and follows with **"Operator Advisory & Strategy"** as the qualifier.

Reject copy that:

- Leads with "Operator Advisory & Strategy" alone (v2.0 to v2.2 pattern, retired in v2.3 because it buried the AI market pull).
- Leads with "AI Strategy Advisory" narrowly to a single vertical (v1.x pattern, retired in v2.0 because it closed doors).
- Uses "fractional CTO", "fractional executive", or "management consulting" as the frame. None of these are the C9D Consulting frame.

Approved framing examples:

- "operator-grade practice for AI Strategy & Enablement"
- "AI Strategy & Enablement, delivered by an operator across cycles"
- "AI Strategy & Enablement (cornerstone) with Operator Advisory & Strategy (differentiator)"

### Positioning consistency

The two-part POD holds throughout:

- Part A (cornerstone): AI Strategy & Enablement is the leading offering. Market pull is real. Work is defensible.
- Part B (differentiator): nearly two decades of operator experience across enterprise software, technology and business strategy, governance, compliance, cybersecurity, mobile, SaaS, machine learning, and new product introduction.

Reject copy that:

- Leaves out either part (both are required together).
- Substitutes a shorter list of domains without reason.
- Replaces "nearly two decades" with a bigger or smaller number (see Section 04 for evidence checks).

### Vocabulary lock

Use "observers" (never "watchers") for the class of outside advisors. Use "operator" (never "practitioner" or "veteran") for the credential position. Use "credential" for the abstract asset, "operator experience" for the concrete history.

### Voice principles

Every claim in the copy meets the four voice principles from the main brand:

1. **Evidence-first.** Each substantive claim is defensible from CV, public record, or the artifact itself. Reject market-level claims about competitors' careers, unstated assertions dressed as facts, or figures presented without provenance.

2. **Plain-named-precision.** Roles, companies, waves, and domains are named specifically. Reject generic references like "a Fortune 500 acquirer" when the actual company (Keysight) is on public record.

3. **Concede-first.** Where a competing position has genuine merit, the copy concedes it before differentiating. Reject copy that attacks competitors, exaggerates their weaknesses, or treats their existence as evidence of poor judgment.

4. **Diagnose, do not moralize.** Patterns are described structurally, not judgmentally. Reject copy that reads as scolding, superior, or performatively contrarian.

## Section 02. Color audit

### Token compliance

Every color instance is one of the tokens in `c9d-consulting-brand/assets/tokens.css`. Load the file to verify hex values. Search the artifact source (SVG, CSS, HTML, DOCX XML, PPTX XML) for every fill, stroke, and color value. Cross-reference each against the token list.

Reject any color not in the list. This includes:

- Blue, green, teal, purple, pink accents.
- Gradient stops of any kind.
- Alpha-blended colors that resolve to off-token hex values in the render.
- Client-brand colors imported into the C9D chrome. If a client logo is required, use the client logo as an image and keep the C9D chrome tokens intact.

### Mode selection

- **Dark mode** is the default for all screen artifacts: decks, web, dashboards, SVG diagrams, banners.
- **Light mode** is used only for print artifacts: Word docs, PDFs for printing, letterhead.
- **Print media query mode** applies automatically to web artifacts when the user prints them.

Reject an artifact that uses light mode on screen or dark mode for print without a specific reason.

### Ratio compliance

The Dossier uses a fixed 70 ground / 22 ink / 6 signal / 2 crit composition ratio. Visually estimate the ratio on the artifact. If:

- Amber signal covers more than 6% by visual weight, demote some to standard ink or elevated ground.
- Classified red covers more than 2%, remove some. Red is rationed to actual refusals, kill nodes, or error paths.
- Ground covers less than 60%, the artifact is over-decorated. Remove content or increase whitespace.

## Section 03. Typography audit

### Font stack

Every text run uses one of:

- **Inter Tight** (primary sans, all weights).
- **Instrument Serif** italic (accent serif for pullquotes and single-word emphasis).
- **JetBrains Mono** (metadata, file IDs, page numbers, eyebrows, mono labels).

Reject any use of Arial, Helvetica, Times New Roman, Calibri, Aptos, Georgia, Trebuchet MS, Comic Sans, or system defaults as the primary face. If the render environment substitutes (LibreOffice preview, some Google Docs configurations), that is a preview limitation. The source font declaration must be the correct Dossier font.

### Weight and style

- Inter Tight: weights 400 (regular), 500 (medium), 600 (semibold). Never 700 bold for headlines; use 500 or 600 with tight letter spacing instead. Never 100 or 200 (thin).
- Instrument Serif: italic 400 only. Never Instrument Serif regular. Never bold or semibold.
- JetBrains Mono: 400 or 500. Bold JetBrains Mono acceptable for uppercase eyebrows.

### Size hierarchy

Type scale is defined in `tokens.css` under `--size-*`. Rough guide:

| Element | Size |
|---|---|
| Display XL (hero) | 72 to 116 pixels |
| Display L | 48 to 72 pixels |
| Display M | 36 to 48 pixels |
| H1 | 22 to 30 pixels |
| H2 | 18 to 22 pixels |
| Body | 15 to 17 pixels |
| Small | 13 pixels |
| Extra small (mono) | 11 pixels |

Reject text that departs from this scale without a specific reason.

### Letter spacing

- Display sizes: negative tracking, roughly negative 0.03 to negative 0.04 em.
- Headings: slight negative tracking, negative 0.02 to negative 0.03 em.
- Body: 0 tracking.
- Mono metadata: positive 0.04 em.
- Eyebrows and stamps: positive 0.18 em.

### Alignment

Left-align all body copy. Never justify. Center only titles that carry weight (cover title, section divider title, close signature).

## Section 04. Evidence audit

Every quantified claim in the artifact must trace back to a defensible source.

### Approved evidence citations

- **Luma for Landslide.** Spirent's first agentic AI product. Launched publicly Feb 18, 2026. Roughly 16 months to first release. Documented at brandonwilburn.pro.
- **Seven-Dimension enterprise adoption playbook.** Cleared agentic dev adoption through real legal and IP review. Measured 20 to 40% throughput lift via DORA + DX surveys. Documented at brandonwilburn.pro.
- **Spirent to Keysight acquisition close.** October 2025. Fifteen percent premium over Viavi's competing bid. Four concurrent strategic initiatives ran toward acquisition-readiness. Zero critical vulnerabilities at close. Clean license posture before final diligence. The scope (four concurrent initiatives) and the premium (over Viavi) are the credential. The dollar close value ($1.3B, public record) is intentionally deprioritized in copy per the v2.0 discipline. Reject copy that leads with $1.3B or with "$600M to $1.3B trajectory" language.
- **Nearly two decades operator experience.** Total tech tenure roughly 18 years (Feb 2008 to present). Principal architect and above tenure roughly 11 years (April 2015 to present at Viavi and Spirent). "Nearly two decades" is defensible in positioning copy. "Over 15 years" or "18 years" are stricter but defensible. Reject "over two decades" or "decades" (plural, strict) without context.
- **Ten domains of operator experience.** Enterprise software, technology and business strategy, governance, compliance, cybersecurity, mobile, SaaS, machine learning, agentic AI, new product introduction. This list is locked. Reject substitutions or reorderings.

### Reject unsourced claims

- Market-level statistics about advisor career paths (e.g. "most AI strategists have never shipped") without a primary source.
- Client outcomes that are not part of the brandonwilburn.pro case study set.
- Confidential deal details that were not publicly disclosed.
- Estimates presented as facts. If the source is your inference, mark it as inference or remove.

## Section 05. Logo audit

### Correct lockup for the surface

- **Header, footer, deck cover, doc cover:** horizontal wordmark.
- **Narrow surfaces, mobile hero, social profile:** stacked wordmark. Both lines centered on shared midline.
- **Single-color reproduction, letterhead, embossed:** mono wordmark.
- **When practice attribution should be visible:** endorsed lockup ("A practice of Brandon Wilburn" beneath wordmark).
- **When primary tagline should be visible:** tagline lockup ("The playbook, not the deck." beneath wordmark).
- **App icon, profile picture, favicon:** square icon using the live-site-aligned treatment.

Reject any invented lockup, modified wordmark, altered spacing, changed color, or non-approved combination.

### Wordmark integrity

- "C9D" in amber (`#D6743A` dark mode, `#9C4F24` light mode) with tight letter spacing.
- " Consulting" in ink bright (`#F0E6D0` dark mode, `#1A1612` light mode) with matching tight letter spacing.
- Joined form (no space between "C9D" and "Consulting" in the wordmark, only a soft optical space).
- Single-color version uses the same ink color throughout (mono variants).

Never render the wordmark:

- With shadow or outline effects.
- Rotated at any angle other than 0 degrees.
- Scaled non-uniformly.
- With filter effects (blur, glow, bevel).
- Against a busy or textured background.
- Below the minimum size (32 pixels tall for wordmark, 16 pixels for favicon icon).

### Clear space

Around any wordmark or lockup, maintain minimum clear space equal to the height of the "C" glyph in "C9D". No text, image, or graphic element enters this margin.

## Section 06. Layout audit

### Grid and alignment

- Every element aligns to a 4-pixel or 8-pixel grid.
- Consistent margins across the artifact. Minimum 0.5 inch on print, 24 to 48 pixels on screen.
- Consistent gutters between content blocks. Choose 0.3 or 0.5 inch on print, 24 or 48 pixels on screen, and hold to it.

### Whitespace

- Content should feel deliberate, not cramped. Leave breathing room.
- Cover pages, section dividers, close pages carry more whitespace than content pages.
- If every inch of the artifact is filled, remove content until the ratio breathes.

### Forbidden layout patterns

- **No accent bars or color stripes** along the edge of a card, panel, or section. This is a hallmark AI-generated pattern.
- **No decorative color bars** at the top or side of the artifact.
- **No drop shadows** on any element. The Dossier is flat.
- **No gradients** as fills. Flat colors only.
- **No rounded content boxes.** Rounded corners cap at 2 pixels on buttons; 0 pixels on content.
- **No center-aligned body text.** Left-align paragraphs and lists always.

## Section 07. Signature audit

Every C9D Consulting artifact carries a specific signature pattern at the end.

### Signature elements

1. Wordmark or endorsed lockup.
2. Attribution: "A practice of Brandon Wilburn" exactly, with no terminal period, as `naming.founder.attribution` in `tokens.json` holds it.
3. If a signing surface (letter, memo, client-facing deliverable): signer name, role, date.
4. Closing line where appropriate: "Coordinated, not improvised."

### Reject substitutions

- "Thank you" as a close on a client-facing artifact.
- "Questions?" on a close deck slide.
- "For further information contact..." as the sign-off. Instead include the C9D Consulting URL.
- Emojis, decorative characters, or promotional copy in the signature area.

## Audit result

When every section passes, the artifact ships. When any section fails, state the specific rule and quote the source token or copy line. Do not paraphrase. Correct or return to the user for correction. If the correction requires a foundational decision (new engagement type, new tagline, new lockup), stop and escalate rather than invent.

## Related files

**Inlined in this skill (available without main package):**

- `snapshot.md`: full tokens, typography, logo inventory, invariants 1 through 13, voice principles, frame evolution history.
- `refuse-patterns.md`: AI slop and banned pattern library, fourteen categories.
- `audit-report.md`: standardized audit output template with severity framework and worked example.
- `SKILL.md`: entry point with 60-second check.

**Referenced in main c9d-consulting-brand package (require main package if attached):**

- Full manifesto (v2.3): `c9d-consulting-brand/references/foundation.md` under Manifesto.
- Full 21-invariant list including strategic invariants: `c9d-consulting-brand/SKILL.md` at root.
- Voice library detail (Tier A vocabulary, refused vocabulary, tone flex matrix): `c9d-consulting-brand/references/voice-library.md`.
- Engagement architecture, pricing, refuse list: `c9d-consulting-brand/references/engagement-architecture.md`.
- Visual system detail (spatial system, federated Posture B, logo showcase): `c9d-consulting-brand/references/visual-system.md`.
- Site copy history: `c9d-consulting-brand/references/site-copy-v2.md`.
- Token source: `c9d-consulting-brand/assets/tokens.css` and `tokens.json`.
- Logo asset files: `c9d-consulting-brand/assets/logos/`.
