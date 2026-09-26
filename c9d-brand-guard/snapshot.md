# C9D Consulting Brand Snapshot, v2.3

Inlined brand data for offline compliance verification. This file is the guard's self-contained snapshot of the main c9d-consulting-brand package. When this snapshot is present, the guard can run a full audit without loading the main package.

## Version discipline

This snapshot is locked at brand version **v2.3**, cut from the main c9d-consulting-brand package on the date of guard release. When the main package version moves (v2.4 or later), this snapshot goes stale and must be rebuilt. The guard's `SKILL.md` records the snapshot version in its metadata. Do not mix versions between the main package and the guard snapshot.

Strategic invariants (14 through 21, the ones about brand architecture, engagement structure, and cross-property scope) are NOT inlined here. They remain in the main package. If an audit surfaces a question about those, load the main package or escalate.

## Section A. Color tokens

Every color in a C9D Consulting artifact must match one of the tokens below. Values are hex without the # prefix for portability across CSS, SVG, DOCX, PPTX, and JSON.

### Dark mode (default for all screen artifacts)

| Token role | Hex | Purpose |
|---|---|---|
| bg | 0C0B08 | Page ground, deepest layer |
| bg-2 | 131210 | Cards, panels, standard boxes |
| bg-3 | 1A1815 | Inset blocks, emphasis boxes |
| paper | 161410 | Stamps and signed artifact moments |
| rule | 2A2620 | Standard hairlines |
| rule-bright | 3D362C | Emphasized borders, active states |
| ink-bright | F0E6D0 | Headlines, key data, hero copy |
| ink | D8CDB8 | Default body text |
| ink-mute | 8A7E6A | Supporting copy, sidebar notes |
| ink-dim | 5A5042 | Tertiary metadata, page numbers |
| stamp | D6743A | Primary signal: case IDs, markers, emphasis |
| stamp-dim | 8A4824 | Reserved or aged secondary signal, eyebrows |
| classified | C0392B | Refusals and crit-vulnerability only |
| classified-dim | 8B2A20 | Refusal outlines, error path arrows |

### Light mode (print artifacts only)

| Token role | Hex | Purpose |
|---|---|---|
| bg | F5F1E8 | Paper background |
| bg-2 | EBE5D6 | Card and callout backgrounds |
| bg-3 | E0D8C5 | Inset blocks within cards |
| paper | EDE7D4 | Stamps and signed moments |
| rule | C8BDA5 | Standard hairlines |
| rule-bright | A89C82 | Emphasized borders |
| ink-bright | 1A1612 | Headlines |
| ink | 2E2820 | Body text |
| ink-mute | 5A5042 | Supporting copy |
| ink-dim | 8A7E6A | Metadata |
| stamp | 9C4F24 | Sodium amber, adjusted for print contrast |
| stamp-dim | 6B3818 | Aged amber |
| classified | 8B2A20 | Classified red for print |
| classified-dim | 6B1E18 | Aged classified red |

### Print media query (auto-applied when web is printed)

| Token role | Hex |
|---|---|
| bg | FFFFFF |
| bg-2 | F8F4EB |
| bg-3 | EBE5D6 |
| ink-bright | 000000 |
| ink | 1A1612 |
| stamp | 9C4F24 |
| classified | 8B2A20 |

### Composition ratio (locked, applies to all modes)

70 ground / 22 ink / 6 signal / 2 crit.

If amber signal covers more than 6% of the artifact by visual weight, demote some to ink. If classified red covers more than 2%, remove some. Red is rationed to refusals, kill nodes, and error paths only.

## Section B. Typography

Three faces. No exceptions.

### Font stack

| Face | Fallback stack | Usage |
|---|---|---|
| Inter Tight | Inter, -apple-system, system-ui, sans-serif | Headlines, body copy, wordmark, buttons |
| Instrument Serif | Georgia, serif | Italic accent, pullquotes, single-word emphasis |
| JetBrains Mono | ui-monospace, SFMono-Regular, Menlo, monospace | Metadata, file IDs, page numbers, eyebrows, mono labels |

### Weights and styles

- **Inter Tight:** 400 regular, 500 medium, 600 semibold. Never 700 bold for headlines. Never 100 or 200 thin.
- **Instrument Serif:** italic 400 only. Never regular. Never bold.
- **JetBrains Mono:** 400 or 500. Bold acceptable for uppercase eyebrows.

### Type scale (pixel values, adjust for medium)

| Element | Size |
|---|---|
| Display XL (hero cover) | 72 to 116 px |
| Display L | 48 to 72 px |
| Display M | 36 to 48 px |
| H1 | 22 to 30 px |
| H2 | 18 to 22 px |
| Body | 15 to 17 px |
| Small | 13 px |
| Extra small (mono) | 11 px |

### Line height

