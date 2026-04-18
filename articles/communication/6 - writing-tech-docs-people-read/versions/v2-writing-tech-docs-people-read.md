# Writing Technical Documents That Non-Technical People Actually Read

Part 6 of my series on Technical Communication. Last time, we explored [facilitating design reviews that actually produce decisions](link). This time: the written word — and why your beautifully detailed RFC is sitting unread in someone's inbox.

## The RFC Nobody Read

You spent three weeks writing a 47-page RFC. Architecture diagrams. Sequence diagrams. Risk analysis with probability matrices. Cost projections broken down by quarter. Appendices with code samples. It was thorough, technically precise, and comprehensive.

Two people read it. One skimmed the conclusion. The other read the title and asked "can you just summarize this in Slack?"

The project got approved anyway — based on a 5-minute hallway conversation with the VP of Engineering.

Your RFC was technically perfect and practically useless. And this happens constantly. Not because executives don't care about technical depth, but because you wrote a document for engineers and sent it to people who aren't engineers.

[Need a stat here — something like "average executive spends 28 seconds on a document before deciding whether to read it" — need to verify this]

## The Three-Audience Problem

Here's the thing nobody tells you about technical documents: they have three audiences with completely different reading patterns.

**Executives** read the title, first paragraph, and conclusion. Maybe a diagram if it's simple. They're looking for: What's the problem? What's the solution? What does it cost? What's the risk? They have 47 other documents competing for their attention.

**Product managers** read the impact section, timeline, and dependencies. They skip implementation details entirely. They're looking for: How does this affect the roadmap? What are the dependencies? When will it be done?

**Engineers** read everything. They want more detail. They're looking for: How does this work? What are the tradeoffs? What alternatives were considered? Show me the code.

One document. Three audiences. Three completely different reading patterns. Most technical documents fail because they're written for one audience (engineers) and read by three.

The solution isn't three separate documents. It's one document with layers.

## The One-Page Executive Summary

This is the most important page you'll ever write. If your executive reads only one page of your entire document, this is it.

**Structure**: Problem → Solution → Impact → Ask

300 words maximum. Not a suggestion — a hard limit. If you can't explain it in 300 words, you don't understand it well enough.

**Rules**:
- No jargon. No acronyms without expansion.
- No "we need to refactor the service mesh to reduce coupling between bounded contexts"
- Instead: "Our checkout system fails 3% of the time during peak traffic, costing $2.1M annually. We propose upgrading the payment processing pipeline, which reduces failures to 0.1% and pays for itself in 4 months."
- Every sentence must pass the "So What?" test from Part 1
- Lead with the business impact, not the technical approach

**Bad executive summary**:
"We propose migrating from a monolithic architecture to microservices using Kubernetes orchestration with Istio service mesh, implementing event-driven communication via Apache Kafka, and adopting a CQRS pattern for read/write separation."

[The executive reading this: "I have no idea what any of that means or why I should care."]

**Good executive summary**:
"Our platform can't handle Black Friday traffic — last year we lost $3.2M in 4 hours of downtime. We propose splitting the system into independent components that fail independently, so a problem in recommendations doesn't take down checkout. Cost: $400K over 6 months. Expected result: 99.99% uptime during peak traffic. ROI: positive within one Black Friday."

Same project. Same technical approach. Completely different framing.

## RFC Structure That Gets Read

The standard RFC structure most companies use is backwards. It starts with background, moves through technical details, and buries the recommendation on page 15. By page 3, your executive has stopped reading.

**Structure that works**:

1. **Executive Summary** (1 page) — Problem, solution, impact, ask
2. **Problem Statement** (1 page) — What's broken, who's affected, what it costs
3. **Proposed Solution** (2-3 pages) — High-level approach, not implementation
4. **Alternatives Considered** (1-2 pages) — Shows you did your homework
5. **Tradeoffs** (1 page) — Honest about what you're giving up
6. **Implementation Plan** (1-2 pages) — Phases, timeline, milestones
7. **Risks and Mitigation** (1 page) — What could go wrong and how you'll handle it
8. **Open Questions** (half page) — What you don't know yet
9. **Appendix: Technical Details** (unlimited) — Architecture, code, data models

The key insight: front-load the business value, back-load the technical details. Executives read top-down and stop when they've decided. Engineers skip to the appendix. Product managers read sections 1-6 and stop.

**The open questions section is underrated.** Including what you don't know builds trust. It shows intellectual honesty and invites collaboration. "We haven't determined the optimal database replication strategy yet — we'd like input from the DBA team" is better than pretending you have all the answers.

## Architecture Decision Records (ADRs)

ADRs are the most underused documentation tool in software engineering. They're short, focused records of individual technical decisions — one decision per record.

**Format**:
- **Title**: Short, descriptive (e.g., "Use PostgreSQL for user data")
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Context**: What's the situation? What are the constraints?
- **Decision**: What did we decide?
- **Consequences**: What happens because of this decision? (good and bad)

