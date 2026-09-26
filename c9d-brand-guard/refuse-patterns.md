# C9D Consulting Refuse Patterns

Banned patterns and AI-slop detection library. Run copy against this file before shipping. Any hit is a fail. Examples are concrete: reject exact matches and structural variants.

The categories below are ordered by frequency of occurrence in AI-generated copy. Category 01 (em-dashes) is the highest-signal, highest-frequency failure and should be checked first.

## Category 01. Em-dashes

**Rule:** No em-dashes anywhere in C9D Consulting copy. This is a locked user preference and the single most reliable AI-generated writing signal.

**Reject:**

- Any occurrence of the character `—` (Unicode U+2014).
- Two consecutive hyphens `--` where they would be auto-corrected to an em-dash in Word or Google Docs.
- Any usage where an em-dash is functioning as a parenthetical break, an emphasis pause, or a sentence connector.

**Approved alternatives:**

- Period. Break the sentence.
- Comma. Continue the thought.
- Colon: introduce the elaboration.
- Semicolon; connect the related clause.
- En-dash (`–`, Unicode U+2013) for numeric ranges only, such as 20–40% or Series A–D.
- Parentheses (for actual asides).

**Examples of failure:**

- "The playbook — not the deck." (should be "The playbook, not the deck.")
- "Operator, not observer — the credential distinction." (drop the em-dash portion or restructure)
- "AI Strategy & Enablement — the cornerstone of the practice." (should be "AI Strategy & Enablement. The cornerstone of the practice." or "AI Strategy & Enablement, the cornerstone of the practice.")

## Category 02. "X, not Y" repetition

**Rule:** The "X, not Y" construction is a locked brand rhetorical device (primary tagline, alternate tagline, closing line). Because it is locked in specific places, it must not appear elsewhere in the same artifact more than once. Over-use degrades the signature.

**Approved usages (locked, always allowed):**

- "The playbook, not the deck." (primary tagline)
- "Operator, not observer." (alternate tagline)
- "Coordinated, not improvised." (closing line)

**Reject unlocked usages:**

- "Signal, not noise."
- "Substance, not style."
- "Delivered, not proposed."
- "Diagnosed, not moralized."
- "Shipped, not planned."
- "Working, not aspirational."

Any "X, not Y" construction in body copy that is not one of the three locked taglines is a fail. It reads as brand-mimicry rather than brand.

## Category 03. Concessions that are actually flattery

**Rule:** Concede-first is a real voice principle. Fake concessions that exist only to hedge or flatter are AI-slop.

**Reject copy that:**

- Concedes a competitor's approach is "valid" or "right" or "excellent" when the underlying claim is that C9D Consulting is different, not that competitors are wrong.
- Uses "both approaches have their place" without specifying which situations map to which approach.
- Hedges every substantive claim with "of course", "naturally", "obviously", "certainly".

**Examples of failure:**

- "The observer's credential is valuable, real, and important. Ours is simply different." (empty flattery to soften the differentiation)
- "Both credentials compound wonderfully, each in its own way." (adverbs doing the flattery work)
- "Neither approach is right or wrong, better or worse. They are simply distinct." (three ways of saying the same thing with no added information)

**Approved concession pattern:**

- "Both credentials compound. They carry different kinds of judgment. C9D Consulting reasons from the operating credential."

This concedes both credentials are real, names the specific difference (kinds of judgment), and states which side C9D operates from. Every word carries information.

## Category 04. Meta-commentary about the writing

**Rule:** The copy should say things, not describe the moves it is making. Meta-commentary is AI-slop.

**Reject copy that:**

- Explains the rhetorical device it just used.
- Announces the transition to the next section.
- Signals that it is being contrarian or bold.
- Draws attention to its own structure.

**Examples of failure:**

- "As we have established, the pattern is structural." (drop "As we have established")
- "This is the contrarian move: we lead with AI." (just lead with AI without announcing it)
- "The concede-first move here is load-bearing." (this is meta, belongs in the brand guide, not in copy)
- "Before we get to the diagnosis, some context." (drop the meta transition)

## Category 05. Chiasmus and inverted-parallel constructions

**Rule:** ChatGPT and Claude default to chiastic constructions ("X does Y; Y does not X") when trying to sound insightful. In small doses this is fine. In accumulation it is a slop signal.

