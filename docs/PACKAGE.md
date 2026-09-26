# C9D Consulting Brand Skills, v2.3

Two companion Claude skills for the C9D Consulting brand system (The Dossier).

A practice of Brandon Wilburn.

## What is in this archive

```
c9d-brand-skills-v2.3/
├── README.md                     This file
│
├── c9d-consulting-brand/         Main brand package (76 files, 4.6 MB)
│   ├── SKILL.md                  Entry point, 21 strategic invariants
│   ├── README.md                 Package overview and file map
│   ├── references/               Strategic foundation (5 files)
│   ├── templates/                Working templates (Word, PowerPoint, architecture diagrams, specs)
│   └── assets/                   Design tokens, logos, banners (57 files)
│
└── c9d-brand-guard/              Compliance verifier (5 files, 71 KB)
    ├── SKILL.md                  Entry point, 60-second check
    ├── snapshot.md               Inlined brand data for standalone operation
    ├── audit-checklist.md        Detailed audit workflow
    ├── refuse-patterns.md        AI slop and banned pattern library
    └── audit-report.md           Standardized output format
```

## What each skill does

**c9d-consulting-brand** is the strategic foundation and production asset library. Load it when producing a new C9D Consulting artifact, referencing brand strategy, using logo lockups, or applying design tokens. It carries the full 21 invariants, the v2.3 manifesto, engagement architecture, voice library, and every production logo and banner.

**c9d-brand-guard** is the compliance verifier. Load it when auditing an artifact for brand compliance, checking a written surface against voice principles, or approving an artifact before it ships. It runs standalone (via its inline snapshot) or alongside the main package (for full strategic depth).

## The relationship

The main package produces artifacts. The guard verifies them.

The guard's `snapshot.md` is a v2.3-locked extract of the compliance-relevant portions of the main package. That extract makes the guard runnable without the main package attached. When both are attached, the guard escalates strategic questions (new frame, new lockup, palette extension, positioning inconsistency) to the main package for resolution.

Both skills carry the same version tag: v2.3. When the strategic foundation moves (v2.4 or later), both rebuild together. Do not mix versions.

## Install

Move both folders into your Claude user skills directory:

```
/mnt/skills/user/c9d-consulting-brand/
/mnt/skills/user/c9d-brand-guard/
```

Or drop them both into a project's working directory to scope both skills to that project.

Both skills auto-load based on their `description` tags in `SKILL.md`. The main package triggers on any C9D Consulting artifact production. The guard triggers on any C9D Consulting artifact production, audit, review, or approval question. In practice, both fire together when you are producing an artifact, and the guard fires alone when you are only auditing.

## Which skill loads when

| Situation | Skills that load |
|---|---|
| Producing a new C9D Consulting artifact | Both. Main package for strategy, guard for compliance verification. |
| Auditing an existing C9D Consulting artifact | Guard alone (standalone via snapshot). Main package if attached, for strategic escalation. |
| Answering a strategic question about C9D Consulting positioning | Main package alone. |
| Answering a compliance question ("is this on brand") | Guard alone. |
| Editing a locked artifact after brand version change | Both, at the new matched version. |

## Version discipline

Both skills are locked at v2.3. The guard's `snapshot.md` mirrors the compliance-relevant portions of the main package at that exact version. If either version moves independently, the guard's audits produce false positives (against outdated rules) or false negatives (miss new rules).

When you rebuild for v2.4 or later, rebuild both together and update the `snapshot_version`, `main_package_version`, and `audit_report_format` fields in the guard's `SKILL.md` frontmatter to match.

## Version history

v2.3, current. AI Strategy and Enablement as cornerstone frame, Operator Advisory and Strategy as differentiator, "Operator, not observer" alternate tagline locked, observers vocabulary locked, deal-value framing (scope plus premium, not dollar) locked, guard added as companion skill with standardized audit report format.

Earlier versions in the main package `README.md`.

## Source

Brand system built and iterated across sessions. Current source chat: https://claude.ai/share/acdf57c3-1240-461e-a672-73205274fc0f.

## Version tag

v2.3, C9D Consulting brand skills, a practice of Brandon Wilburn.

Coordinated, not improvised.
