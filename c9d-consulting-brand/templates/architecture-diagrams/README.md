# Architecture Diagrams — The Dossier

Five reusable diagram templates plus a Mermaid theme config. All follow the same visual system as the site, decks, and Word artifacts.

## Files in this directory

| File | When to use |
|---|---|
| `system-architecture-template.svg` | System / component architecture. Multiple layers of technical components with connections. |
| `decision-framework-template.svg` | Decision tree with branching logic. YES / NO / KILL paths. |
| `timeline-roadmap-template.svg` | Engagement or project timeline. Phases with milestone markers. |
| `org-chart-template.svg` | Organization hierarchy. Reporting lines with load-bearing role emphasis. |
| `data-flow-template.svg` | Input → Transform → Output flow with error routing. |
| `mermaid-theme.json` | Config for Mermaid-generated diagrams (flowchart, sequence, gantt, state, ER, class). |

Each `.svg` has a matching `.png` alongside it — the PNG is a rendered preview for quick reference. Edit the `.svg` directly in a code editor (Cursor, VS Code) or a vector editor (Figma with SVG import, Illustrator, Inkscape). The PNG regenerates from the SVG when needed.

## Visual language

The five templates share the same encoding conventions. Learn once, apply everywhere.

### Color roles

| Role | Token | Hex | Where it appears |
|---|---|---|---|
| Ground | `--bg` | `#0C0B08` | Diagram background |
| Elevated ground | `--bg-2` | `#131210` | Standard boxes and nodes |
| Insetblock | `--bg-3` | `#1A1815` | Emphasis boxes (load-bearing, decision nodes) |
| Rule | `--rule` | `#2A2620` | Standard hairlines, standard box borders |
| Rule bright | `--rule-bright` | `#3D362C` | Emphasized borders, active state |
| Ink bright | `--ink-bright` | `#F0E6D0` | Node titles |
| Ink | `--ink` | `#D8CDB8` | Node body text |
| Ink mute | `--ink-mute` | `#8A7E6A` | Supporting labels, metadata |
| Ink dim | `--ink-dim` | `#5A5042` | Standard connection lines, arrows |
| Signal (sodium amber) | `--stamp` | `#D6743A` | Load-bearing components, decision nodes, main-flow arrows |
| Signal dim | `--stamp-dim` | `#8A4824` | Load-bearing outlines, secondary signal, eyebrows |
| Classified (red) | `--classified` | `#C0392B` | Kill/stop-call node text |
| Classified dim | `--classified-dim` | `#8B2A20` | Kill/stop-call outlines, error-path arrows |

### Encoding conventions

**A component's border color encodes its role:**
- Standard component: `--rule` border, `--bg-2` fill
- Emphasis component: `--rule-bright` border, `--bg-3` fill
- Load-bearing component: `--stamp-dim` border at 1.5px, `--bg-3` fill
- Kill / stop-call node: `--classified-dim` border at 1.5px, `--bg-3` fill or `#1A1210`

**A connection's color encodes its type:**
- Standard flow: `--ink-dim` line, standard arrowhead
- Main / primary flow: `--stamp-dim` line at 1.5px, amber arrowhead
- Error / retry path: `--classified-dim` dashed line, red arrowhead
- Reporting line (org chart only): `--ink-dim` line, no arrowhead

**Eyebrows sit above every logical group:**
- Uppercase mono in `--stamp-dim`, letter-spacing `0.18em`
- Label the layer, tier, phase, or lane the group belongs to
- No punctuation

### Typography

- **Titles / body:** `Inter Tight`
- **Labels / metadata / captions:** `JetBrains Mono`
- **Italic accents:** `Instrument Serif` — rarely used in architecture diagrams; keep for prose surfaces

### Composition rules

- **70 / 22 / 6 / 2** — ground / ink / signal / crit. Don't exceed 6% amber usage. Kill/red should be under 2%.
- **Left-align content within nodes.** Never center body text.
- **Uniform box widths within a layer / tier / lane.** Variable widths only when semantically meaningful (composite boxes spanning multiple columns).
- **Hairline rules between layers.** 0.5–1px, `--rule` color, full width.

