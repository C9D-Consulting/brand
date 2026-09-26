# C9D Consulting Brand Audit Report Template

Standardized output format for every audit run against the C9D Consulting brand system. This template makes audit results iterable: a producer receives the report, addresses blockers, optionally addresses advisories, and can re-run the audit against the same template to close the loop.

## When to use this template

Every audit produced by the guard writes its output in this format. That includes:

- A full audit run against the checklist and refuse patterns.
- A quick 60-second check from `SKILL.md`.
- A follow-up audit after corrections.
- A batch audit of multiple artifacts (one report per artifact).

## Result modes

An audit resolves to one of three states.

**PASS.** No blockers, no advisories. Artifact ships as-is.

**PASS WITH ADVISORIES.** No blockers, one or more advisories. Producer may ship at their discretion. Advisories are documented for future artifacts and for the next audit iteration.

**FAIL.** One or more blockers. Artifact does not ship until every blocker is resolved. Advisories may accompany blockers but do not by themselves block shipping.

## Severity framework

Two levels. Simple. Binary decisions produce actionable feedback loops.

**BLOCKER.** Violates a locked invariant from `snapshot.md` Section D, a token from Section A, a typography rule from Section B, a logo rule from Section C, or Category 01 (em-dashes) from `refuse-patterns.md`. Must fix before ship.

**ADVISORY.** Violates a documented rule that reduces quality but does not violate a locked invariant. Includes AI slop patterns from `refuse-patterns.md` Categories 02 through 14, weak framing verbs, minor layout inconsistencies, and stylistic preferences. Producer may override with documented reason.

The distinction: blockers are things Brandon or a diligence-minded reader would spot as brand-broken. Advisories are things a careful editor would improve.

## The template

Fill every field. Do not omit sections that had no findings; write "None" instead. Empty sections erode the audit trail.

```markdown
# C9D CONSULTING BRAND AUDIT REPORT

**Artifact:** [filename, deck slide range, or one-line description]
**Artifact type:** [Word doc | PowerPoint deck | SVG diagram | Web page | Social banner | Image | Email signature | Written surface]
**Auditor:** [Claude session name or human name]
**Audit date:** [YYYY-MM-DD]
**Brand version:** v2.3
**Snapshot version:** v2.3
**Audit type:** [Quick check | Full audit]
**Iteration:** [n of n] (1 for first pass, increments on re-audit)

---

## RESULT: [PASS | PASS WITH ADVISORIES | FAIL]

- Blockers: [n]
- Advisories: [n]
- Sections audited: [n] of 8

---

## SECTION RESULTS

| Section | Status | Blockers | Advisories |
|---|---|---|---|
| 01. Copy | [PASS \| FAIL] | [n] | [n] |
| 02. Color | [PASS \| FAIL] | [n] | [n] |
| 03. Typography | [PASS \| FAIL] | [n] | [n] |
| 04. Evidence | [PASS \| FAIL] | [n] | [n] |
| 05. Logo | [PASS \| FAIL] | [n] | [n] |
| 06. Layout | [PASS \| FAIL] | [n] | [n] |
| 07. Signature | [PASS \| FAIL] | [n] | [n] |
| 08. Refuse patterns | [PASS \| FAIL] | [n] | [n] |

---

## BLOCKERS

Blockers must be resolved before the artifact ships. Fix every item below, then re-run the audit.

### BLOCKER-01

- **Section:** [01 through 08]
- **Rule:** [rule name from checklist or snapshot]
- **Rule source:** [snapshot.md § D, invariant N | audit-checklist.md § N | refuse-patterns.md § Category N]
- **Location in artifact:** [page 3 | slide 2, top-right | line 47 | SVG element ID | color reference in CSS]
- **Found:** "[exact quoted text or specific visual description]"
- **Correction:** [specific proposed fix, quoted if applicable]
- **Verification:** [how to verify the fix resolves the blocker]

### BLOCKER-02

[same structure]

[Repeat until all blockers listed. If none, write "None" and move to advisories.]

---

## ADVISORIES

Advisories are recommendations. Producer may address or override with documented reason.

### ADVISORY-01

- **Section:** [01 through 08]
- **Rule:** [rule name]
- **Rule source:** [file § section]
- **Location in artifact:** [where]
- **Found:** "[exact quoted text or description]"
- **Suggested correction:** [specific proposal]
- **Rationale:** [why this is advisory rather than blocker]

### ADVISORY-02

[same structure]

[Repeat. If none, write "None".]

---

## OBSERVATIONS

Non-blocking, non-advisory notes. Items that passed but are worth flagging for future work or context.

- [Observation 1]
- [Observation 2]
- [If none, write "None"]

---

## NEXT ACTIONS

### If RESULT is PASS

1. Ship artifact to [target surface: public site, client deck, internal review, print, social].
2. File audit report at [audit archive location].

### If RESULT is PASS WITH ADVISORIES

1. Review advisories with producer.
2. Ship artifact at producer's discretion (either after addressing advisories or as-is with a note).
3. File audit report with disposition of each advisory (accepted, deferred, overridden with reason).

### If RESULT is FAIL

1. Return this report to the producer.
2. Producer addresses every BLOCKER-* item.
3. Producer optionally addresses ADVISORY-* items.
4. Re-run audit with iteration number incremented.
5. Repeat until RESULT is PASS or PASS WITH ADVISORIES.

---

## AUDIT TRAIL

- **This iteration:** [n]
- **Previous audit:** [link, filename, or "None (first iteration)"]
- **Corrections since previous:** [list of BLOCKER-* IDs resolved from previous iteration, or "N/A"]
- **Advisories addressed since previous:** [list of ADVISORY-* IDs resolved, or "N/A"]
- **New findings this iteration:** [list of new BLOCKER-* or ADVISORY-* IDs added, or "None"]

---

## SIGN-OFF

- **Audited by:** [Claude session or human name]
- **Reviewed by:** [Brandon Wilburn, agency partner, or "Self-audit"]
- **Sign-off date:** [YYYY-MM-DD or "Pending"]
- **Disposition:** [Ship | Return to producer | Escalate to strategic review]
```

