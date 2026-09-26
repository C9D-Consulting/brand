---
name: c9d-brand-guard
description: Verify that any visual asset, document, deck, diagram, web mockup, banner, icon, or written surface is on brand for C9D Consulting (The Dossier system, v2.3). Use this skill whenever the user asks Claude to produce, review, audit, correct, or approve a visual or written artifact intended to carry the C9D Consulting brand, or when a user question implies brand compliance (e.g. "is this on brand", "does this match C9D Consulting", "can I use this", "check this against the brand"). Load this skill BEFORE producing a new C9D Consulting artifact, and BEFORE approving an existing one. This skill runs standalone via the inline v2.3 snapshot; for full strategic depth, load the main c9d-consulting-brand package alongside.
license: Proprietary. C9D Consulting LLC. A practice of Brandon Wilburn.
snapshot_version: v2.3
main_package_version: v2.3
audit_report_format: v1.0
---

# C9D Consulting Brand Guard, v2.3

Compliance verifier for The Dossier brand system. When any visual asset, document, deck, diagram, or written surface carries the C9D Consulting name, run this check.

## Deployment mode

This skill runs standalone. All compliance data required for verification (tokens, typography, logos, invariants 1 through 13, voice principles, frame evolution) is inlined at `snapshot.md`. The main c9d-consulting-brand package is not required for a compliance audit.

For strategic depth (full manifesto, strategic invariants 14 through 21, engagement architecture, voice library detail, site copy history), load the main c9d-consulting-brand package alongside this skill.

Snapshot and main package are locked at matching version v2.3. If either version moves, both must move together to prevent version skew.

## When to use

Load this skill when Claude is asked to:

1. Produce a new visual asset for C9D Consulting (logo application, banner, icon, favicon, deck, doc, diagram, web mockup, social graphic, email signature).
2. Audit or review an existing artifact for brand compliance.
3. Correct or adjust an artifact that failed a brand check.
4. Approve an artifact before it ships to a client, publication, or public surface.
5. Answer any user question of the form "is this on brand", "does this match", "can I use this for C9D Consulting".

Load this skill in addition to any format-specific skill (pptx, docx, xlsx). Run brand-guard BEFORE the format skill applies its generic guidance, then again AFTER as a final check.

## Files in this skill

| File | Contents |
|---|---|
| SKILL.md | Entry point, deployment mode, 60-second check, routing to other files. |
| snapshot.md | Full inline brand data. Tokens, typography, logo inventory, compliance invariants, voice principles, frame history. Locked at v2.3. |
| audit-checklist.md | Detailed audit workflow. Seven sections plus refuse-patterns run. |
| refuse-patterns.md | AI slop and banned pattern library. Fourteen categories. |
| audit-report.md | Standardized output template with worked example. |

## The 60-second check

For quick sanity checks. When any C9D Consulting artifact is being produced or reviewed, verify every item below. Any blocker fails the check.

### Quick copy check

1. Full name written as **"C9D Consulting"** in every prose reference. `C9D` alone appears only in wordmark, favicon, or metadata slugs.
2. Attribution **"A practice of Brandon Wilburn"** on any major surface (cover, footer, signature).
3. Any tagline matches one of four locked constructs, character-for-character:
   - Primary: `The playbook, not the deck.`
   - Alternate: `Operator, not observer.`
   - Campaign: `Judgment across cycles.`
   - Closing line: `Coordinated, not improvised.`
4. Frame reads AI-first, operator-second. Hero copy leads with `AI Strategy and Enablement`, followed by `Operator Advisory and Strategy` as qualifier.
5. Zero em-dashes. Use periods, commas, colons, en-dashes for ranges only.
6. Vocabulary lock: `observers` (never `watchers`).

### Quick color check

Every color used matches a token from `snapshot.md` Section A. No blue, no green, no gradients, no client-brand color imports.

Dark mode default for screens: ground `#0C0B08`, ink `#D8CDB8`, signal amber `#D6743A`, classified red `#C0392B`.

Light mode for print only: ground `#F5F1E8`, ink `#2E2820`, signal amber `#9C4F24`, classified red `#8B2A20`.

### Quick typography check

Three faces only: Inter Tight (body, headlines, wordmark), Instrument Serif (italic accents only), JetBrains Mono (metadata, eyebrows, file IDs). Never Arial, Helvetica, Times, Calibri, Aptos, Georgia as primary.

