# Word Document Template Spec

> **STATUS: PROPOSED, NOT LOCKED.**
> 
> This template specification is Claude's structured application of The Dossier system to this output format. It was NOT in the locked §9 Visual Identity Doc or §10 Product/Offering Doc source artifacts. The locked source documented the brand foundation, visual tokens, voice library, and engagement architecture — not format-specific templates.
> 
> Treat this file as a starting point for discussion with Brandon, not as locked system. Specific patterns flagged below as **[proposed]** are derivable from locked tokens and rules; structures flagged as **[invented]** were created for this file and have no source. Review and lock with Brandon before treating as system.


The Dossier system applied to Word documents. Reports, memos, proposals, engagement letters, findings documents, and the playbook artifacts the practice ships with every engagement.

C9D Consulting Word documents are built by `generators/c9d_docx_build.py` from markdown with document front matter, the same source the PDF and HTML builds read. Do not hand-build them with the generic `docx` skill; the generator applies this spec. Decisions marked **[decided 2026.09.26]** were made by Brandon while fixing rendered documents and are implemented in layout v1.4 of the generator; they are locked for Word even though the rest of this file is still a proposal.

---

## Document type matrix

Six document types cover every standard deliverable. Resist creating new types; if a new type is needed, flag it.

| Type | Purpose | Length |
|---|---|---|
| D-01 Findings Document | Engagement findings report (E-01/E-02/E-03 main deliverable) | 20–60 pages |
| D-02 The Playbook | Re-runnable methodology document the client keeps | 15–40 pages |
| D-03 Proposal / SOW | Pre-engagement proposal or signed Statement of Work | 6–15 pages |
| D-04 Engagement Letter | Legal engagement letter (separate from SOW) | 2–4 pages |
| D-05 Memo | Short structured memo on a specific decision or finding | 2–8 pages |
| D-06 Weekly Status Note | Friday status to the engaged client | 1 page |

---

## Page setup (every document)

**Page size:** US Letter (8.5 × 11 inches).

**Margins:** **[decided 2026.09.26]**
- Top: 1.3 inch (clear air of about 0.4 inch between the header hairline and the first line of body)
- Bottom: 1.0 inch
- Left: 1.0 inch
- Right: 1.0 inch
- Header: 0.5 inch
- Footer: 0.5 inch

Body text, headings, lists, tables and rules all run the full 6.5 inch text block. There is no right-hand indent and no narrowed measure. The earlier 1.25 / 1.0 inch margins with body held to a 4.75 inch measure left an empty strip down the right of every page and were judged off-brand for print.

**Background:** White (this is a print-mode artifact). Use the light-mode token map from `references/visual-system.md` for color.

**Column structure:** Single column for body. Two-column allowed for comparison tables, decision registers, and risk registers.

---

## Header (every page except the cover)

Three-cell row, separated by 0.5pt `--rule-light` hairlines. Inter Tight 9pt for body, JetBrains Mono 8pt for metadata.

- Left cell: file ID in JetBrains Mono. Format: `FILE-E01-2026-014`.
- Center cell: classification in Inter Tight uppercase 8pt with letter-spacing 0.18em, color `--stamp-light`. Examples: `OPERATING EVIDENCE`, `CLIENT CONFIDENTIAL`, `DRAFT — NOT FOR DISTRIBUTION`.
- Right cell: section marker and page number in JetBrains Mono. Format: `§ 03 · 14 / 42`. The page number renders at the same 8pt as the marker (the field is written in separately formatted runs).

Cells are 2.0 / 2.5 / 2.0 inches with zero table cell margins, so the file ID starts exactly on the left margin.

Below the row: a 0.5pt `--rule-light` hairline spanning the full content width.

---

## Footer (every page except the cover)

Three-cell row, separated by 0.5pt `--rule-light` hairlines. Inter Tight 9pt.