## Worked example

Below is a filled report for a hypothetical LinkedIn banner audit. Use this as a reference for the level of specificity expected.

```markdown
# C9D CONSULTING BRAND AUDIT REPORT

**Artifact:** c9d-banner-linkedin-personal-1584x396.png
**Artifact type:** Social banner
**Auditor:** Claude, session claude-2026-09-25-abc
**Audit date:** 2026-09-25
**Brand version:** v2.3
**Snapshot version:** v2.3
**Audit type:** Full audit
**Iteration:** 1 of 1

---

## RESULT: FAIL

- Blockers: 3
- Advisories: 2
- Sections audited: 8 of 8

---

## SECTION RESULTS

| Section | Status | Blockers | Advisories |
|---|---|---|---|
| 01. Copy | FAIL | 2 | 0 |
| 02. Color | PASS | 0 | 0 |
| 03. Typography | PASS | 0 | 0 |
| 04. Evidence | FAIL | 1 | 0 |
| 05. Logo | PASS | 0 | 0 |
| 06. Layout | PASS | 0 | 1 |
| 07. Signature | PASS | 0 | 0 |
| 08. Refuse patterns | PASS | 0 | 1 |

---

## BLOCKERS

### BLOCKER-01

- **Section:** 01. Copy
- **Rule:** Frame language (v2.3)
- **Rule source:** snapshot.md § D, invariant 1
- **Location in artifact:** Banner subtitle, x=48px y=280px
- **Found:** "Operator Advisory and Strategy for growth-stage decisions"
- **Correction:** "AI Strategy and Enablement, delivered by an operator across cycles"
- **Verification:** Subtitle must open with "AI Strategy and Enablement" per v2.3 frame lock.

### BLOCKER-02

- **Section:** 01. Copy
- **Rule:** Tagline exactness
- **Rule source:** snapshot.md § D, invariant 6
- **Location in artifact:** Banner tagline, x=48px y=330px
- **Found:** "The playbook, not the pitch deck."
- **Correction:** "The playbook, not the deck."
- **Verification:** Primary tagline is locked at exactly four words. No variations permitted.

### BLOCKER-03

- **Section:** 04. Evidence
- **Rule:** Deal-value framing
- **Rule source:** snapshot.md § D, invariant 11
- **Location in artifact:** Banner credential line, x=48px y=360px
- **Found:** "$600M portfolio, $1.3B close"
- **Correction:** "Four concurrent initiatives, fifteen percent premium close"
- **Verification:** Deal value is deprioritized in v2.0 onwards. Scope and premium carry the credential, not the dollar figures.

---

## ADVISORIES

### ADVISORY-01

- **Section:** 06. Layout
- **Rule:** Whitespace consistency
- **Rule source:** audit-checklist.md § 06, Whitespace
- **Location in artifact:** Left-edge margin
- **Found:** Left margin measures 32 pixels, less than the 48-pixel minimum applied on other banners in the set.
- **Suggested correction:** Increase left margin to 48 pixels to match OG banner and X banner spacing.
- **Rationale:** Consistency across the banner set improves brand recognition. Not a blocker because 32 pixels remains readable and does not violate a locked rule.

### ADVISORY-02

- **Section:** 08. Refuse patterns
- **Rule:** Adverb padding (Category 06)
- **Rule source:** refuse-patterns.md § Category 06
- **Location in artifact:** Banner attribution line, x=48px y=380px
- **Found:** "Truly operator-grade advisory"
- **Suggested correction:** "Operator-grade advisory" (drop "truly").
- **Rationale:** "Truly" is an adverb that adds no information and reads as AI-generated emphasis.

---

## OBSERVATIONS

- Colors and typography audit cleanly against v2.3 tokens. No token drift detected.
- Logo lockup used is the endorsed horizontal wordmark on dark ground, correct choice for a LinkedIn personal banner.
- Banner set was produced under v1.x positioning and needs a full re-render, not just the fixes above. Recommend batching the fix with re-renders of the other four banners (OG, LinkedIn company, X header, Reddit) to keep the set consistent.

---

## NEXT ACTIONS

### If RESULT is FAIL

1. Return this report to the producer.
2. Producer addresses BLOCKER-01, BLOCKER-02, BLOCKER-03.
3. Producer optionally addresses ADVISORY-01 and ADVISORY-02.
4. Re-run audit with iteration 2.
5. Consider batching with re-renders of the other four v1.x banners per Observations.

---

## AUDIT TRAIL

- **This iteration:** 1
- **Previous audit:** None (first iteration)
- **Corrections since previous:** N/A
- **Advisories addressed since previous:** N/A
- **New findings this iteration:** BLOCKER-01, BLOCKER-02, BLOCKER-03, ADVISORY-01, ADVISORY-02

---

## SIGN-OFF

- **Audited by:** Claude, session claude-2026-09-25-abc
- **Reviewed by:** Pending
- **Sign-off date:** Pending
- **Disposition:** Return to producer
```