**Reject patterns like:**

- "The buyer who needs to be sold does not need this; the buyer who needs this does not need to be sold."
- "AI strategy done by an operator is different from operator work done by an AI strategist."
- "The advisor observes what the operator lives; the operator lives what the advisor observes."
- "We do not do what we recommend; we recommend what we do."

**Rule of thumb:** If the sentence structure would work equally well flipped or rearranged, and it feels clever, cut or rewrite. Real claims survive translation; slop dies under rewrite.

## Category 06. Adverb padding

**Rule:** AI-generated prose overuses adverbs to signal emphasis it did not earn.

**Reject:**

- "Genuinely", "truly", "actually", "really", "fundamentally", "essentially", "importantly".
- "Ultimately", "critically", "significantly", "dramatically".
- "Uncommonly", "distinctly", "uniquely".
- Repeated intensifiers stacked on the same claim.

**Examples of failure:**

- "This is genuinely different from the market." (drop "genuinely")
- "The operator credential is fundamentally more durable." (drop "fundamentally")
- "We uniquely combine..." (never use "uniquely"; the claim should stand on specifics)

## Category 07. Curly-quote and typography slop

**Rule:** Use straight quotes (`"` and `'`) in source files unless the render environment requires curly quotes for typography rendering. Never mix.

**Reject:**

- Mixed curly and straight quotes within one artifact.
- Curly single quotes used for apostrophes when the surrounding text uses straight quotes.
- The wrong direction curly quote (an opening quote where a closing should be, or vice versa).

## Category 08. Corporate-consulting vocabulary

**Rule:** C9D Consulting speaks in operator vocabulary, not consulting-firm vocabulary.

**Reject:**

- "Leverage" as a verb.
- "Utilize" (use "use").
- "Solutioning".
- "Ideate", "ideation".
- "Bandwidth" (as a metaphor for time or capacity).
- "Move the needle".
- "Circle back".
- "Deep dive" (as a noun).
- "Best-in-class", "world-class", "cutting-edge", "state-of-the-art".
- "At scale" when not specifying what scale.
- "Enterprise-grade" when not specifying which enterprise standard.
- "Mission-critical" (either explain what fails when it breaks or cut).
- "Trusted advisor" (the reader decides, C9D Consulting does not claim it).
- "Thought leader", "thought leadership".
- "Value proposition" in copy (the concept can exist in strategy documents; the phrase should not appear in surfaces).
- "Synergy", "synergies".
- "Alignment" when meaning "agreement".
- "Learnings" (use "lessons" or "what we learned").
- "Reach out" (use "email", "call", "message", "contact").

**Approved operator vocabulary:**

- "Ship", "shipped", "shipping".
- "Cleared", "signed", "documented".
- "In production", "at close", "under diligence".
- "On the hook", "on the record".
- "Playbook" (yes; it is in the primary tagline).
- "Register" (as in decision register).
- "Cadence".

## Category 09. Weak framing verbs

**Rule:** Verbs should carry specific, testable meaning. Weak framing verbs allow the writer to avoid taking a position.

**Reject:**

- "Enables", "empowers", "unlocks", "delivers value", "drives outcomes".
- "Helps [someone] to [do something]" (specify what "help" means).
- "Provides [thing]" (specify what "provides" means; often "sells", "gives", "ships", or "documents" is more accurate).
- "Supports", "facilitates" (both are weak; specify the actual action).

**Approved specific verbs:**

- "Ships", "clears", "documents", "signs", "runs", "leads", "advises", "diagnoses", "recommends", "refuses".

## Category 10. False specificity

**Rule:** Numbers, percentages, and quantifiers that are stated without a source read as manufactured.

**Reject:**

- Percentages that cannot be traced to a specific measurement (survey, dashboard, DORA metric).
- "Over 90%" or "more than 80%" statistics that are not documented.
- Named "frameworks" that are not real (invented three-part frameworks with alliterative names).
- Numbered lists ("The Seven Pillars", "The Four Principles") that are actually collapsed versions of a paragraph.

**Approved specificity:**

