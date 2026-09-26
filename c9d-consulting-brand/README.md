# C9D Consulting Brand Package — v2.3

The Dossier system as a full brand package: strategic foundation, verified tokens, production logo assets, plus working templates for Word, PowerPoint, architecture diagrams, and Mermaid.

A practice of Brandon Wilburn.

---

## What's in this package

```
c9d-consulting-brand/
├── SKILL.md                                    # Entry point — 21 invariants
├── README.md                                   # This file
│
├── references/                                 # Brand foundation (load these first)
│   ├── foundation.md                           # v2.3 positioning, POD, RTBs, manifesto
│   ├── visual-system.md                        # Color, typography, logo system, spatial
│   ├── voice-library.md                        # Tagline system, vocabulary, voice principles
│   ├── engagement-architecture.md              # E-01 / E-02 / R-01, pricing, refuse list
│   └── site-copy-v2.md                         # Surface-by-surface site update text
│
├── templates/                                  # Working templates
│   ├── c9d-consulting-word-template.docx       # Dossier light mode — cover, styles, tables
│   ├── c9d-consulting-deck-template.pptx       # Dossier dark mode — 6 slide types
│   ├── architecture-diagrams/                  # 5 SVG templates + Mermaid theme
│   │   ├── README.md                           # Visual language + editing guide
│   │   ├── system-architecture-template.svg    # Multi-layer component boxes
│   │   ├── decision-framework-template.svg     # Branching logic + kill criteria
│   │   ├── timeline-roadmap-template.svg       # Phased timeline + milestones
│   │   ├── org-chart-template.svg              # Hierarchy + reporting lines
│   │   ├── data-flow-template.svg              # Inputs / transform / outputs + errors
│   │   ├── mermaid-theme.json                  # Dossier tokens for Mermaid
│   │   └── *.png                               # PNG previews of each SVG
│   ├── docx-spec.md                            # Word design spec
│   ├── pptx-spec.md                            # PowerPoint design spec
│   ├── xlsx-spec.md                            # Excel design spec
│   ├── web-spec.md                             # Web application spec
│   ├── outbound-spec.md                        # Email / signature spec
│   └── gamma-spec.md                           # Gamma deck reference spec
│
└── assets/
    ├── tokens.css                              # CSS variables (dark + light + print modes)
    ├── tokens.json                             # Structured tokens for design tooling
    └── logos/                                  # 50+ production logo assets
        ├── README.md
        ├── logo-showcase.html / .png           # Overview of all lockups
        ├── c9d-consulting-wordmark-*.svg       # Horizontal, stacked, mono (dark + light)
        ├── c9d-consulting-endorsed-*.svg       # Endorsed lockup with attribution
        ├── c9d-consulting-with-tagline-*.svg   # Tagline lockup
        ├── c9d-monogram-stamp.svg              # Original monogram (superseded)
        ├── c9d-icon-square-*.svg / .png        # Live-site-aligned square icon (64–512)
        ├── c9d-favicon-*.png                   # Favicon sizes (16–512, plus 180 Apple)
        ├── c9d-banner-*.png                    # OG, LinkedIn (personal + company), X, Reddit
        └── audit/                              # Alignment audits + comparisons
```

---

## Version history

**v2.3 — Current.** AI Strategy & Enablement as cornerstone frame with Operator Advisory & Strategy as differentiator. AI-forward messaging. Full brand package: Word template, PowerPoint template, five architecture diagram templates, Mermaid theme config.

**v2.2.** "Observers" vocabulary lock; SOW-boundedness axis added to the advising-vs-operating credential distinction.

**v2.1.** Advising-vs-operating credential distinction replaces the market-level assertion about single-cycle advisors. Defensibility problem in v2.0 opening fixed.

**v2.0.** Repositioned from AI Strategy Advisory in five verticals (v1.x, too narrow) to Operator Advisory & Strategy for growth-stage decisions. RTB 3 corrected — "$600M → $1.3B trajectory" language subsequently backed out in favor of scope + premium framing. Refuse list restructured from vertical-refusal to engagement-shape-refusal. Manifesto restructured. Federated Posture B locked as an invariant. brandonwilburn.pro out of scope.

**v1.1.** Rebuild against verified source after v1.0 accuracy audit.

**v1.0.** Initial reconstruction from locked source artifacts. Pulled after audit.

---

## What's in each layer

### references/

The strategic core. Every artifact derives from these decisions.

- **foundation.md** — v2.3 positioning ("operator-grade practice for AI Strategy & Enablement"), two-part POD (AI cornerstone + operator differentiation), contrarian belief, primary alternative (observers whose accountability ends with the SOW), three RTBs, 60-second script, six attribute pairs, four voice principles, and the v2.3 manifesto (opens on AI market surge, uses credential distinction to explain why C9D is the exception, lands the arc, closes on portfolio-as-support).
- **visual-system.md** — Color tokens (dark + light + print), typography (Inter Tight / Instrument Serif / JetBrains Mono), the 70/22/6/2 composition ratio, logo system, spatial system, federated Posture B architecture.
- **voice-library.md** — Full tagline system (Primary "The playbook, not the deck." / Alternate "Operator, not observer." / Campaign "Judgment across cycles." / Closing "Coordinated, not improvised."), Tier A owned vocabulary, refused vocabulary, competitor-territory list, voice principles.
- **engagement-architecture.md** — Three engagement categories (E-01 Decision Advisory, E-02 Posture & Diligence Review, R-01 Operating Partner Retainer), pricing structure, qualification mechanics, delivery system, six-refusal list.
- **site-copy-v2.md** — Ten site surfaces with current copy, v2.3 replacement text, and phased rollout suggestions.

