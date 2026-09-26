# Outbound Spec

> **STATUS: PROPOSED, NOT LOCKED.**
> 
> This template specification is Claude's structured application of The Dossier system to this output format. It was NOT in the locked §9 Visual Identity Doc or §10 Product/Offering Doc source artifacts. The locked source documented the brand foundation, visual tokens, voice library, and engagement architecture — not format-specific templates.
> 
> Treat this file as a starting point for discussion with Brandon, not as locked system. Specific patterns flagged below as **[proposed]** are derivable from locked tokens and rules; structures flagged as **[invented]** were created for this file and have no source. Review and lock with Brandon before treating as system.


The Dossier system applied to outbound surfaces: email signatures, outbound emails (cold and warm), proposal copy, LinkedIn posts, and social-distribution moments. These are the surfaces where the brand's voice is exposed most directly to the reader; the discipline is highest here.

---

## Email signature

The locked email signature block. Inter Tight for the name and role; JetBrains Mono for engagement reference and domain.

**Plain-text version (for plain-text outbound and signature defaults):**

```
Brandon Wilburn
C9D Consulting — a practice of Brandon Wilburn
[E-01 / E-02 / E-03 / R-01 reference if applicable to the thread]
c9d.consulting
```

**HTML version (for rich email clients):**

```html
<table cellpadding="0" cellspacing="0" border="0" style="font-family: 'Inter Tight', sans-serif;">
  <tr>
    <td style="padding-bottom: 4px;">
      <span style="font-size: 14px; font-weight: 500; color: #1a1612;">Brandon Wilburn</span>
    </td>
  </tr>
  <tr>
    <td style="padding-bottom: 6px;">
      <span style="font-size: 13px; color: #2e2820;">
        <span style="color: #9c4f24; font-weight: 500;">C9D</span> Consulting
      </span>
      <span style="font-size: 13px; color: #5a5042;"> · a practice of Brandon Wilburn</span>
    </td>
  </tr>
  <tr>
    <td style="padding-bottom: 4px;">
      <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #5a5042; letter-spacing: 0.05em;">E-01 PRODUCTIZATION ENGAGEMENT</span>
    </td>
  </tr>
  <tr>
    <td>
      <a href="https://c9d.consulting" style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #9c4f24; text-decoration: none; border-bottom: 1px solid #6b3818; letter-spacing: 0.05em;">c9d.consulting</a>
    </td>
  </tr>
</table>
```

**Rules:**

- The signature never includes a phone number unless the engagement requires it.
- The signature never includes social links (the practice is not promoting itself on social channels).
- The signature never includes a marketing tagline below "Coordinated, not improvised" already lives in the wordmark territory; double-stamping is refused.
- The engagement reference line is optional — include it only when the thread is engagement-specific.

---

## Cold outbound (rare)

C9D Consulting does very little cold outbound. The brand is built for inbound from warm referral. When cold outbound is required, the format is constrained.

### When cold outbound is allowed