| Context | Value |
|---|---|
| Display and hero | 1.05 (tight) |
| Headings | 1.2 (snug) |
| Body and captions | 1.6 (normal) |

### Letter spacing (tracking)

| Context | Value |
|---|---|
| Display sizes | -0.04 em |
| Headings | -0.03 em |
| Body | 0 em |
| Mono metadata | 0.04 em |
| Eyebrows and stamps | 0.18 em |

### Alignment rules

Left-align all body copy. Never justify. Center only titles that carry weight: cover title, section divider title, close signature. Never center body paragraphs, lists, or captions.

## Section C. Logo inventory

Six lockups plus favicons and banners. Each has a defined usage context. Never invent a new lockup or modify an existing one.

### Wordmark lockups

| Lockup | SVG filename (in assets/logos/) | Use for |
|---|---|---|
| Horizontal wordmark, dark | c9d-consulting-wordmark-horizontal-dark.svg | Default for headers, footers, deck covers, doc covers on dark ground |
| Horizontal wordmark, light | c9d-consulting-wordmark-horizontal-light.svg | Same as above on light ground (print) |
| Stacked wordmark, dark | c9d-consulting-wordmark-stacked-dark.svg | Narrow surfaces: mobile hero, social profile, stacked layouts. Both lines centered on shared midline. |
| Stacked wordmark, light | c9d-consulting-wordmark-stacked-light.svg | Same as above on light ground |
| Mono wordmark, dark | c9d-consulting-wordmark-mono-dark.svg | Single-color reproduction, letterhead, embossed |
| Mono wordmark, light | c9d-consulting-wordmark-mono-light.svg | Same as above on light ground |
| Endorsed lockup, dark | c9d-consulting-endorsed-dark.svg | Carries "A practice of Brandon Wilburn" attribution beneath wordmark. Use when attribution should be visible. |
| Endorsed lockup, light | c9d-consulting-endorsed-light.svg | Same as above on light ground |
| Tagline lockup, dark | c9d-consulting-with-tagline-dark.svg | Carries primary tagline beneath wordmark. Use for cover surfaces where deliverable distinction should be visible. |

### Icon assets

| Asset | Filename | Use for |
|---|---|---|
| Square icon (SVG) | c9d-icon-square.svg | App icon, profile picture. Live-site-aligned treatment. |
| Square icon (120) | c9d-icon-square-120.svg / .png | Google Cloud, specific integrations requiring 120x120 |
| Square icon (64 through 512) | c9d-icon-square-{64,96,128,180,256,512}.png | Various UI contexts |
| Favicon (16 through 512) | c9d-favicon-{16,32,48,64,180,512}.png | Browser favicon, Apple touch icon (180) |
| Monogram stamp | c9d-monogram-stamp.svg | Superseded. Do not use in new artifacts. Kept for legacy reference only. |

### Banners

| Banner | Filename | Use for |
|---|---|---|
| OG image | c9d-banner-og-1200x630.png | Open Graph social preview |
| LinkedIn personal | c9d-banner-linkedin-personal-1584x396.png | LinkedIn personal profile header |
| LinkedIn company | c9d-banner-linkedin-company-1584x396.png | LinkedIn company page header |
| X header | c9d-banner-x-header-1500x500.png | X (Twitter) profile header |
| Reddit banner | c9d-banner-reddit-1920x384.png | Reddit profile or subreddit banner |

Note: banners are pending re-render against v2.3 positioning. Current versions carry v1.x "$600M-class enterprise portfolio" copy that has been retired.

### Wordmark integrity rules

- "C9D" renders in stamp color (D6743A dark mode, 9C4F24 light mode) with tight letter spacing.
- " Consulting" renders in ink-bright (F0E6D0 dark mode, 1A1612 light mode) with matching tight letter spacing.
- Joined form: no visible space between "C9D" and "Consulting" in the wordmark, only a soft optical space.
- Never render the wordmark with shadow, outline, rotation other than 0 degrees, non-uniform scaling, filter effects (blur, glow, bevel), or against a busy or textured background.
- Below 32 pixels tall for the wordmark, use the square icon instead.
- Below 16 pixels, use the favicon.

### Clear space rule

Around any wordmark or lockup, maintain minimum clear space equal to the height of the "C" glyph in "C9D". No text, image, or graphic element enters this margin.

## Section D. Compliance invariants (visual and copy scope)

The main brand package carries 21 numbered invariants. The ones below are the visual and copy compliance subset, inlined for the guard. Strategic invariants (10, 14, 16, 17, 20 by their original numbering) remain in the main package as referenced.

### Invariant 1: Frame

Site subtitles, hero copy, and lead surfaces open with **"AI Strategy & Enablement"**. The **"Operator Advisory & Strategy"** framing follows as the qualifier that separates the practice from the mass market of AI-strategy observers.

Reject any lead copy that opens with:

