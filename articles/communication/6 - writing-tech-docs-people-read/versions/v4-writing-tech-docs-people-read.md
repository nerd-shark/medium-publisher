---
title: "Writing Technical Documents That Non-Technical People Actually Read"
subtitle: "You spent 3 weeks on a 47-page RFC. Two people read it. One skimmed the conclusion. Here's how to write docs that get funded, not filed."
series: "Technical Communication Part 6"
reading-time: "9 minutes"
target-audience: "Engineers, architects, technical leads writing proposals and documentation"
keywords: "technical writing, RFC, ADR, executive summary, technical proposals, documentation, architecture decision records"
tags: "Technical Communication, Engineering Leadership, Documentation, RFC, ADR, Technical Writing"
status: "v4-publishable"
created: "2026-03-29"
author: "Daniel Stauffer"
---

# Writing Technical Documents That Non-Technical People Actually Read

Part 6 of my series on Technical Communication. Last time, we explored [facilitating design reviews that actually produce decisions](link) — how to run productive technical discussions as a facilitator, not just a presenter. This time: the written word, and why your beautifully detailed RFC is sitting unread in someone's inbox. Follow along for more deep dives into communicating technical work effectively.

## The RFC Nobody Read

I once spent three weeks writing a 47-page RFC for a platform migration. UML diagrams. Sequence diagrams for every service interaction. A risk matrix with color-coded probability scores. Cost projections broken down by quarter with three scenarios. Appendices with code samples, data models, and a glossary. I was proud of it. Sent it to 12 people on a Monday morning.

By Wednesday, two people had opened it. One skimmed the conclusion. The other — my boss's boss — replied with: "Can you just give me the summary on Slack?"

The project got approved the following week. Not because of my RFC. Because I cornered the VP of Engineering near the coffee machine and explained it in five minutes.

That 47-page document was technically perfect and practically useless. And I've watched this happen to other engineers dozens of times since. The executives aren't the problem — they actually do care about technical depth when it's relevant to their decision. The problem is that we write documents for engineers and then send them to people who aren't engineers and wonder why nobody reads past page 2.

## The Three-Audience Problem

Nobody told me this when I started writing technical documents, and I wish someone had: your RFC has three audiences, and they read completely differently.

Executives skim. Title, first paragraph, conclusion. Maybe a diagram if it doesn't require squinting. They want four things — what's broken, what's the fix, what does it cost, what's the risk — and they want them in about 30 seconds. They've got a stack of other documents on their desk and yours needs to earn its spot.

Product managers cherry-pick. They jump to the impact section, the timeline, the dependencies. Implementation details? Skipped entirely. They're trying to figure out how this affects the roadmap and what they need to tell stakeholders next Thursday.

Engineers read everything. All of it. They want more. They'll read your appendices and email you asking for the raw benchmark data you didn't include.

So you've got one document being consumed three completely different ways. And most of us — because we're engineers — write the whole thing for that third audience. The executives and PMs never stood a chance.

You don't need three separate documents. You need one document that works in layers.

## The One-Page Executive Summary

If I could only teach one thing about technical writing, it would be this: write the executive summary first. Or rather, write it last, but put it first. Either way, it's the most important page in your document. If your VP reads nothing else, they'll read this.

Structure: Problem, Solution, Impact, Ask. Keep it under 300 words. That's not a guideline — treat it as a hard ceiling. If you can't explain your proposal in 300 words, you probably don't understand it well enough yet. I've been there. It's humbling.

Kill the jargon. All of it. No "refactoring the service mesh to reduce coupling between bounded contexts." Your CTO might know what that means. Your CFO doesn't, and she's the one approving the budget.

Try this instead: "Our checkout system fails 3% of the time during peak traffic, costing us roughly $2.1M a year in lost sales. We want to upgrade the payment processing pipeline to handle 10x current load. It'll cost about $400K over six months. Failures should drop to 0.1%. Pays for itself in four months."

Every sentence needs to survive the "So What?" test from [Part 1](link) of this series. If a sentence doesn't answer why the reader should care, delete it. Be ruthless.

I want to show you what this looks like in practice, because the gap is wild.

Bad executive summary — reads like a technical abstract: "We propose migrating from a monolithic architecture to microservices using Kubernetes orchestration with Istio service mesh, implementing event-driven communication via Apache Kafka, and adopting a CQRS pattern for read/write separation." I've read this sentence to three different executives. All three said some version of "I don't know what any of that means."

Good executive summary — reads like a business case: "Our platform can't handle Black Friday traffic — last year we lost $3.2M in 4 hours of downtime. We want to split the system into independent pieces so a problem in recommendations doesn't take down checkout. Cost: $400K over 6 months. Expected result: 99.99% uptime during peak traffic. ROI: positive within one Black Friday."

Same project. Same technical approach underneath. Completely different framing. One gets filed in a folder nobody opens. The other gets a budget line item.

## RFC Structure That Gets Read

Most RFC templates I've seen at companies are structured backwards. They start with background and motivation — two pages of context-setting before you even get to the proposal. Then technical details. Then implementation specifics. The actual recommendation? Buried on page 15.

