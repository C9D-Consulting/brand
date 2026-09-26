# Excel Template Spec

> **STATUS: PROPOSED, NOT LOCKED.**
> 
> This template specification is Claude's structured application of The Dossier system to this output format. It was NOT in the locked §9 Visual Identity Doc or §10 Product/Offering Doc source artifacts. The locked source documented the brand foundation, visual tokens, voice library, and engagement architecture — not format-specific templates.
> 
> Treat this file as a starting point for discussion with Brandon, not as locked system. Specific patterns flagged below as **[proposed]** are derivable from locked tokens and rules; structures flagged as **[invented]** were created for this file and have no source. Review and lock with Brandon before treating as system.


The Dossier system applied to Excel workbooks. Decision registers, risk registers, qualification grids, financial models, and the P-06/P-07 playbook artifacts the practice ships with every engagement.

When creating a C9D Consulting workbook, use the generic `xlsx` skill for mechanics (openpyxl, formulas, cell styling) and layer this spec on top for the brand decisions.

---

## Workbook structure

Every C9D Consulting workbook opens with a cover sheet and a metadata row across each working sheet. The format is consistent across deliverables; only the working sheets change.

### Standard sheet structure

| Sheet | Purpose |
|---|---|
| `Cover` | Title, metadata table, table of contents |
| `Metadata` | Document chrome data referenced by all sheets |
| `Index` | List of sheets with descriptions |
| `[working sheets]` | The body of the workbook |
| `Refs` | Reference tables and lookups |
| `Notes` | Notes, assumptions, definitions |

---

## Color palette in Excel

Excel doesn't carry CSS variables; the colors are applied directly. Use the light-mode token map (workbooks are typically reviewed in light mode and may be printed).

| Token | Hex | Excel use |
|---|---|---|
| `--bg-light` | `#f5f1e8` | Default sheet background (set on every sheet) |
| `--bg-2-light` | `#ebe5d6` | Header row backgrounds, summary row backgrounds |
| `--bg-3-light` | `#e0d8c5` | Inset block backgrounds, metadata table backgrounds |
| `--rule-light` | `#c8bda5` | Cell borders, standard hairlines |
| `--rule-bright-light` | `#a89c82` | Emphasized borders, table outer borders |
| `--ink-bright-light` | `#1a1612` | Headlines, important numbers |
| `--ink-light` | `#2e2820` | Default body text and numbers |
| `--ink-mute-light` | `#5a5042` | Supporting text, metadata, units |
| `--ink-dim-light` | `#8a7e6a` | Faint annotations, page numbers |
| `--stamp-light` | `#9c4f24` | Header labels, key metric callouts, framework names |
| `--stamp-dim-light` | `#6b3818` | Footer text, stamp interiors |
| `--classified-light` | `#8b2a20` | Refusal markers, critical risk cells |

---

## Cover sheet

The first sheet of every workbook. No data; only identity.

**Layout:**

- Set the entire sheet background to `--bg-light`.
- A2: classification stamp in Inter Tight uppercase 11pt letter-spacing 1.8 color `--stamp-light`. Examples: `OPERATING EVIDENCE`, `CLIENT CONFIDENTIAL`.
- A4: file ID in JetBrains Mono 11pt color `--ink-mute-light`. Format: `FILE-E01-2026-014`.
- A8: workbook title in Inter Tight 36pt weight 300 color `--ink-bright-light`. Merge cells A8:H8.
- A10: a `--rule-bright-light` border on the bottom of the row, spanning A10:D10 only (3 inches at default column width).
- A12: workbook subtitle in Inter Tight 16pt weight 350 color `--ink-mute-light`. Merge cells A12:H12.
- A16:B22: metadata table. Five rows. Column A is mono labels in JetBrains Mono 10pt `--stamp-dim-light` uppercase letter-spacing 1.8; column B is values in Inter Tight 11pt `--ink-light`. Borders are 0.5pt `--rule-light` hairlines.

**Metadata table rows:**

| A (mono) | B (Inter Tight) |
|---|---|
| `DOCUMENT` | The full title |
| `PREPARED FOR` | Client name |
| `PREPARED BY` | Brandon Wilburn, C9D Consulting |
| `CLASSIFICATION` | Operating Evidence |
| `VERSION` | `v1.0 · 2026.06.17` |