- A specific named individual is hitting one of the three trigger events (platform-rebuild wall, AI-adoption decision, diligence moment) and is a personal warm connection of Brandon Wilburn.
- A board member or investor has explicitly asked Brandon to reach out to a portfolio company.
- A referral with full context (the referrer's name, the trigger event, the introduction) lands in the inbox and a follow-up note is needed.

Generic prospecting outbound is refused.

### Cold outbound template

Subject line: one of the three trigger-event phrasings.

- "Re: the platform rebuild decision"
- "Re: the AI build / buy / defer decision"
- "Re: the diligence moment"

The subject line names the work, not the practice.

Body:

```
[First name],

[Referrer] mentioned you're working through [specific trigger event] at [company]. The work I do is fractional executive presence on exactly that decision — I've shipped what I'd recommend in a comparable system, and I run a structured engagement to surface the threads an acquirer's counterparts would pull.

If a 20-minute diagnostic call is useful, here's a calendar link: [link]. If it's not, no follow-up.

Brandon
```

The body is short. It names the referrer, names the engagement, names the deliverable (the diagnostic call), and offers a clean opt-out. No follow-up sequence runs automatically; the diagnostic-call request gets one reply and no chase.

### Refused outbound patterns

- "I hope this finds you well." (Refused on principle.)
- "I'll keep this brief." (Implies the rest will be long; just be brief.)
- "Just wanted to circle back." (Refused vocabulary.)
- Multi-paragraph case studies in the cold email.
- Calendly links without a stated purpose.
- "Quick question" subject lines.
- Sequenced follow-ups (no follow-up unless the recipient replies).
- "Hope to hear from you" closes.

---

## Warm outbound (the default)

The bulk of C9D Consulting outbound is warm: replies to inbound referrals, replies to introductions, follow-ups after a diagnostic call.

### Standard warm template (post-introduction)

When a referrer introduces Brandon to a prospect via email:

```
Subject: Re: [referrer's subject line]

[First name] — thank you for the introduction. [Referrer] mentioned [the specific context they shared].

I run a fractional executive practice for Series B-to-D companies navigating [the specific trigger event named in the introduction]. Four engagement types, fixed scope and fixed price, structured around the decision in front of you.

If it's useful, I'd suggest a 20-minute diagnostic call. The goal is to establish whether the engagement is a fit — not to sell anything in the call. Here's a calendar link: [link].

If the timing isn't right, no follow-up.

Brandon
```

### Standard warm template (post-diagnostic call, going to proposal)

```
Subject: Re: [original thread]

[First name] — thank you for the call yesterday.

Confirming the scope as we discussed: [E-01 / E-02 / E-03 / R-01] with [specific scope summary in 1-2 sentences].

I'll prepare the SOW and send it through this week. The baseline is $[amount]; the specific quote will reflect [the scope/risk/stakes drivers].

Brandon
```

### Standard warm template (post-diagnostic call, declining)

```
Subject: Re: [original thread]

[First name] — thank you for the call yesterday.

After review, this engagement is not a fit for C9D Consulting. The reason: [specific named reason — stage, vertical, scope, decision authority].

For [their specific need], I'd suggest looking at [adjacent category, no specific vendor]. If you'd like an intro to someone in that category I know personally, happy to make it.

Best of luck with the work.

Brandon
```

---

## Proposal cover email

When sending an SOW or proposal as an email attachment:

```
Subject: SOW: [Engagement type] for [Company]

[First name],

Attached is the SOW for [E-01 / E-02 / E-03 / R-01]. Key elements:

· Scope: [one-line summary]
· Timeline: [start–end dates]
· Pricing: $[amount], fixed scope, fixed price
· Lead operator: Brandon Wilburn

Sign and return when ready. If anything in the scope or pricing needs adjustment, let me know before signature — adjustments after signature trigger a written scope change.

Brandon
```

The cover email is short. The SOW carries the detail; the email summarizes.

---

## LinkedIn posts

C9D Consulting does very little on LinkedIn. The brand's discipline is to publish rarely and to publish operating evidence rather than thought leadership. When a LinkedIn post is published, the format is constrained.

### When a LinkedIn post is allowed

- An engagement has closed and the client has explicitly approved a public reference.
- A board observation or industry observation crosses a threshold where the practice's perspective is materially distinct.
- A new productized asset (P-XX) has shipped and is being made available.

LinkedIn-as-content-marketing is refused.

### Standard LinkedIn post structure

```
[Opening claim, one line, post-shipping posture.]

[Three paragraphs of evidence. Each paragraph is 2–4 sentences. The evidence is specific: named scenarios, named patterns, named outcomes. No general advice.]

[Closing line — usually a refusal or a specific call to readers who match the engagement criteria.]

— Brandon Wilburn
C9D Consulting · a practice of Brandon Wilburn
```

### Refused LinkedIn patterns

- "Here are 7 things I learned about [topic]."
- "I built a $X business by [thing]. Here's how."
- "Hot take: [contrarian-sounding take that isn't contrarian]."
- Posts with images of slide-deck screenshots.
- Posts that end with a CTA to "DM me to learn more."
- Posts that summarize someone else's content with the author's takes (this is borrowed-authority pattern).
- Posts using the word "thoughts" or "musings" anywhere in the body.
- Carousel posts.
- Polls.
- Posts longer than 250 words.

---

## Substack / newsletter (TechieBrandon — separate surface)

LinkedIn cross-posting from TechieBrandon is refused. TechieBrandon and C9D Consulting are deliberately separate surfaces; the boundary between publication and practice is enforced.

If a TechieBrandon article is relevant to a C9D Consulting prospect, the relevance is mentioned in a direct outbound message, not posted as a feed item.

---

## Referral / introduction language

When Brandon makes a referral to someone outside C9D Consulting's scope:

```
[First name] — meet [Referee]. [One-sentence context about the referee.]

[Referee] — meet [First name]. They're working through [the specific situation]. I think your [E-01-comparable / E-02-comparable / etc.] practice is the right fit — this falls outside C9D Consulting's scope on [the specific dimension that drove the referral out].

Leaving you both to it.

Brandon
```

The referral always names why C9D Consulting declined the work. Naming the decline reason makes the referral specific and useful, and protects the brand by reinforcing the engagement criteria.

---

## Calendar invite format

Calendar invites sent by C9D Consulting follow a specific format.

**Event title:** `Diagnostic call · C9D Consulting · [Company]`

**Event description:**

```
20-minute diagnostic call.

The goal of the call: establish whether C9D Consulting is a fit for the work [Company] is considering. The call is not a sales pitch.

Topics:
· The decision in front of [Company]
· The trigger event driving the decision
· Whether the engagement maps to E-01, E-02, E-03, R-01, or none of them

If the engagement is a fit, the next step is scope alignment (1–2 conversations) leading to a written SOW. If it is not a fit, the call ends as a referral.

Brandon Wilburn
C9D Consulting · a practice of Brandon Wilburn
c9d.consulting
```

The description explains what the call is and what it is not. The reader knows what to expect before joining.

---

## Out-of-office message

When Brandon is unavailable (engagement intensive period, holiday, deep work block):

```
I'm in deep work on a current engagement and am offline until [date]. Inbound to brandon@c9d.consulting will be reviewed on return.

For active client engagements: [client contact path or alternative].
For inbound diagnostic call requests: c9d.consulting/contact — I'll review after [date].

Brandon Wilburn
C9D Consulting · a practice of Brandon Wilburn
```

The out-of-office message does not promise faster turnaround than is honest. The brand's discipline is to set the actual expectation, not the optimistic one.
