---
title: "Writing Technical Documents That Non-Technical People Actually Read"
subtitle: "You spent 3 weeks on a 47-page RFC. Two people read it. One skimmed the conclusion."
series: "Technical Communication Part 6"
reading-time: "9 minutes"
target-audience: "Engineers, architects, technical leads writing proposals and documentation"
keywords: "technical writing, RFC, ADR, executive summary, technical proposals, documentation, architecture decision records"
tags: "Technical Communication, Engineering Leadership, Documentation, RFC, ADR, Technical Writing"
status: "v3-draft"
created: "2026-03-29"
author: "Daniel Stauffer"
---

# Writing Technical Documents That Non-Technical People Actually Read

Part 6 of my series on Technical Communication. Last time, we explored [facilitating design reviews that actually produce decisions](link) — how to run productive technical discussions as a facilitator, not just a presenter. This time: the written word, and why your beautifully detailed RFC is sitting unread in someone's inbox. Follow along for more deep dives into communicating technical work effectively.

## The RFC Nobody Read

You spent three weeks writing a 47-page RFC. Architecture diagrams with proper UML notation. Sequence diagrams showing every interaction. Risk analysis with probability matrices. Cost projections broken down by quarter. Appendices with code samples and data models. It was thorough, technically precise, and comprehensive.

Two people read it. One skimmed the conclusion. The other read the title and asked "can you just summarize this in Slack?"

The project got approved anyway — based on a 5-minute hallway conversation with the VP of Engineering.

Your RFC was technically perfect and practically useless. And this happens constantly. A 2023 study by Atlassian found that knowledge workers spend an average of 25 minutes per day searching for information buried in documents that weren't written for them. Not because executives don't care about technical depth — they do. But because you wrote a document for engineers and sent it to people who aren't engineers.

The problem isn't your technical depth. It's your document structure.

## The Three-Audience Problem

Here's the thing nobody tells you about technical documents: they have three audiences with completely different reading patterns.

Executives read the title, first paragraph, and conclusion. Maybe a diagram if it's simple enough to understand in 10 seconds. They're looking for four things: What's the problem? What's the solution? What does it cost? What's the risk? They have 47 other documents competing for their attention, and yours has about 30 seconds to prove it's worth reading.

Product managers read the impact section, timeline, and dependencies. They skip implementation details entirely. They're looking for: How does this affect the roadmap? What are the dependencies on other teams? When will it be done? What do I need to communicate to stakeholders?

Engineers read everything. They want more detail. They're looking for: How does this actually work? What are the tradeoffs? What alternatives were considered? Show me the code. They'll read your appendices and wish there were more.

One document. Three audiences. Three completely different reading patterns. Most technical documents fail because they're written for one audience — engineers — and read by three.

The solution isn't three separate documents. It's one document with layers.

## The One-Page Executive Summary

This is the most important page you'll ever write. If your executive reads only one page of your entire document, this is it. Everything else is supporting material.

The structure is simple: Problem, Solution, Impact, Ask. 300 words maximum. Not a suggestion — a hard limit. If you can't explain your proposal in 300 words, you don't understand it well enough yet.

No jargon. No acronyms without expansion. No "we need to refactor the service mesh to reduce coupling between bounded contexts." Your executive doesn't know what a service mesh is, and they shouldn't have to.

Instead: "Our checkout system fails 3% of the time during peak traffic, costing us an estimated $2.1M annually in lost sales. We propose upgrading the payment processing pipeline to handle 10x current load. Cost: $400K over 6 months. Expected result: failures drop to 0.1%. The investment pays for itself in 4 months."

Every sentence must pass the "So What?" test from Part 1 of this series. If a sentence doesn't directly answer "why should the reader care?", cut it.

Here's the difference in practice:

A bad executive summary reads like a technical abstract: "We propose migrating from a monolithic architecture to microservices using Kubernetes orchestration with Istio service mesh, implementing event-driven communication via Apache Kafka, and adopting a CQRS pattern for read/write separation." The executive reading this has no idea what any of that means or why they should care.

A good executive summary reads like a business case: "Our platform can't handle Black Friday traffic — last year we lost $3.2M in 4 hours of downtime. We propose splitting the system into independent components that fail independently, so a problem in recommendations doesn't take down checkout. Cost: $400K over 6 months. Expected result: 99.99% uptime during peak traffic. ROI: positive within one Black Friday."

Same project. Same technical approach. Completely different framing. The first one gets filed. The second one gets funded.

## RFC Structure That Gets Read

The standard RFC structure most companies use is backwards. It starts with background and motivation, moves through technical details and implementation specifics, and buries the recommendation on page 15. By page 3, your executive has stopped reading. By page 7, your product manager has stopped. Only the engineers make it to the end — and they would have read it regardless.