## Editing the SVG templates

Every template has three consistent zones:

1. **Top chrome** (y: 0–52): file ID left, classification stamp center, section marker right, hairline rule below.
2. **Figure header** (y: 90–195): eyebrow, title, subtitle, short rule.
3. **Diagram body** (y: 200 onwards): the actual content.
4. **Bottom chrome** (last 60px): hairline rule, caption text, C9D Consulting attribution.

Keep the chrome zones consistent when editing — they establish the artifact register. The diagram body is where you swap real content in.

### Common edits

**Replace a component:**
```xml
<!-- Find the group for the component you want to replace -->
<g transform="translate(40, 260)">
  <rect x="0" y="0" width="200" height="80" class="box-fill-standard" />
  <text x="16" y="24" class="box-meta">01</text>            <!-- Update ID -->
  <text x="16" y="46" class="box-title">Component A</text>  <!-- Update title -->
  <text x="16" y="66" class="box-body">Standard description</text>  <!-- Update body -->
</g>
```

**Mark a component as load-bearing:**
Change the class from `box-fill-standard` to `box-fill-signal`. Also change the title text to use the `box-title-amber` class.

**Update the section marker in top chrome:**
Change `§ FIG-01 / ARCHITECTURE` in the `chrome-section` text to whatever describes your specific figure.

## Mermaid theme config

For AI-generated or code-generated diagrams (flowcharts, sequence diagrams, gantt charts, etc.), use `mermaid-theme.json`. The file contains inline usage examples and covers every Mermaid diagram type with C9D Consulting Dossier tokens.

### Quick start (HTML)

```html
<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    const themeVariables = /* paste themeVariables object from mermaid-theme.json */;
    mermaid.initialize({ startOnLoad: true, theme: 'base', themeVariables });
  </script>
</head>
<body style="background: #0C0B08">
  <pre class="mermaid">
    flowchart TB
      Trigger[Decision triggered] --> Q{Question one?}
      Q -->|Yes| Ship[Ship]
      Q -->|No / Kill| Stop[Stop call]
      style Stop stroke:#8B2A20,fill:#1A1210
  </pre>
</body>
</html>
```

### Quick start (Mermaid file with front-matter)

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#1A1815', 'primaryBorderColor':'#8A4824', 'primaryTextColor':'#F0E6D0', 'lineColor':'#5A5042', 'background':'#0C0B08', 'fontFamily':'Inter Tight, sans-serif' }}}%%

flowchart LR
  A[Input] --> B[Transform]
  B --> C[Output]
```

## When to use SVG vs Mermaid

**Use the SVG templates when:**
- You need pixel-perfect control over layout and styling
- The diagram will be embedded in a deck, Word doc, or a PDF
- You want to hand-edit the diagram after generation
- The diagram is a signature artifact for a specific engagement

**Use Mermaid when:**
- The diagram is generated from code, data, or an LLM
- You need many diagrams that follow the same visual system
- The diagram will be embedded in Markdown or documentation
- Speed of iteration matters more than pixel-level precision

## What NOT to do

- **Don't use gradients.** The Dossier is flat by design.
- **Don't use drop shadows.** They read as consulting-firm decoration.
- **Don't use rounded corners on standard components.** Radius max 2px for buttons, 0 for content boxes.
- **Don't use color outside the tokens.** No blue, green, or other palette additions.
- **Don't fill boxes with color.** Only outlines carry semantic meaning. Fills are ground / elevated ground / inset — never signal color.
- **Don't overload amber.** If more than 6% of the diagram is amber, remove some emphasis.
- **Don't leave classification stamp on a public artifact.** Change `CLIENT CONFIDENTIAL` to the appropriate value for public / share / internal use.

## Adding a new template

If you build a new architecture diagram type (network topology, sequence diagram in SVG, sankey, etc.), copy an existing template as a starting point to inherit:
- The top chrome layout
- The figure header layout
- The color token references in the `<style>` block
- The bottom chrome layout

Then replace only the diagram body. Save alongside the others in this directory with a matching `.png` preview.