## Report filing convention

Save each audit report at:

```
c9d-consulting-brand/audits/YYYY-MM-DD-[artifact-slug]-iter-[n].md
```

Example:

```
c9d-consulting-brand/audits/2026-09-25-c9d-banner-linkedin-personal-iter-1.md
```

This filing convention makes the audit history discoverable, keyed by artifact and iteration. When re-auditing, the previous iteration is easy to find and cite in the "Previous audit" field.

## When to escalate rather than audit

Some findings are not audit failures; they are strategic questions that the guard cannot resolve. Escalate rather than audit when:

- A copy line proposes a new frame beyond v2.3 (e.g. a fifth tagline construct).
- An artifact requires a new lockup that is not in `snapshot.md` Section C.
- A color choice proposes extending the token palette.
- A refuse-list rule (`c9d-consulting-brand/references/engagement-architecture.md`) needs updating based on an observed pattern.
- The audit surfaces a positioning inconsistency between C9D Consulting and brandonwilburn.pro.

In these cases, write the audit report with the finding noted as an escalation rather than as a blocker or advisory, and route to Brandon for strategic review.

## Automation notes

Because this format is structured, an audit report can be parsed programmatically. Fields to key on:

- `RESULT:` (single-line, values PASS | PASS WITH ADVISORIES | FAIL)
- `BLOCKER-NN` (per-blocker sections, keyed by ID)
- `ADVISORY-NN` (per-advisory sections, keyed by ID)
- `AUDIT TRAIL` (structured for tracking iterations)

Automated tools can consume these reports to track compliance metrics over time (blocker rate per artifact type, most common failure categories, iteration count to reach PASS) or to produce a compliance dashboard for the practice.

## Version

Audit report template v1.0, aligned with c9d-brand-guard v2.3 and c9d-consulting-brand v2.3.