- "Operator Advisory & Strategy" alone (v2.0 through v2.2 pattern, retired in v2.3).
- "AI Strategy Advisory" narrowly to a single vertical (v1.x pattern, retired in v2.0).
- "Fractional CTO", "fractional executive", or "management consulting" as the frame.

### Invariant 2: Point of difference (POD)

Two-part POD. Both parts required in any surface that states positioning.

- **Part A (cornerstone):** AI Strategy & Enablement is the leading offering.
- **Part B (differentiator):** Nearly two decades of operator experience across enterprise software, technology and business strategy, governance, compliance, cybersecurity, mobile, SaaS, machine learning, agentic AI, and new product introduction.

Reject copy that carries only one part, substitutes a shorter domain list without reason, or replaces "nearly two decades" with a different quantifier.

### Invariant 3: Three RTBs at brandonwilburn.pro

The three approved evidence citations are:

- **Luma for Landslide.** Spirent's first agentic AI product, launched publicly February 18, 2026, roughly 16 months to first release.
- **Seven-Dimension enterprise adoption playbook.** Cleared agentic dev adoption through real legal and IP review, measured 20 to 40% throughput lift via DORA and DX surveys.
- **Spirent to Keysight acquisition close, October 2025.** Fifteen percent premium over Viavi's competing bid, four concurrent strategic initiatives, zero critical vulnerabilities at close.

Every substantive proof claim must map to one of these three or be explicitly documented at brandonwilburn.pro. Reject invented case studies, unsourced statistics, and confidential deal details that were not publicly disclosed.

### Invariant 4: Full name only in body copy

Write **"C9D Consulting"** in full in every prose reference. Never shortened to "C9D" alone in body copy. "C9D" appears standalone only in the wordmark, favicon, or metadata slugs.

### Invariant 5: Attribution required

**"A practice of Brandon Wilburn"** appears on any major surface: cover, footer, signature, about section. Written in full, with terminal period on signatures.

Reject variants:

- "A Brandon Wilburn practice"
- "By Brandon Wilburn"
- "From the practice of Brandon Wilburn"
- "A boutique practice by Brandon Wilburn"

### Invariant 6: Tagline system

Four locked constructs. Each has a specific role. No substitutions, paraphrases, or creative variations.

- **Primary tagline:** "The playbook, not the deck." (deliverable distinction)
- **Alternate tagline:** "Operator, not observer." (credential distinction, v2.3 lock)
- **Campaign tagline:** "Judgment across cycles." (multi-cycle claim)
- **Closing line, not a tagline:** "Coordinated, not improvised." (signature)

Shelf constructs like "We've shipped what we recommend" (v1.x alternate) and "Decades in the seat" (v2.0 draft) are allowed only in specific documented contexts.

### Invariant 7: 70/22/6/2 composition ratio

Locked. See Section A above.

### Invariant 8: Sodium amber indexes proof

Amber (D6743A) is used only to mark load-bearing components, decision nodes, main-flow arrows, case IDs, or approved status. Never decorative. Never on accent stripes or edge bars.

### Invariant 9: Classified red is rationed

Red (C0392B) appears only on refusals, kill nodes, error paths, crit-vulnerability call-outs. Never on titles, decorative elements, or general emphasis. Under 2% of the artifact by visual weight.

### Invariant 11: Deal-value framing on Spirent to Keysight