**Example**:
```
# ADR-007: Use Event-Driven Architecture for Order Processing

## Status: Accepted

## Context
Order processing currently uses synchronous REST calls between 6 services.
During peak traffic, a slow inventory check blocks the entire order flow.
Average order processing time: 4.2 seconds. Target: under 500ms.

## Decision
Adopt event-driven architecture using message queues for order processing.
Orders are published as events. Each service subscribes to relevant events
and processes independently.

## Consequences
- Good: Services process independently, no blocking
- Good: Natural retry mechanism via message redelivery
- Good: Easy to add new processing steps without changing existing services
- Bad: Eventual consistency (order status may lag by 1-2 seconds)
- Bad: Debugging distributed events is harder than tracing REST calls
- Bad: Requires message broker infrastructure (additional operational cost)
```

ADRs are for future you — the person who asks "why did we do it this way?" six months from now. Keep them short. If it's more than one page, it's not an ADR, it's an RFC.

Link ADRs together to form a decision history. ADR-007 might reference ADR-003 (which chose the message broker) and be superseded by ADR-012 (which switched to a different event schema).

## The Layered Document Approach

Think of your document like a newspaper article: headline, lead paragraph, full story, background.

**Layer 1: Executive Summary** (1 page)
- Business value, cost, timeline, ask
- Self-contained — reader can stop here and have the full picture
- Written last, placed first

**Layer 2: Technical Overview** (3-5 pages)
- Architecture approach, key decisions, tradeoffs
- Enough detail for a technical product manager or engineering director
- Self-contained — reader can stop here and understand the approach

**Layer 3: Implementation Details** (appendix, unlimited)
- Code examples, data models, API contracts, deployment plans
- For engineers who will build it
- Reference material, not narrative

Each layer is self-contained. A reader can stop at any layer and have a complete, coherent picture of the proposal. The executive stops at Layer 1. The product manager stops at Layer 2. The engineer reads Layer 3.

[Maybe add a visual here showing the three layers as a pyramid or nested boxes]

## Visual Communication That Clarifies

A good diagram replaces 1,000 words of explanation. A bad diagram adds 1,000 words of confusion.

**Architecture diagrams**: Show components and connections. Not implementation details. If your architecture diagram has database table schemas on it, you've gone too deep.

**Data flow diagrams**: Show how data moves through the system. Great for explaining to non-technical audiences because they can follow the flow.

**Sequence diagrams**: Show interactions between components over time. Best for explaining complex workflows to technical audiences.

**Decision trees**: Show branching logic. Great for explaining complex business rules or escalation paths.

**The #1 mistake**: Too much detail. If your diagram needs a legend with 20 symbols, simplify it. If you need to zoom in to read the labels, simplify it. If someone asks "what does this arrow mean?", simplify it.

**Color rules**:
- Red = problem, risk, or current state (broken)
- Green = solution, benefit, or proposed state (fixed)
- Gray = existing infrastructure (unchanged)
- Blue = new components (what you're building)
- Use color intentionally, not decoratively

## The Inverted Pyramid

Journalism's most powerful technique, and it works perfectly for technical writing.

**Paragraph 1**: The conclusion — what you want the reader to know or do
**Paragraph 2**: The evidence — why this is the right answer
**Paragraph 3**: The context — background for those who need it

Most people read the first paragraph of each section and move on. Make sure that first paragraph carries the weight.

**Bad** (bottom-up):
"We evaluated PostgreSQL, MySQL, MongoDB, DynamoDB, and CockroachDB across 14 criteria including ACID compliance, horizontal scalability, operational complexity, cost, team expertise, and ecosystem maturity. After extensive benchmarking over 3 weeks using production-like workloads... [3 paragraphs later] ...we recommend PostgreSQL."

**Good** (inverted pyramid):
"We recommend PostgreSQL for the user data store. It meets all requirements, the team has deep expertise, and it's 40% cheaper than the alternatives. We evaluated 5 databases across 14 criteria — PostgreSQL scored highest in 11 of them. Full analysis in Appendix B."

Same information. The reader gets the answer in the first sentence instead of the last paragraph.

## Pre-Alignment: Don't Surprise Stakeholders

The biggest mistake engineers make with technical documents isn't the writing — it's the process.

Don't spend 3 weeks writing a 47-page RFC and then surprise stakeholders with it. By the time they see it, you're emotionally invested in your solution. Any feedback feels like criticism. Any alternative feels like rejection.

Instead:
- Share a one-page problem statement first. "Here's what's broken. Does this match your understanding?"
- Share your proposed approach informally. "I'm thinking about X. Any concerns before I write it up?"
- Share a draft with key stakeholders. "I'd love your input before I formalize this."
- The formal submission should be a formality, not a surprise.

"I'd love your input on this before I formalize it" is the most powerful sentence in technical communication. It invites collaboration, builds buy-in, and surfaces objections early — when they're cheap to address.

## What to Do Monday Morning

Take your last RFC or technical proposal. Apply these three changes:

1. Add a one-page executive summary at the top. Problem, solution, impact, ask. 300 words max.
2. Move all implementation details to an appendix. The main body should be readable by a product manager.
3. Ask a non-technical colleague to read the first page. If they can't explain what you're proposing and why, rewrite it.

The best technical document isn't the most thorough one. It's the one that gets read, understood, and acted upon.

Your 47-page RFC might be technically perfect. But if nobody reads it, it doesn't matter.

---

Target: ~2,800 words at v4, 9 min read