Here's a structure that respects how people actually read:

The executive summary comes first — one page covering problem, solution, impact, and ask. Then the problem statement — one page explaining what's broken, who's affected, and what it costs in business terms. Then the proposed solution — two to three pages covering the high-level approach, not implementation details. Then alternatives considered — one to two pages showing you did your homework and didn't just pick the first option. Then tradeoffs — one page being honest about what you're giving up. Then the implementation plan — one to two pages with phases, timeline, and milestones. Then risks and mitigation — one page covering what could go wrong and how you'll handle it. Then open questions — half a page listing what you don't know yet. Finally, the appendix with unlimited technical details — architecture diagrams, code examples, data models, API contracts.

The key insight: front-load the business value, back-load the technical details. Executives read top-down and stop when they've decided. Engineers skip to the appendix. Product managers read the first six sections and stop.

The open questions section is the most underrated part of any RFC. Including what you don't know builds trust. It shows intellectual honesty and invites collaboration rather than criticism. "We haven't determined the optimal database replication strategy yet — we'd like input from the DBA team" is infinitely better than pretending you have all the answers. Nobody believes you have all the answers anyway.

## Architecture Decision Records: Your Future Self Will Thank You

ADRs are the most underused documentation tool in software engineering. They're short, focused records of individual technical decisions — one decision per record, one page maximum.

The format is simple. A short descriptive title like "Use PostgreSQL for user data." A status — proposed, accepted, deprecated, or superseded. Context explaining the situation and constraints. The decision itself. And consequences — both good and bad.

Here's what a real ADR looks like:

```
# ADR-007: Use Event-Driven Architecture for Order Processing

## Status: Accepted (2026-02-15)

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
- Good: Easy to add new processing steps without modifying existing services
- Bad: Eventual consistency — order status may lag by 1-2 seconds
- Bad: Debugging distributed events is harder than tracing REST calls
- Bad: Requires message broker infrastructure (additional operational cost)
```

ADRs are for future you — the person who asks "why did we do it this way?" six months from now when the original context has been forgotten. They're also for new team members who join and wonder why the system looks the way it does.

Keep them short. If it's more than one page, it's not an ADR — it's an RFC. Link ADRs together to form a decision history. ADR-007 might reference ADR-003 (which chose the message broker) and later be superseded by ADR-012 (which switched to a different event schema). Over time, you build a navigable history of every significant technical decision and why it was made.

The teams I've seen adopt ADRs consistently report fewer "why did we do this?" conversations, faster onboarding for new engineers, and better decision quality because writing down consequences forces you to think through implications before committing.

## The Layered Document

Think of your document like a newspaper article: headline, lead paragraph, full story, background. Each layer is self-contained — a reader can stop at any layer and have a complete, coherent picture.

Layer 1 is the executive summary. One page. Business value, cost, timeline, ask. Written last, placed first. A reader who stops here knows what you're proposing, why it matters, and what you need from them.

Layer 2 is the technical overview. Three to five pages. Architecture approach, key decisions, tradeoffs, implementation phases. Enough detail for a technical product manager or engineering director. A reader who stops here understands the approach well enough to ask informed questions and make resource decisions.

Layer 3 is the implementation details. Appendix, unlimited length. Code examples, data models, API contracts, deployment plans, configuration details. For engineers who will actually build it. Reference material, not narrative.

Each layer serves a different audience at a different depth. The executive stops at Layer 1. The product manager stops at Layer 2. The engineer reads Layer 3. Nobody is forced to read content that isn't relevant to their role.

## Visual Communication That Clarifies

A good diagram replaces a thousand words of explanation. A bad diagram adds a thousand words of confusion. The difference is restraint.

Architecture diagrams should show components and connections — not implementation details. If your architecture diagram has database table schemas on it, you've gone too deep. Show boxes with clear labels and arrows with clear meanings. That's it.

Data flow diagrams show how data moves through the system. They're excellent for non-technical audiences because anyone can follow a flow from left to right. "User submits order → Order service validates → Payment service charges → Inventory service reserves → Confirmation sent." Clear, linear, no technical knowledge required.

Sequence diagrams show interactions between components over time. They're best for technical audiences explaining complex workflows — request flows, error handling paths, retry logic.

The number one mistake in technical diagrams is too much detail. If your diagram needs a legend with 20 symbols, simplify it. If you need to zoom in to read the labels, simplify it. If someone asks "what does this arrow mean?", simplify it.