The credential is carried by **scope** (four concurrent strategic initiatives) and **premium** (fifteen percent over Viavi's competing bid). Deal value has been intentionally deprioritized in all copy. The $1.3B close figure is public record but is not used in positioning, hero copy, case cards, or credential footers. The "$600M to $1.3B trajectory" framing has been retired.

Reject copy that leads with $1.3B, uses "$600M to $1.3B", or otherwise centers the dollar close value.

### Invariant 12: Advising vs operating credential vocabulary lock

Use **"observers"** (never "watchers") when referring to the class of outside advisors. The distinction is drawn structurally, not moralistically. Reject copy that attacks advisors or treats their existence as evidence of poor judgment. Concede-first is required.

### Invariant 13: AI-forward architecture

Frame surfaces (hero, subtitle, meta rail, cover slides) lead with AI. Portfolio surfaces (about, credentials, engagement details) surface the broader operator credential. The engagement architecture stays domain-neutral (Decision Advisory, Posture and Diligence Review, Operating Partner Retainer).

### Invariant 15: Em-dashes are watched

Zero em-dashes in any C9D Consulting copy. See refuse-patterns.md Category 01.

### Invariant 18: Voice posture

Sage anchor plus Creator secondary. Diagnose, do not moralize. See Section E for the four voice principles with pass/fail criteria.

### Invariant 19: Dark by default

The Dossier is dark mode by default. Light mode is used only for print artifacts (Word docs, PDFs for printing, letterhead). Reject a screen artifact using light mode without a specific print-headed justification.

## Section E. Voice principles

Four principles. Every claim in C9D Consulting copy must pass all four.

### Principle 1: Evidence-first

**Rule:** Each substantive claim is defensible from CV, public record, or the artifact itself.

**Pass example:** "Nearly two decades operating inside technology firms across enterprise software, cybersecurity, mobile, SaaS, and agentic AI." (CV supports the timeframe and the domains.)

**Fail example:** "Most AI strategists have never shipped." (Market-level claim about competitors' career paths without a primary source.)

**Audit test:** For each substantive claim, ask "what is the source?" If the source is inference, cut or mark as inference. If the source is a market impression, cut or restructure as a first-person observation.

### Principle 2: Plain-named-precision

**Rule:** Roles, companies, waves, and domains are named specifically. Generic references fail.

**Pass example:** "Keysight acquired Spirent in October 2025 at fifteen percent premium over Viavi's competing bid."

**Fail example:** "A Fortune 500 acquirer completed the deal at a premium." (The actual companies are on public record.)

**Audit test:** For each generic reference, ask "is the specific version defensible?" If yes, name it. If no, cut or explain the reason for the generality.

### Principle 3: Concede-first

**Rule:** Where a competing position has genuine merit, the copy concedes it before differentiating.

**Pass example:** "Both credentials compound. They carry different kinds of judgment. C9D Consulting reasons from the operating credential."

**Fail example:** "Observers have their place, of course, but the operator credential is fundamentally more valuable." (The "of course" and "fundamentally" are hedges dressed as concessions.)

**Audit test:** Where the copy differentiates from a competitor, ask "does the competitor's position get a clean statement of merit?" If not, add one. If the concession reads as flattery or hedge, rewrite.

### Principle 4: Diagnose, do not moralize

**Rule:** Patterns are described structurally, not judgmentally.

**Pass example:** "An advisor's accountability ends when the SOW ends. An operator was inside the firm when the wave hit, accountable for the outcome long past when an advisor's engagement would have closed."

**Fail example:** "Advisors abandon their clients the moment the check clears. Operators actually stay and do the work." (Judgmental verbs "abandon" and "actually" moralize rather than describe.)

**Audit test:** For each differentiation, ask "does this describe a structural difference or a moral one?" Structural describes what is different in mechanics. Moral describes why one is better than the other. Cut moral, keep structural.

## Section F. Frame evolution history

Legacy artifacts may carry framing from earlier versions. Identify by version, note as legacy, do not use as source.

| Version | Frame | Status |
|---|---|---|
| v0 | Fractional CTO landing page | Retired, v0.app default. |
| v1.x | AI Strategy Advisory in five verticals | Retired in v2.0. Scope too narrow. |
| v2.0 through v2.2 | Operator Advisory and Strategy (portfolio-first) | Retired in v2.3. Buried the AI market pull. |
| v2.3 (current) | AI Strategy and Enablement plus Operator Advisory and Strategy | Current locked frame. |

If auditing an artifact and the frame does not match v2.3, note the version detected, flag as legacy, propose the v2.3 rewrite.

## Section G. Master brand relationship

The master brand at brandonwilburn.pro is out of scope for the guard. Never propose edits to brandonwilburn.pro from a C9D Consulting audit. Never assume brandonwilburn.pro shares the C9D Consulting frame directly. The two properties intentionally offer complementary engagement modes (brandonwilburn.pro carries operator role candidacy, c9d.consulting carries the advisory practice).

If an artifact ambiguously references both properties, hold the C9D Consulting scope and note the master brand reference as observed only.

## Snapshot integrity check

Before running an audit with this snapshot, verify:

1. Version tag reads v2.3 at the top of this file.
2. Section A tokens match the values in the main package `tokens.css`.
3. Section B typography matches the main package `tokens.css` type scale.
4. Section C logo filenames match the actual files in the main package `assets/logos/` directory.

If any mismatch is found, the snapshot is stale. Rebuild from the main package before proceeding, or attach the main package to the session and reference it directly.

## References to main package (not inlined)

For strategic depth beyond compliance verification, load the following from the main package if attached:

- Full manifesto text (v2.3): `references/foundation.md` under the Manifesto section.
- Full 21-invariant list including strategic invariants 10, 14, 16, 17, 20: `SKILL.md` at the root.
- Full voice library including Tier A vocabulary, refused vocabulary, tone flex matrix: `references/voice-library.md`.
- Engagement architecture, pricing, refuse list, qualification mechanics: `references/engagement-architecture.md`.
- Visual system detail beyond Section C (spatial system, federated Posture B, logo showcase): `references/visual-system.md`.
- Site copy surface-by-surface: `references/site-copy-v2.md`.
- Source chat: https://claude.ai/share/acdf57c3-1240-461e-a672-73205274fc0f.