- Left cell: "C9D Consulting" in Inter Tight 10pt. "C9D" in `--stamp-light`, "Consulting" in `--ink-light`.
- Center cell: "A practice of Brandon Wilburn" (no terminal period; `naming.founder.attribution` in `tokens.json`) in Inter Tight 9pt `--ink-mute-light`.
- Right cell: "c9d.consulting" in JetBrains Mono 9pt `--ink-mute-light`.

Same 2.0 / 2.5 / 2.0 inch cells as the header, so the attribution stays on one line.

Above the row: a 0.5pt `--rule-light` hairline spanning the full content width.

---

## Cover page (page 1 of every document type)

The cover has no header or footer. It carries the document's full identity. **[decided 2026.09.26]** The cover is always exactly one page, including in previewers that ignore embedded fonts and substitute a wider face: the file ID starts at the top margin, 48pt sits above the title and above the metadata table, and the metadata rows are kept together so the table never splits onto page 2.

**Composition top-to-bottom:**

- 1.5 inches from the top: file ID and classification on two lines.
  - Line 1: file ID in JetBrains Mono 11pt `--ink-mute-light`.
  - Line 2: classification in Inter Tight uppercase 9pt letter-spacing 0.18em color `--stamp-light`.
- 3 inches from the top: document title in Inter Tight 36pt weight 300 color `--ink-bright-light`. Letter-spacing -0.03em. Maximum two lines.
- Below the title: a 1pt `--rule-bright-light` line spanning 3 inches.
- Below the line, 0.3 inch gap: document subtitle in Inter Tight 18pt weight 350 color `--ink-mute-light`. Maximum one line.
- Mid-page (around 6 inches from top): metadata table. Five rows, JetBrains Mono 10pt for keys, Inter Tight 12pt for values, separated by `--rule-light` hairlines.

**Metadata rows:**

| Key (mono) | Value (Inter Tight) |
|---|---|
| `DOCUMENT` | The full title |
| `PREPARED FOR` | Client name or audience |
| `PREPARED BY` | Brandon Wilburn, C9D Consulting |
| `CLASSIFICATION` | See classification table below |
| `VERSION` | `v1.0 · 2026.06.17` |

- Bottom of page (around 9.5 inches from top): the wordmark and attribution block. C9D Consulting wordmark in Inter Tight 16pt with "C9D" in `--stamp-light` and "Consulting" in `--ink-bright-light`. Below: "A practice of Brandon Wilburn" (no terminal period) in Inter Tight 10pt `--ink-mute-light`. Below that: the closing signature in JetBrains Mono 8pt `--stamp-dim-light` (see Closing signature).

---

## Classification system

Every document carries one classification in the header and on the cover. Five values.

| Classification | Use |
|---|---|
| `OPERATING EVIDENCE` | Default for findings documents and playbooks delivered to clients |
| `CLIENT CONFIDENTIAL` | Drafts and working documents shared with the client during the engagement |
| `INTERNAL DRAFT` | Working documents not yet shared with the client |
| `SIGNED — ENGAGEMENT LETTER` | Executed legal engagement letters |
| `REFUSED` | Documents recording an engagement decline |

---

## Body typography (all body content)

**Font stack:** Inter Tight (with system fallback chain). JetBrains Mono for code, file IDs, metadata, classification stamps. Instrument Serif italic 11pt for inline emphasis and pullquotes only.

### Paragraph styles