### templates/

Working files ready to use.

- **c9d-consulting-word-template.docx** — Dossier light mode. Cover page with wordmark, meta chrome (file ID / classification / section marker), header and footer chrome on every page, H1/H2/H3 styles, body text, callout box with left amber border, pullquote in italic accent, decision-metadata block, custom amber bullets, mono numbered lists, register table with color-coded status cells, close section with signature block.
- **c9d-consulting-deck-template.pptx** — Dossier dark mode. Six slide types: (S-01) Cover with wordmark + title, (S-02) Section divider with elevated ground, (S-03) Content slide with claim + body + pullquote + evidence citation, (S-04) Register table with color-coded status, (S-05) Metrics/callout with three big-number panels, (S-06) Close slide with locked signature.
- **architecture-diagrams/** — Five SVG templates for common diagram patterns (system architecture, decision framework, timeline/roadmap, org chart, data flow), a Mermaid theme config for AI-generated diagrams, and a README documenting the visual language.
- **docx-spec.md**, **pptx-spec.md**, **xlsx-spec.md**, **web-spec.md**, **outbound-spec.md**, **gamma-spec.md** — Design specs for each format. Reference documents for anyone building a new artifact from scratch outside the working templates above.

### assets/

Drop-in design tokens and logo assets.

- **tokens.css / tokens.json** — CSS variables (dark default, light mode for print, print media query) and structured JSON for design tooling.
- **logos/** — Every logo asset: primary horizontal wordmark, stacked wordmark (centered on shared midline), mono wordmark, endorsed lockup with attribution, tagline lockup, monogram stamp, square icon aligned with live c9d.consulting production treatment, favicons at every size, and banner PNGs for OG / LinkedIn personal / LinkedIn company / X header / Reddit. All SVGs are text-editable; PNGs at production resolutions.

---

## How to install as a Claude skill

Move the entire `c9d-consulting-brand/` directory into your user skills folder:

```
/mnt/skills/user/c9d-consulting-brand/
```

Claude will auto-load the skill when a C9D Consulting deliverable is in scope. Triggers are documented in `SKILL.md` (any mention of C9D Consulting, c9d.consulting, a specific engagement type, a deck / Word / spreadsheet / website / email for C9D Consulting, or anything bearing "A practice of Brandon Wilburn").

---

## How to use the templates directly

### Word

Open `c9d-consulting-word-template.docx` in Word or Google Docs. Fonts render properly if Inter Tight, Instrument Serif, and JetBrains Mono are installed on the reader's system — install once from Google Fonts and forget it. Save As with a specific filename per deliverable. Every style is pre-defined; replace content, keep styles.

### PowerPoint

Open `c9d-consulting-deck-template.pptx` in PowerPoint, Keynote, or Google Slides. Six slide types are pre-built. Duplicate a slide to add more of the same type. Same font installation note as Word — install Inter Tight / Instrument Serif / JetBrains Mono once from Google Fonts.

### Architecture diagrams

Open the `.svg` templates in a code editor (Cursor, VS Code) or vector editor (Figma with SVG import, Illustrator, Inkscape). Edit XML directly to change component labels, add new boxes, or restructure. See `templates/architecture-diagrams/README.md` for the visual language reference.

For AI-generated diagrams (via Mermaid), use `mermaid-theme.json` — inline usage examples in the file.

---

## Non-negotiable invariants (v2.3)

Full list in `SKILL.md`. Headline:

1. **AI Strategy & Enablement is the cornerstone frame, delivered as Operator Advisory & Strategy.** Site subtitles and lead surfaces open with AI.
2. **Two-part POD.** Part A: AI Strategy & Enablement is the leading offering. Part B: nearly two decades of operator experience is what makes the AI work defensible.
3. **Three RTBs at brandonwilburn.pro** — Luma / Seven-Dimension + DORA / Spirent → Keysight.
4. **Full name only in body copy.** "C9D Consulting." Never "C9D" alone.
5. **Attribution required.** "A practice of Brandon Wilburn" on every major surface.
6. **Tagline system:** Primary "The playbook, not the deck." Alternate "Operator, not observer." Campaign "Judgment across cycles." Closing line (NOT a tagline) "Coordinated, not improvised."
7. **70/22/6/2 composition ratio.**
8. **Sodium amber indexes the proof.** Never decorative.
9. **Classified red is rationed.** Refusals only.
10. **Refuse engagement shapes, not domains** (v2.0).
11. **Deal-value framing on Spirent → Keysight** (v2.0): scope + premium carry the credential, not the dollar close.
12. **Advising vs operating credential distinction** (v2.2): position axis + accountability-duration axis. Vocabulary lock: "observers" (never "watchers").
13. **AI-forward architecture** (v2.3): lead surfaces with AI, back with portfolio, keep engagement architecture domain-neutral.
14. **Federated Posture B** (v2.0 Option C): c9d.consulting and brandonwilburn.pro offer complementary engagement modes in parallel. brandonwilburn.pro is out of scope for this skill.
15. **Em-dashes are watched.**
16. **Sequential, not parallel.** One engagement at a time.
17. **The retainer is the exit pattern.** R-01 does not start cold.
18. **Voice posture:** Sage anchor + Creator secondary. Diagnose, don't moralize.
19. **The Dossier is dark by default.** Light mode is constrained to print artifacts.

---

## Version

`v2.3 · 2026 · The Dossier · C9D Consulting · A practice of Brandon Wilburn`

Coordinated, not improvised.