By page 3, your executive has closed the tab. By page 7, your product manager has switched to Slack. The only people who make it to the end are the engineers, and honestly, they would've read it no matter how you structured it.

I've landed on a structure that works much better. It respects how people actually read — top-down, stopping when they've gotten what they need:

1. **Executive Summary** (1 page) — Problem, solution, impact, ask
2. **Problem Statement** (1 page) — What's broken, who it affects, what it costs
3. **Proposed Solution** (2-3 pages) — High-level approach, not implementation
4. **Alternatives Considered** (1-2 pages) — Shows you didn't just pick the first option
5. **Tradeoffs** (1 page) — What you're giving up, honestly
6. **Implementation Plan** (1-2 pages) — Phases, timeline, milestones
7. **Risks and Mitigation** (1 page) — What could go wrong
8. **Open Questions** (half page) — What you don't know yet
9. **Appendix: Technical Details** (unlimited) — Architecture, code, data models

Front-load the business value. Back-load the technical depth. Executives read from the top and stop when they've decided. Engineers jump straight to the appendix. PMs read sections 1 through 6 and call it done.

One thing I want to call out specifically: the open questions section. Most engineers leave this out because it feels like admitting weakness. It's actually the opposite. Saying "we haven't nailed down the replication strategy yet — we'd like the DBA team's input" builds trust. It signals intellectual honesty. It turns reviewers into collaborators instead of critics. Nobody believes you have all the answers anyway, and pretending you do just makes people look harder for holes.

## Architecture Decision Records: Your Future Self Will Thank You

I'm going to make a bold claim: ADRs are the single most underused documentation tool in our industry. They're short — one page max — and they capture one technical decision per record. That's it. Context, decision, consequences. Done.

The format is dead simple. A descriptive title ("Use PostgreSQL for user data"). A status — proposed, accepted, deprecated, or superseded. The context explaining what situation you were in. What you decided. And the consequences, good AND bad.

Here's one from a real project (details changed):

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

These are for future you. The version of you that's staring at the codebase six months from now, wondering "why on earth did we use event sourcing here?" They're also for the new engineer who joins the team and needs to understand not just what the system does, but why it was built that way.

If your ADR is longer than a page, it's not an ADR — it's an RFC. Keep them tight. Link them together so ADR-007 references ADR-003 (which chose the message broker) and eventually gets superseded by ADR-012 (which changed the event schema). Over time you end up with a navigable decision history that's worth its weight in gold.

Michael Nygard [designed the format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) to be lightweight on purpose. Heavy documentation doesn't get written. A one-page ADR that exists beats a ten-page design doc that lives in someone's "I'll finish it later" folder.

## The Layered Document

Think of it like a newspaper. Headline. Lead paragraph. Full story. Background. A reader can bail at any point and still walk away with something useful.

Layer 1 is the executive summary. One page. Business value, cost, timeline, the ask. You write this last but it goes first. Someone who reads only this page should know exactly what you're proposing, why it matters, and what you need from them.

Layer 2 is the technical overview. Three to five pages. Architecture approach, key decisions, tradeoffs, implementation phases. This is for your engineering director or technical PM — someone who needs enough depth to ask smart questions and allocate resources, but doesn't need to see your database schema.

Layer 3 is the implementation details. Appendix. No length limit. Code examples, data models, API contracts, deployment plans. This is for the engineers who'll actually build the thing. Reference material, not narrative.

The executive stops at Layer 1. The PM stops at Layer 2. The engineer reads Layer 3. Nobody has to wade through stuff that isn't for them.

The part that trips people up: each layer needs to stand on its own. Layer 1 can't say "see section 4.2 for the approach." It needs to summarize the approach in a sentence. Layer 2 can't assume you've read Layer 3. If someone reads only their layer, they should have a complete picture. That's harder to write than it sounds, but it's what makes the format work.

## Visual Communication That Clarifies

A good diagram saves you a thousand words of explanation. A bad one costs you a thousand words of confusion. The difference, almost always, is restraint.

Architecture diagrams should show components and connections. That's it. If your architecture diagram has database table schemas on it, you've gone way too deep. Boxes with clear labels. Arrows with clear meanings. Done.

Data flow diagrams are great for non-technical audiences because anyone can follow a flow from left to right. "User submits order → Order service validates → Payment charges → Inventory reserves → Confirmation sent." No technical knowledge required. I've used these in board presentations and they land every time.

Sequence diagrams are for technical audiences — request flows, error handling, retry logic. Don't put these in your executive summary. I've made that mistake. The CFO's eyes glazed over in about four seconds.

The mistake I see most often: too much detail. If your diagram needs a legend with 20 symbols, it's too complex. If you have to zoom in to read the labels, it's too dense. If someone in the room asks "what does this arrow mean?" — that's your signal to simplify.

Color helps, but only when it's intentional. Red for problems or risks. Green for solutions. Gray for existing stuff that isn't changing. Blue for new things you're proposing. When color has meaning, the reader's eye goes where it should without you having to explain it.