| Style | Font | Size | Weight | Line height | Color |
|---|---|---|---|---|---|
| Title (cover only) | Inter Tight | 36pt | 300 | 1.05 | `--ink-bright-light` |
| H1 (section title) | Inter Tight | 24pt | 300 | 1.1 | `--ink-bright-light` |
| H2 (subsection) | Inter Tight | 18pt | 350 | 1.2 | `--ink-bright-light` |
| H3 (component title) | Inter Tight | 14pt | 500 | 1.3 | `--ink-bright-light` |
| H4 (inline tag) | JetBrains Mono | 10pt | 600 | 1.3 | `--stamp-light`, uppercase, ls 0.18em |
| Body | Inter Tight | 11pt | 400 | 1.6 | `--ink-light` |
| Body bold | Inter Tight | 11pt | 600 | 1.6 | `--ink-bright-light` |
| Body italic | Instrument Serif | 11pt | 400 italic | 1.6 | `--ink-light` |
| Small | Inter Tight | 9pt | 400 | 1.5 | `--ink-mute-light` |
| Mono inline | JetBrains Mono | 10pt | 500 | 1.5 | `--ink-light` |
| Mono block | JetBrains Mono | 10pt | 500 | 1.6 | `--ink-light`, in a `--bg-3-light` panel |
| Metadata | JetBrains Mono | 9pt | 500 | 1.4 | `--ink-mute-light`, uppercase, ls 0.10em |
| Pullquote | Instrument Serif | 18pt | 400 italic | 1.4 | `--stamp-light` |
| Caption | JetBrains Mono | 9pt | 500 | 1.4 | `--ink-mute-light` |

### Maximum measure

**[decided 2026.09.26]** Word documents use the full page width at standard margins. The 65-character measure (`spatial.measure` in `tokens.json`) is a screen rule and does not apply to Word; at 11pt across 6.5 inches, body lines run about 95 characters. Do not narrow the column or widen the margins to hold a measure.

### Section structure

Every major section opens with:

1. An eyebrow in H4 style ("FINDING 01", "THE PLAYBOOK", "DECISION POINT").
2. The H1 section title.
3. A 0.5pt `--rule-bright-light` horizontal rule spanning the column, set close under the title: no space after the title, and the paragraph carrying the rule is an exact 6pt line. **[decided 2026.09.26]**
4. A 12pt vertical space.
5. The body content.

---

## Tables

Tables are first-class in The Dossier. They appear in every engagement deliverable. Use the format.

**Header row:**
- Font: JetBrains Mono 9pt weight 600 uppercase letter-spacing 0.18em.
- Color: `--stamp-dim-light` text on `--bg-2-light` (light cream) background.
- Bottom border: 1pt `--rule-bright-light`.

**Body rows:**
- Font: Inter Tight 10pt weight 400.
- Color: `--ink-light` text on white background.
- Row separator: 0.5pt `--rule-light` hairline.
- No vertical separators.
- No alternating row backgrounds.

**Cell geometry:** **[decided 2026.09.26]**
- Left and right padding 0.1 inch in every cell, including the first and last column, so text never sits on the fill edge.
- Line height 1.15 inside cells. Top padding 5pt, bottom padding 2pt: the line box already carries the descent, so this measures about 7pt of air above the text and 7pt below. Equal top and bottom padding reads bottom-heavy.
- Header cells centred vertically; body cells top-aligned, so a label stays on the first line of a multi-line value.
- The header fill and row rules sit exactly on the 1.0 inch margins, flush with the section rules. Set the padding both per cell and as the table default, with the table indent equal to the left padding; LibreOffice otherwise shifts the table 0.025 inch off the margin.

**Status cells:**
Use the color system for status:
- Open / active: `--stamp-light`
- Resolved / closed: `--ink-mute-light`
- Refused / declined: `--classified-light`
- Critical / urgent: `--classified-light` with bold

---

## Lists

Lists in The Dossier are restrained.

### Refused list patterns

- Bullets with checkmark glyphs
- Numbered lists with parenthesized numbers (1) (2) (3)
- Nested lists more than two levels deep
- Long bullets that should be prose

### Allowed list patterns

**Unordered list (use sparingly):**
- En-dash (`–`) as the marker, color `--stamp-dim-light`
- Inter Tight 11pt for the body content
- Single-line bullets only; multi-line content goes in prose paragraphs

**Numbered list (preferred when sequence matters):**
- JetBrains Mono numbers in `--stamp-dim-light` (e.g., `01.`, `02.`, `03.`)
- Inter Tight 11pt for the body content
- Numbers are zero-padded to two digits

---

## Code blocks and mono blocks