Use color intentionally, not decoratively. Red for problems or risks. Green for solutions or benefits. Gray for existing infrastructure that isn't changing. Blue for new components you're proposing. When a diagram uses color with purpose, the reader's eye is drawn to what matters.

## The Inverted Pyramid

Journalism's most powerful technique works perfectly for technical writing. Structure every section — every paragraph, really — with the most important information first.

Paragraph one: the conclusion. What you want the reader to know or do. Paragraph two: the evidence. Why this is the right answer. Paragraph three: the context. Background for those who need it.

Most people read the first paragraph of each section and move on. Make sure that first paragraph carries the weight.

Here's the difference. Bottom-up writing: "We evaluated PostgreSQL, MySQL, MongoDB, DynamoDB, and CockroachDB across 14 criteria including ACID compliance, horizontal scalability, operational complexity, cost, team expertise, and ecosystem maturity. After extensive benchmarking over 3 weeks using production-like workloads..." Three paragraphs later: "...we recommend PostgreSQL."

Inverted pyramid: "We recommend PostgreSQL for the user data store. It meets all requirements, the team has deep expertise, and it's 40% cheaper than the alternatives. We evaluated 5 databases across 14 criteria — PostgreSQL scored highest in 11 of them. Full analysis in Appendix B."

Same information. The reader gets the answer in the first sentence instead of the last paragraph. The people who want the full analysis can find it. The people who just need the recommendation have it immediately.

## Don't Surprise Stakeholders

The biggest mistake engineers make with technical documents isn't the writing — it's the process.

Don't spend three weeks writing a 47-page RFC and then surprise stakeholders with it. By the time they see it, you're emotionally invested in your solution. Any feedback feels like criticism. Any alternative feels like rejection. You've already decided, and the RFC is really just asking for permission.

Instead, pre-align incrementally. Share a one-page problem statement first: "Here's what's broken. Does this match your understanding?" Share your proposed approach informally: "I'm thinking about X. Any concerns before I write it up?" Share a draft with key stakeholders: "I'd love your input before I formalize this."

By the time you submit the formal RFC, everyone has already seen the direction, raised their concerns, and had their input incorporated. The formal submission becomes a formality — a record of a decision that's already been made collaboratively — not a surprise that triggers defensive reactions.

"I'd love your input on this before I formalize it" is the most powerful sentence in technical communication. It invites collaboration, builds buy-in, and surfaces objections early — when they're cheap to address instead of expensive to accommodate.

## What to Do Monday Morning

Take your last RFC or technical proposal. Apply three changes:

First, add a one-page executive summary at the top. Problem, solution, impact, ask. 300 words maximum. If your document doesn't have one, it's incomplete — no matter how thorough the technical content is.

Second, move all implementation details to an appendix. The main body should be readable by a product manager who doesn't know what Kubernetes is. If they can't follow the argument, restructure it.

Third, ask a non-technical colleague to read the first page. If they can't explain what you're proposing and why it matters, rewrite it. This is the single most effective test of document quality.

The best technical document isn't the most thorough one. It's the one that gets read, understood, and acted upon. Your 47-page RFC might be technically perfect. But if nobody reads it, it doesn't exist.

---

**Resources**:
- [Google's Engineering Practices: Design Documents](https://google.github.io/eng-practices/)
- [Documenting Architecture Decisions (Michael Nygard)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [The Pyramid Principle (Barbara Minto)](https://www.amazon.com/Pyramid-Principle-Logic-Writing-Thinking/dp/0273710516)
- [RFC 2119: Key Words for Use in RFCs](https://www.rfc-editor.org/rfc/rfc2119)

---

## Series Navigation

**Previous Article**: [The Design Review Playbook: Facilitating Technical Discussions That Actually Work](link) *(Part 5)*

**Next Article**: [Communicating Technical Debt to Non-Technical Stakeholders](link) *(Part 7 — Coming soon!)*

**Coming Up**: Making invisible work visible, building business cases for refactoring, and cross-functional collaboration

---

*This is Part 6 of the Technical Communication series. Read [Part 1: Speaking Executive](link) for C-suite communication fundamentals, [Part 2: Navigating Executive Disagreement](link) for stakeholder dynamics, [Part 3: The Technical Presentation Playbook](link) for audience adaptation, [Part 4: The Architecture Review Survival Guide](link) for defending technical decisions, and [Part 5: The Design Review Playbook](link) for facilitating productive reviews.*

**About the Author**: Daniel Stauffer is a software engineer and technical leader with 15+ years of experience writing technical proposals, RFCs, and architecture documents that actually get read and funded.

**Tags**: #TechnicalCommunication #EngineeringLeadership #Documentation #RFC #ADR #TechnicalWriting #SoftwareArchitecture #ExecutiveCommunication
