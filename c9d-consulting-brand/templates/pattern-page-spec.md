# Pattern Page Spec

> **STATUS: PROPOSED, NOT LOCKED.**
>
> This specification applies The Dossier system to a Playbook Library page on c9d.consulting. It was not part of the locked source artifacts. Treat it as a starting point for review with the Principal, not as locked system.

A pattern is a platform-neutral solution design owned by C9D Consulting. One markdown file per pattern, in the dialect `generators/c9d_html_build.py` builds: `## NN · Title` sections, GFM tables, single-line lists, `**Lead-in.**` paragraphs, no raw HTML. The same source builds the site page and a standalone or PDF version.

## Front matter

```yaml
file_id: FILE-PAT-2026-001
classification: REFERENCE DESIGN
title: Governed Intake and Routing
subtitle: One line, plain, no refused vocabulary.
prepared_for: Public
prepared_by: C9D Consulting
version: v1.0
section_marker: P-01
pattern_id: P-01
evidence: none
engagement_shapes: [E-01]
platforms: [monday-com]
last_reviewed: 2026-09-30
```

| Key | Allowed values | Notes |
| --- | --- | --- |
| `classification` | `REFERENCE DESIGN`, `OPERATING EVIDENCE` | `OPERATING EVIDENCE` only when `evidence` is `anonymized` or `named` |
| `pattern_id` | `P-NN` | Matches `section_marker` |
| `evidence` | `none`, `anonymized`, `named` | `named` needs the Principal's sign-off |
| `engagement_shapes` | Engagement IDs published on the site | The shapes this pattern is delivered through |
| `platforms` | Platform page slugs | Each slug must resolve to a platform page |

## Sections, in fixed order

1. **Problem.** What the manual state costs, described plainly.
2. **Shape.** The steps of the pattern, platform-neutral.
3. **Control set.** Who reviews output, what data it touches, how it is monitored, how it is switched off, how an error is corrected. Mandatory.
4. **Measures.** Baseline, metric, and an example target labelled as an example.
5. **Handoff.** What the client team owns at the end: playbook, champions, runbook.
6. **Where it applies.** Links to platform pages.
7. **Engagement.** Which engagement shape delivers it, linking to the Engagement Specification.

## Claim rules

- A pattern claims a shape and a control set, not a result.
- While `evidence` is `none`, the page says in one sentence that it is a reference design.
- No statistic, client count, testimonial, certification or logo unless it is a measured result from the Evidence Library or a cited public source the Principal approves.

## Public and private depth

Published: problem, shape, control categories, measures, handoff, platform capability mapping. Never published: prompts, system instructions, board and data schemas, agent configurations, evaluation sets, integration code, client-specific variants.