Code, command-line examples, structured data:

- Background: `--bg-3-light` (cream inset).
- Border: 0.5pt `--rule-bright-light` on all sides.
- Padding: 12pt on all sides.
- Font: JetBrains Mono 10pt weight 500 color `--ink-light`.
- Line height: 1.6.
- Caption below: JetBrains Mono 9pt color `--ink-mute-light` uppercase letter-spacing 0.18em.

---

## Closing signature

**[decided 2026.09.26]** Every Word document carries the locked closing line (`naming.tagline` in `tokens.json`, "Coordinated, not improvised.") as the closing signature `→ COORDINATED, NOT IMPROVISED`, in JetBrains Mono caps with 0.18em tracking, in two places:

- At the end of the body, after a 0.5pt `--rule-light` hairline, 9pt weight 600 in `--stamp-light`, kept on the same page as the last body paragraph.
- On the cover, as the third footer line under the attribution, 8pt in `--stamp-dim-light`.

It is a closing line, not a tagline: never welded to the wordmark, never reworded, and never typed into the source; the generator places it.

---

## Specific document type notes

### D-01 Findings Document

Structure (suggested table of contents):

1. Executive summary (2 pages max)
2. Methodology (1 page)
3. Findings (8–40 pages — bulk of the document)
4. The threads most likely pulled (E-03 only)
5. Risk register (table)
6. Decision register (table)
7. The playbook (cross-reference to D-02)
8. Next steps and ongoing watch

Open with eyebrow `FINDINGS DOCUMENT · [ENGAGEMENT TYPE]`.

### D-02 The Playbook

Structure:

1. What this playbook does
2. When to run it
3. The diagnostic (re-runnable by the client)
4. The decision logic
5. The execution sequence
6. The kill criteria
7. The closeout

The playbook is the durable IP. It must be re-runnable by the client after the engagement closes. Every section answers a "what do I do" question, not "what did C9D Consulting do."

### D-03 Proposal / SOW

Structure:

1. Cover page
2. Background and engagement context (2 pages)
3. The engagement (D-03 names the engagement type, E-01/E-02/E-03/R-01)
4. Scope (specific deliverables, named)
5. Non-scope (what's explicitly out)
6. Timeline and milestones
7. Pricing (baseline floor with V2 justification if above baseline)
8. Lead operator and team
9. Acceptance criteria
10. Signatures

Pricing language uses the locked formulation from `references/engagement-architecture.md`: "from $185,000, fixed scope, fixed price, quoted to the specific scope, complexity, and stakes of the work."

### D-04 Engagement Letter

A short legal document. The brand chrome is the same; the body is legal language. The engagement letter is not the SOW; the SOW is operational.

### D-05 Memo

Short document for specific decisions. Skip the metadata table; use a one-line header instead:

> `MEMO · 2026.06.17 · [TOPIC] · BRANDON WILBURN → [RECIPIENT]`

### D-06 Weekly Status Note

One page. Five sections, exactly:

1. **Done this week** (3–5 lines)
2. **In flight** (3–5 lines)
3. **Blocked or watching** (1–3 lines)
4. **Next week** (3–5 lines)
5. **What you should know** (1–2 lines)

Closes with: "Coordinated, not improvised. — Brandon"

---

## Cross-references

Within a document, cross-reference other documents and assets using the asset ID:

- "See P-06 Decision Register Workbook (separate file)."
- "See §3 of this document."
- "See D-02 The Playbook delivered with this engagement."

---

## Refused Word patterns

- Default Word "Normal" style (Calibri 11pt)
- Headers using Times New Roman or any default serif
- Track changes left on in the delivered version
- Comments left in the delivered version
- Page numbers in the footer center without the JetBrains Mono treatment
- Hyperlinks in the default blue underline (use `--stamp-light` color and no underline)
- Bullet-point lists with 8+ bullets per section (rewrite as prose or split)
- "Confidentiality notice" walls of text at the bottom of every page (single classification stamp in the header is sufficient)