- "20 to 40% throughput lift, measured via DORA + DX surveys, six teams."
- "Nearly two decades" (defensible against CV).
- "Fifteen percent premium over Viavi's competing bid" (public record).
- "Four concurrent strategic initiatives" (documented).
- "Zero critical vulnerabilities at close" (documented).

## Category 11. Imagery and metaphor slop

**Rule:** The Dossier voice is document-grade, not literary. Metaphors carry weight only when they earn it.

**Reject:**

- Journey metaphors ("your journey", "the roadmap ahead").
- Battle metaphors ("winning the war for talent", "the AI battle").
- Weather metaphors ("navigate the storm", "weather the change").
- Sports metaphors ("moving the ball", "in the red zone").
- Musical metaphors ("orchestrate", "harmony", "rhythm of the business").

**Approved metaphors (in specific contexts only):**

- "In the seat" (operator credential context).
- "In the room" (decision context).
- "On the hook" (accountability context).
- "Under diligence" (stakes context).

## Category 12. Overwrought openings and closings

**Rule:** The Dossier opens with the finding, not with a preamble. Reject preambles.

**Reject openings:**

- "In today's rapidly evolving landscape..."
- "As we navigate the complexity of..."
- "The world of AI is changing at an unprecedented pace..."
- "Every organization faces the challenge of..."
- "It is often said that..."
- "There has never been a more important time to..."

**Reject closings:**

- "Together, we can..."
- "The future is bright."
- "We look forward to hearing from you."
- "Please do not hesitate to reach out."
- "Thank you for your time."

**Approved openings:**

- Start with the specific finding, decision, or claim.
- Start with the eyebrow and title, no preamble.

**Approved closings:**

- Signature block.
- "Coordinated, not improvised." where appropriate.
- No thank-you, no "we look forward", no invitation to reach back.

## Category 13. Bulleted-list overuse

**Rule:** Bullets are a legitimate structure for parallel items. They are a slop signal when overused, when they replace prose that would carry more weight, or when items lack parallel structure.

**Reject bullet lists that:**

- Contain fewer than three items.
- Have items of wildly different lengths (a two-word bullet next to a full-paragraph bullet).
- Start every item with a different part of speech.
- Are followed immediately by another bullet list on the same topic.
- Restate what a paragraph above already said.

**Approved bullet usage:**

- Parallel items, similar length, same part of speech at the start.
- Three or more items.
- Not adjacent to another bullet list on the same topic.
- Introduced by prose that specifies what the list contains.

## Category 14. Heading and section-title slop

**Rule:** Headings should name the content, not preview or promote it.

**Reject headings:**

- "Why this matters."
- "The bottom line."
- "Key takeaways."
- "In summary."
- "The path forward."
- "Our approach."
- "Introduction."
- "Overview."
- "Executive summary." (unless the document has a specific executive summary structure required by the client).

**Approved headings:**

- Name the section content directly. "Findings." "Recommendations." "Decision register." "Refuse list." "Close."
- Use the eyebrow + title pattern from the Dossier: "SECTION 01" as eyebrow, "Findings." as title.

## Rendering a fail

When a category hit is found:

1. Quote the exact offending text.
2. Name the category and rule.
3. Propose a specific replacement using the approved pattern.
4. Do not proceed with the artifact until fixed.

## When in doubt

If a construction feels clever, it probably is (in the derogatory sense). If a sentence would survive being cut without losing information, cut it. If a claim requires an adverb to feel true, the claim is weak. The best C9D Consulting copy reads like an operating memo: dense, specific, defensible, quiet.

## Related files

**Inlined in this skill:**

- `snapshot.md`: voice principles Section E (evidence-first, plain-named-precision, concede-first, diagnose don't moralize) with pass and fail examples; tagline system in Section D invariant 6; frame evolution in Section F.
- `SKILL.md`: 60-second check and skill entry point.
- `audit-checklist.md`: full audit workflow that calls into these patterns as Section 08.
- `audit-report.md`: standardized report template. Category hits from this file typically resolve to advisories unless they violate Category 01 (em-dashes), which is a blocker.

**Referenced in main c9d-consulting-brand package:**

- Full voice library (Tier A vocabulary, refused vocabulary, tone flex matrix, boilerplate categories): `c9d-consulting-brand/references/voice-library.md`.
- Full 21-invariant list: `c9d-consulting-brand/SKILL.md` at root.