## The Inverted Pyramid

Borrowed from journalism, and it's the single best writing technique I've adopted for technical documents. Put the most important information first. Always.

First paragraph of any section: the conclusion. What you want the reader to know or do. Second paragraph: the evidence. Why you're right. Third paragraph: the context and background, for the people who want it.

Most readers only make it through the first paragraph of each section before moving on. So that first paragraph has to do the heavy lifting.

Watch the difference. Bottom-up writing (how most engineers write): "We evaluated PostgreSQL, MySQL, MongoDB, DynamoDB, and CockroachDB across 14 criteria including ACID compliance, horizontal scalability, operational complexity, cost, team expertise, and ecosystem maturity. After extensive benchmarking over 3 weeks using production-like workloads..." Three paragraphs later: "...we recommend PostgreSQL."

Inverted pyramid: "We recommend PostgreSQL for the user data store. It meets all our requirements, the team already knows it well, and it's 40% cheaper than the next best option. We evaluated 5 databases across 14 criteria — PostgreSQL scored highest in 11. Full analysis in Appendix B."

Same information. But the reader gets the answer in the first sentence instead of the last paragraph. The people who want the deep analysis know where to find it. Everyone else has what they need and can move on.

## Don't Surprise Stakeholders

The biggest mistake I've made with technical documents — and I've watched other engineers make it too — isn't about the writing. It's about the process.

I used to disappear for three weeks, write a massive RFC, and then drop it on stakeholders like a surprise exam. By the time they saw it, I was emotionally invested. I'd already decided. The RFC wasn't really asking for input — it was asking for permission. And that dynamic puts reviewers in a weird position where they can either rubber-stamp it or reject it. Neither is collaboration.

What works way better: pre-align incrementally. Share a one-page problem statement first. "Here's what I think is broken. Does this match what you're seeing?" Then share your proposed approach over coffee or Slack. "I'm leaning toward X. Any red flags before I write it up?" Then share a rough draft with the two or three people whose opinions matter most. "I'd love your input before I formalize this."

By the time you submit the formal RFC, everyone's already seen the direction. They've raised concerns. You've incorporated their feedback. The formal submission is a formality — a record of a decision that was made collaboratively over the past two weeks — not a surprise that triggers defensive reactions and political maneuvering.

"I'd love your input before I formalize this." That sentence has gotten me more projects approved than any amount of technical rigor. It invites collaboration, builds buy-in, and surfaces objections early — when they're cheap to address instead of expensive to accommodate.

## What to Do Monday Morning

Pull up your last RFC or technical proposal. Make three changes:

Add a one-page executive summary at the top. Problem, solution, impact, ask. 300 words. If your document doesn't have one, it's incomplete — doesn't matter how thorough the rest is.

Move all the implementation details to an appendix. The main body should make sense to a product manager who's never heard of Kubernetes. If they can't follow the argument, you've got restructuring to do.

Then — and this is the real test — ask a non-technical colleague to read that first page. Buy them a coffee. Ask them to explain back to you what you're proposing and why it matters. If they can't, rewrite it. Five minutes of their time will save you weeks of misalignment.

The best technical document isn't the most thorough one. It's the one that gets read, understood, and acted on. Your 47-page RFC might be technically flawless. But if nobody reads it, it might as well not exist.

---

**Resources**:
- [Documenting Architecture Decisions — Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Google Engineering Practices: Design Documents](https://google.github.io/eng-practices/)
- [The Pyramid Principle — Barbara Minto](https://www.amazon.com/Pyramid-Principle-Logic-Writing-Thinking/dp/0273710516)
- [RFC 2119: Key Words for Use in RFCs](https://www.rfc-editor.org/rfc/rfc2119)
- [Atlassian: How Teams Spend Their Time](https://www.atlassian.com/time-wasting-at-work)

---

## Series Navigation

**Previous Article**: [The Design Review Playbook: Facilitating Technical Discussions That Actually Work](link) *(Part 5)*

**Next Article**: [Communicating Technical Debt to Non-Technical Stakeholders](link) *(Part 7 — Coming soon!)*

**Coming Up**: Making invisible work visible, building business cases for refactoring, and cross-functional collaboration between engineering, product, and design

---

*This is Part 6 of the Technical Communication series. Read [Part 1: Speaking Executive](link) for C-suite communication fundamentals, [Part 2: Navigating Executive Disagreement](link) for stakeholder dynamics, [Part 3: The Technical Presentation Playbook](link) for audience adaptation, [Part 4: The Architecture Review Survival Guide](link) for defending technical decisions, and [Part 5: The Design Review Playbook](link) for facilitating productive reviews.*

**About the Author**: Daniel Stauffer is an Enterprise Architect with 15+ years of experience writing technical proposals, RFCs, and architecture documents across fintech, healthcare, and e-commerce. He has strong opinions about executive summaries.

**Tags**: #TechnicalCommunication #EngineeringLeadership #Documentation #RFC #ADR #TechnicalWriting #SoftwareArchitecture #ExecutiveCommunication
