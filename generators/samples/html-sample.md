---
file_id: FILE-E02-2026-003
classification: CLIENT CONFIDENTIAL
title: AI Posture Review
subtitle: Findings from a two-week review of the model delivery pipeline
prepared_for: Northwind Analytics, Inc.
prepared_by: Brandon Wilburn, C9D Consulting
version: v1.0 · 2026.09.26
section_marker: E-02
---

# AI Posture Review

*What the review found, what it means for the Series C diligence window, and what to do first.*

## 1 · Summary

The model delivery pipeline is sound at the core and brittle at the edges. Three findings carry most of the risk, and all three are fixable inside one quarter by the team already in place.

**The short version.** Evaluation is manual, lineage stops at the training set, and nobody owns the rollback decision. An acquirer's counterparts will find all three in the first week.

## 2 · Findings

### Evaluation

Offline evaluation runs by hand before each release. The harness exists; it is not wired into the promotion gate.

| ID | Finding | Severity | Owner |
| --- | --- | --- | --- |
| F-01 | Evaluation is not a promotion gate | High | Platform |
| F-02 | Lineage stops at the training set | High | Data |
| F-03 | No named owner for rollback | Medium | Engineering |

### Lineage

- Training data is versioned in object storage.
- Feature definitions are not versioned alongside the model.
- Prompt templates live in application code with no release tag.

## 3 · Recommendations

1. Wire the existing harness into the promotion gate.
2. Version feature definitions and prompts with the model artifact.
3. Name the rollback owner and write the runbook.

#### Sequencing

Do the gate first. It makes the other two measurable, and it is the finding a diligence team will test directly. See the [DORA research](https://dora.dev) for the delivery metrics that frame it.