### Quick composition check

70 ground / 22 ink / 6 signal / 2 crit. Amber under 6% by visual weight. Red under 2%. Left-align body copy. Center only titles that carry weight.

### Quick logo check

Correct lockup for the surface: horizontal wordmark for default, stacked for narrow, mono for single-color print, endorsed for attribution-visible, tagline lockup for cover surfaces, square icon for app icon and favicon. Never invent a lockup or modify wordmark spacing, weight, color, or letter treatment.

### Quick layout check

No accent bars or color stripes along card edges. No drop shadows. No gradients. Rounded corners 0px default, 2px maximum on buttons. Minimum 0.5 inch margins on print, 24 to 48 pixels on screen.

### Quick refuse patterns check

Zero em-dashes. No "X, not Y" constructions beyond the three locked taglines. No fake concessions ("both approaches have their place"). No meta-commentary about the writing. No consulting-firm vocabulary (leverage, utilize, ideate, learnings, reach out, thought leader).

## The full audit

When the 60-second check surfaces any risk, or when the artifact is high-stakes (public site, client engagement cover, board deck, investor material, published social banner), run the full audit from `audit-checklist.md`. Seven sections cover copy, color, typography, evidence, logo, layout, signature. Plus the refuse-patterns library.

Full audit produces a standardized report per the format in `audit-report.md`.

## The audit output

Every audit (quick or full) resolves to one of three states.

**PASS.** No blockers, no advisories. Ship as-is.

**PASS WITH ADVISORIES.** No blockers, one or more advisories. Producer ships at their discretion.

**FAIL.** One or more blockers. Producer must fix before shipping, then re-run the audit.

Two severity levels. **Blocker:** violates a locked invariant, token, typography rule, logo rule, or Category 01 (em-dashes) from refuse patterns. Must fix. **Advisory:** violates a documented rule that reduces quality but does not violate a locked invariant. Producer may override with documented reason.

Every audit report follows the template in `audit-report.md`. Every finding is quoted from the artifact, cited to a specific rule, and proposed with a specific correction. See the worked example in `audit-report.md` for the level of specificity expected.

## When to escalate

Some findings are strategic questions the guard cannot resolve. Escalate rather than audit when:

- A copy line proposes a new frame beyond v2.3.
- An artifact requires a new lockup not in `snapshot.md` Section C.
- A color choice proposes extending the token palette.
- The refuse list needs updating based on an observed pattern.
- An audit surfaces a positioning inconsistency between C9D Consulting and brandonwilburn.pro.

Write the audit with the finding noted as an escalation rather than as a blocker or advisory, and route to Brandon for strategic review.

## Version discipline

This snapshot is v2.3, matched to c9d-consulting-brand v2.3. When the main package moves to v2.4 or later, this guard requires a rebuild to match. Do not mix versions. The guard's snapshot is authoritative for compliance during the version it is locked to; the main package remains authoritative for strategic decisions at all times.

## Related files

**Inlined (available without main package):**

- `snapshot.md` in this skill directory. Tokens, typography, logo inventory, invariants 1 through 13, voice principles.
- `audit-checklist.md` in this skill directory. Full audit workflow.
- `refuse-patterns.md` in this skill directory. AI slop and banned pattern library.
- `audit-report.md` in this skill directory. Standardized output template.

**Referenced (require main package if attached):**

- Full manifesto text (v2.3): `c9d-consulting-brand/references/foundation.md` under Manifesto.
- Full 21-invariant list including strategic invariants 10, 14, 16, 17, 20: `c9d-consulting-brand/SKILL.md` at the root.
- Full voice library including Tier A vocabulary, refused vocabulary, tone flex matrix: `c9d-consulting-brand/references/voice-library.md`.
- Engagement architecture, pricing, refuse list, qualification: `c9d-consulting-brand/references/engagement-architecture.md`.
- Visual system detail (spatial system, federated Posture B, logo showcase): `c9d-consulting-brand/references/visual-system.md`.
- Site copy surface-by-surface: `c9d-consulting-brand/references/site-copy-v2.md`.
- Token source files: `c9d-consulting-brand/assets/tokens.css` and `tokens.json`.
- Logo asset files: `c9d-consulting-brand/assets/logos/`.
- Source chat: https://claude.ai/share/acdf57c3-1240-461e-a672-73205274fc0f.