- A28: wordmark cell. Merge A28:D28. Set Inter Tight 14pt with "C9D" in `--stamp-light` and "Consulting" in `--ink-bright-light`. (Excel doesn't easily mix two colors in one cell; use rich text formatting in the cell value.)
- A29: attribution. "A practice of Brandon Wilburn." Inter Tight 10pt color `--ink-mute-light`.

Hide gridlines on the cover sheet (View > Gridlines off).

---

## Working sheet header (rows 1–6 of every working sheet)

Every working sheet carries a standardized 6-row header that mirrors the chrome on a Word document page.

**Row 1:** file ID. Merged A1:C1. JetBrains Mono 9pt `--ink-mute-light`. Format: `FILE-E01-2026-014 · § 04 · DECISION REGISTER`.

**Row 2:** classification stamp. Merged A2:C2. Inter Tight uppercase 9pt letter-spacing 1.8 color `--stamp-light`.

**Row 3:** sheet title. Merged A3:C3. Inter Tight 20pt weight 300 color `--ink-bright-light`.

**Row 4:** sheet subtitle. Merged A4:F4. Inter Tight 12pt weight 400 color `--ink-mute-light`.

**Row 5:** empty (visual breathing).

**Row 6:** column headers for the working table.

Set rows 1–4 background to `--bg-light`. Set row 5 to white. Set row 6 to `--bg-2-light` (the table header background). Apply 1pt `--rule-bright-light` bottom border to row 6.

---

## Table conventions

### Header row (row 6 of every working sheet)

- Background: `--bg-2-light`.
- Font: JetBrains Mono 9pt weight 600 uppercase letter-spacing 1.5.
- Color: `--stamp-dim-light`.
- Vertical alignment: middle.
- Horizontal alignment: left for text columns, right for number columns.
- Bottom border: 1pt `--rule-bright-light`.

### Body rows

- Background: white.
- Font: Inter Tight 10pt weight 400.
- Color: `--ink-light`.
- Vertical alignment: middle.
- Row separator: 0.5pt `--rule-light` hairline (bottom border on each row).
- No vertical separators between columns.
- No alternating row backgrounds.

### Status cells

Status columns use the color system:

- `Open` / `Active`: text color `--stamp-light`, weight 500.
- `Resolved` / `Closed`: text color `--ink-mute-light`, weight 400.
- `Refused` / `Declined`: text color `--classified-light`, weight 500.
- `Critical`: text color `--classified-light`, weight 600, with a `--bg-3-light` cell background.

### Number formatting

- Currency: `$#,##0` (no decimals for thousands; `$#,##0.00` for under $1,000).
- Percent: `0.0%`.
- Counts: `#,##0`.
- Dates: `YYYY.MM.DD` in JetBrains Mono 10pt.

Right-align all number cells. Number columns are narrower by default (1.5 inches); text columns are wider (3–5 inches).

---

## P-06 Decision Register Workbook (locked template)

The decision register is delivered with every engagement. Locked column structure:

| Column | Header (mono) | Type | Width |
|---|---|---|---|
| A | `ID` | Text (e.g., `DEC-014`) | 0.9 in |
| B | `DECISION` | Text | 4.0 in |
| C | `OWNER` | Text | 1.5 in |
| D | `OPENED` | Date | 1.0 in |
| E | `STATUS` | Status enum (Open / Resolved / Refused) | 1.0 in |
| F | `RESOLVED` | Date or blank | 1.0 in |
| G | `RATIONALE` | Text | 3.5 in |
| H | `SOURCE` | Text (engagement reference) | 1.5 in |

Freeze row 6 (header) so the table headers stay visible during scroll.

Add a summary row at the bottom (e.g., row 100) with:
- `TOTAL OPEN: =COUNTIF(E7:E99,"Open")`
- `TOTAL RESOLVED: =COUNTIF(E7:E99,"Resolved")`
- `TOTAL REFUSED: =COUNTIF(E7:E99,"Refused")`

The summary row uses `--bg-3-light` background, JetBrains Mono 10pt, `--ink-bright-light` color, and a 1pt `--rule-bright-light` top border.

---

## P-07 Risk Register Workbook (locked template)

| Column | Header (mono) | Type | Width |
|---|---|---|---|
| A | `ID` | Text (e.g., `RSK-008`) | 0.9 in |
| B | `RISK` | Text | 4.0 in |
| C | `CATEGORY` | Enum (Engineering / Security / Operational / Commercial / People) | 1.5 in |
| D | `LIKELIHOOD` | Enum (Low / Medium / High) | 1.0 in |
| E | `IMPACT` | Enum (Low / Medium / High / Critical) | 1.0 in |
| F | `EXPOSURE` | Currency or text | 1.2 in |
| G | `MITIGATION` | Text | 3.5 in |
| H | `OWNER` | Text | 1.5 in |
| I | `STATUS` | Status enum (Open / Mitigated / Accepted / Escalated) | 1.2 in |

Apply conditional formatting on the IMPACT column:
- "Critical" cell background: `--classified-light` with white text.
- "High" cell text: `--stamp-light` weight 600.
- "Medium" cell text: `--ink-light`.
- "Low" cell text: `--ink-mute-light`.

---

## Charts

Charts in C9D Consulting workbooks use the constrained color palette. No default Office chart colors.

### Chart color sequence (for multi-series)

1. `--stamp-light` (`#9c4f24`)
2. `--ink-light` (`#2e2820`)
3. `--stamp-dim-light` (`#6b3818`)
4. `--ink-mute-light` (`#5a5042`)
5. `--stamp-light` at 60% opacity
6. `--ink-dim-light` (`#8a7e6a`)

Five series maximum per chart. If more are needed, split the chart.

### Chart styling

- Chart background: white (no fill).
- Plot area background: white.
- Axis lines: 0.5pt `--rule-light`.
- Axis labels: JetBrains Mono 9pt `--ink-mute-light` uppercase letter-spacing 1.8.
- Data labels: JetBrains Mono 9pt `--ink-light`.
- Legend: Inter Tight 9pt `--ink-mute-light`. Positioned at the bottom, horizontal.
- No gridlines on the X axis. Light gridlines on the Y axis (0.5pt `--rule-light` dashed).
- Chart title: Inter Tight 12pt weight 500 `--ink-bright-light`, left-aligned above the chart.

### Refused chart types

- 3D charts of any kind
- Pie charts with more than 5 slices
- Donut charts
- Stacked area charts with more than 3 series
- Charts using the default Office theme colors

---

## Footer (every working sheet)

Add a footer row at the very bottom of the printable area (typically row 50 or wherever the print area ends).

- A: "C9D Consulting" — Inter Tight 10pt with "C9D" in `--stamp-light` and "Consulting" in `--ink-bright-light`.
- B-D (merged): "A practice of Brandon Wilburn." — Inter Tight 9pt `--ink-mute-light`.
- E-F (merged): "c9d.consulting" — JetBrains Mono 9pt `--ink-mute-light`, right-aligned.

Apply a 0.5pt `--rule-light` top border to the footer row.

---

## Print setup

For workbooks that may be printed (engagement letters, signed deliverables):

- Page orientation: Landscape for wide tables; portrait for narrow tables.
- Margins: Normal (0.75 inch).
- Header (page setup, repeats on every page): file ID left, classification center, page number right (`Page &P of &N`).
- Footer: "C9D Consulting · A practice of Brandon Wilburn · c9d.consulting" centered.
- Scaling: Fit to 1 page wide for most tables.
- Print gridlines: off.
- Print row and column headers: off.

---

## Refused Excel patterns

- Default Office theme colors anywhere in the workbook
- Calibri or any default sans (use Inter Tight throughout)
- Multi-colored conditional formatting heatmaps with the default red-yellow-green gradient (the system has no green)
- Comments shown as red triangles in cells (use a separate `Notes` sheet)
- Excel's default cell borders (use the `--rule-light` and `--rule-bright-light` system)
- Pivot tables styled with the default pivot styles (apply the system styling manually)
- Sheet tab colors (leave tabs unstyled, or use `--stamp-light` for currently-active sheets only)
- Workbooks delivered with unprotected formula cells (lock formulas; allow input cells)
- Workbooks delivered with sample data still in them
