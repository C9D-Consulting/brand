# Platform Page Spec

> **STATUS: PROPOSED, NOT LOCKED.**
>
> This specification applies The Dossier system to a Playbook Library page on c9d.consulting. It was not part of the locked source artifacts. Treat it as a starting point for review with the Principal, not as locked system.

A platform page maps C9D Consulting patterns onto one vendor's capabilities, states the relationship with that vendor, and routes the reader to an engagement shape. One markdown file per platform, in the dialect `generators/c9d_html_build.py` builds.

## Front matter

```yaml
file_id: FILE-PLT-2026-001
classification: REFERENCE DESIGN
title: AI Enablement on monday.com
subtitle: One line, plain, no refused vocabulary.
prepared_for: Public
prepared_by: C9D Consulting
version: v1.1
section_marker: monday.com
vendor: monday.com
vendor_slug: monday-com
relationship: independent
program: null
partner_tier: null
compensation: none
patterns: [P-01, P-03]
capabilities_verified_on: 2026-09-30
sources: [https://example.com/vendor-docs]
last_reviewed: 2026-09-30
```

| Key | Allowed values | Notes |
| --- | --- | --- |
| `classification` | `REFERENCE DESIGN`, `OPERATING EVIDENCE` | |
| `relationship` | `independent`, `partner` | `partner` only once accepted. An application in progress is published as `independent`. |
| `program` | Text or `null` | The program as the vendor names it. Required when `relationship` is `partner`. |
| `partner_tier` | Text or `null` | Only if formally awarded |
| `compensation` | `none`, `referral`, `resale`, `program_subsidy`, or omitted | When omitted, no compensation line is rendered and the body makes no compensation statement |
| `patterns` | Pattern IDs | Each must resolve to a pattern page |
| `sources` | URLs | Vendor documentation behind every capability fact |
| `capabilities_verified_on` | Date | When the capability facts were last checked against `sources` |

## Sections, in fixed order

1. **Relationship line.** Rendered from front matter, directly under the cover.
2. **Why this platform.** When it is the right place for the patterns, and when it is not.
3. **Capability map.** Vendor capability to what C9D Consulting uses it for. Facts only from `sources`, named as the vendor names them.
4. **Patterns applied.** Table of pattern ID, name, the platform capabilities it uses, and a link.
5. **Method.** Assess, align, adopt.
6. **Readiness.** The five dimensions.
7. **Measures.** Example targets labelled as examples.
8. **Engagement.** How this is bought, linking to the Engagement Specification and the request-for-engagement section. Never a vendor's site as the call to action.

## Relationship and compensation wording

| `relationship` / `compensation` | Line |
| --- | --- |
| `independent` / `none` | Independent. C9D Consulting has no commercial relationship with the vendor and receives no compensation from it. |
| `partner` / omitted | Partner: the program name. |
| `partner` / `referral` | Partner: the program name. C9D Consulting may receive referral compensation from the vendor; it is disclosed in every proposal. |
| `partner` / `resale` | Partner: the program name. Licences can be purchased through C9D Consulting; margin is disclosed in every proposal. |
| `partner` / `program_subsidy` | Partner: the program name. The vendor may fund part of the engagement through its program; the funding is shown in the proposal. |

## Rules

- A vendor program whose name contains a refused word is referred to by its acronym or a neutral description.
- No vendor logos, partner tiers, certifications or prices that cannot be verified from `sources` or a formal award.
- No page disparages another vendor.
