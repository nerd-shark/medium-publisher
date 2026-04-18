---
title: "The Design Review Playbook: Facilitating Technical Discussions That Actually Work"
subtitle: "Good design reviews aren't about finding flaws—they're about collaborative problem-solving. Here's how to facilitate decisions, not just debates."
series: "Communication Part 5"
reading-time: "10-12 minutes"
target-audience: "Senior engineers, tech leads, engineering managers"
keywords: "design review, facilitation, technical discussions, decision-making, engineering leadership"
status: "v2-draft"
created: "2026-03-13"
author: "Daniel Stauffer"
---

# The Design Review Playbook: Facilitating Technical Discussions That Actually Work

Part 5 of my series on Technical Communication. Last time: surviving architecture reviews by preparing your thinking, not just your slides. This time: running design reviews when YOU'RE the facilitator, not the presenter.

## The Design Review That Went Sideways

It's 2:15 PM. You're 15 minutes into a 2-hour design review for a microservices migration. The junior engineer presenting the design has just finished explaining the proposed service boundaries.

Then it starts.

"Why are we using MongoDB?" asks the Senior Backend Engineer. "PostgreSQL would be way better for this."

"MongoDB gives us flexibility," responds the Principal Engineer. "We don't know the schema yet."

"That's exactly the problem," counters the Backend Engineer. "No schema means no data integrity. I've seen this before—it always ends badly."

"You're being dogmatic," says the Principal. "MongoDB is perfectly fine for this use case."

30 minutes later, they're still arguing. The other four attendees are checking Slack. The junior engineer who's supposed to be presenting is just sitting there, watching two senior engineers fight about databases.

Nobody is facilitating. Everyone is advocating.

The meeting ends at 4:00 PM with "let's schedule a follow-up to continue the discussion." No decisions made. No progress. Just two hours of everyone's time burned.

This is what happens when design reviews have no facilitator.

## The Facilitator vs Presenter Distinction

Here's the shift that changes everything: when you're running a design review, you're not presenting. You're facilitating.

**Presenter mindset**:
- Defend your design
- Answer questions
- Convince others your approach is right
- Focus on your solution

**Facilitator mindset**:
- Guide the discussion
- Draw out concerns
- Help the group reach a decision
- Focus on the process, not the outcome

Part 4 of this series was about being the presenter—defending your architecture in a review. Part 5 is about being the facilitator—helping others reach decisions.

The difference matters. A presenter advocates. A facilitator guides.

When you're presenting, you're attached to the outcome. When you're facilitating, you're attached to the process. You want a good decision, not necessarily YOUR decision.

[Need to expand: what happens when you're both presenter AND facilitator - that's the hardest scenario]


## Why Design Reviews Fail

Before we talk about how to facilitate well, let's understand why design reviews fail. There are five patterns I see repeatedly.

### Pattern 1: Bikeshedding (Parkinson's Law of Triviality)

The team spends 5 minutes on the critical database architecture decision. Then they spend 45 minutes arguing about whether to use `userId` or `user_id` in the API.

Why? Because variable naming is easy to have opinions about. Database architecture requires expertise that not everyone has.

This is Parkinson's Law of Triviality: people focus on what they understand, not what matters.

Real example: I watched a design review where the team spent the entire 90 minutes debating REST vs GraphQL for a public API. Meanwhile, nobody questioned the decision to use a single PostgreSQL database for 10 microservices. That decision caused production incidents six months later. The API choice? Didn't matter.

[The problem: People focus on what they understand, not what's important]

### Pattern 2: The Loudest Voice Wins

A Principal Engineer dominates the discussion. Junior engineers stay quiet even when they have valid concerns. The decision gets made based on seniority, not merit.

Real example: Principal engineer pushed for event sourcing because "it's the right architectural pattern." Nobody challenged it because he's the principal. Six months later, the team was drowning in debugging complexity, replaying events to figure out what went wrong. Everyone regretted it, but nobody had spoken up.

[The problem: Hierarchy kills honest feedback]

### Pattern 3: Analysis Paralysis

Every decision requires "more research." The team needs to "evaluate 5 more options before deciding." They need to "prototype all approaches." The meeting ends with action items, no decisions.

Real example: Team spent 3 months evaluating message queues—Kafka, RabbitMQ, SQS, Kinesis, Pulsar. By the time they decided on Kafka, the requirements had changed and they needed a different solution entirely.

[The problem: Fear of making the wrong decision prevents making any decision]

### Pattern 4: Design by Committee

Everyone has input. The design becomes a Frankenstein of compromises. Nobody is happy with the result.

Real example: API design that tried to satisfy 5 different teams. One team wanted REST, another wanted GraphQL, another wanted gRPC. The result? A REST API with GraphQL-style nested queries and gRPC-style error codes. Inconsistent, confusing, nobody liked it.

[The problem: Too many cooks, no clear decision-maker]

### Pattern 5: The Missing Context

A reviewer suggests an approach that was already tried and failed. Or suggests an approach that doesn't fit constraints. Or questions decisions that were already made by leadership.

Real example: Architect suggested multi-region deployment for better availability. Didn't know the budget had been cut and multi-region was off the table. Spent 20 minutes discussing something that wasn't even an option.

[The problem: Reviewers don't have the full context]

## The Facilitator's Job

Your job as facilitator isn't to make the decision. It's to help the group make a good decision.

Specifically:

1. **Set the stage**: Clear objectives, ground rules, decision-making process
2. **Guide the discussion**: Keep it focused, prevent tangents, manage time
3. **Draw out concerns**: Get quiet people to speak, surface hidden objections
4. **Manage conflict**: Facilitate debates, prevent personal attacks, find common ground
5. **Drive to decisions**: Recognize when enough discussion has happened, call for decision
6. **Document outcomes**: Capture decisions, rationale, action items, open questions

What you're NOT doing:
- Advocating for a specific approach (unless you're also the presenter)
- Making the decision yourself (unless you're the decision-maker)
- Letting the meeting run itself

[Need to expand each of these with specific techniques]

## Pre-Review Preparation

The best design reviews happen before you walk into the room.

### Distribute the Design Doc Early

Send the design doc at least 3 days before the review. Include:
- Problem statement (what are we solving?)
- Proposed solution (high-level approach)
- Alternatives considered (what else did we evaluate?)
- Open questions (what do we need to decide?)

Use a standard format: RFC (Request for Comments) or ADR (Architecture Decision Record).

If people show up without reading it, reschedule. Seriously. You can't have a productive discussion if people are reading the doc during the meeting.

[Real example: team that rescheduled when 4 of 6 people hadn't read the doc - saved everyone's time]

### Set Clear Objectives

Bad objective: "Review the microservices design"

Good objective: "Decide: Do we split the monolith into microservices? If yes, what's the service boundary strategy?"

The difference: Specific decision to make, not vague "review."

### Identify Required vs Optional Attendees

Required: People who need to approve or have critical context
Optional: People who want to stay informed

Why this matters: 10-person design review is a disaster. Keep it to 5-6 max.

[Need to add: how to handle people who want to attend but aren't required]

### Prepare Discussion Questions

What are the 3-5 key questions we need to answer?
What are the likely points of disagreement?
What context do reviewers need?

Example questions for microservices migration:
- "What's the service boundary strategy? By domain? By team? By data?"
- "How do we handle distributed transactions?"
- "What's the migration strategy from the monolith?"

[These questions guide the discussion and keep it focused]


## Creating Psychological Safety

People won't share honest feedback if they fear consequences. Your job as facilitator is to create an environment where dissent is safe.

### Separate Ideas from Identity

Bad: "Your design is wrong."
Good: "I'm concerned about the scalability of this approach."

The shift: Critique the idea, not the person.

### Encourage Dissent

Explicitly say: "I want to hear concerns and objections. That's why we're here."

Ask directly: "What are we missing? What could go wrong?"

Reward dissent: "That's a great point. I hadn't thought of that."

[When people see dissent rewarded, they're more likely to speak up]

### Handle Senior Engineers Who Dominate

The problem: Principal engineer speaks first, everyone else falls in line.

The solution: "Let's hear from everyone before we discuss. [Junior engineer], what's your take?"

Or: "I want to hear from people who haven't spoken yet."

Or: "Let's do a round-robin. Everyone shares one concern."

[The key: Explicitly create space for other voices]

### Draw Out Quiet Participants

The problem: Introverts stay quiet even when they have valuable input.

The solution: "I notice you're quiet. What's your take on this?"

Or: "You worked on the legacy system. What concerns do you have about migration?"

Or: Use written feedback (Slack, Google Doc comments) before the meeting.

[Some people think better in writing than in real-time discussion]

## Keeping Discussions Productive

### Recognize and Stop Bikeshedding

The signal: Discussion is going in circles, people are debating minor details.

The intervention: "This feels like bikeshedding. Let's table this and focus on the critical decisions."

Or: "We've spent 20 minutes on naming. Let's move to the database architecture decision."

The key: Name it explicitly, redirect to high-impact decisions.

[Bikeshedding is insidious - it feels productive but wastes time]

### Time-Box Discussions

The technique: "We have 15 minutes for this decision. Let's focus."

Why it works: Parkinson's Law—work expands to fill time. Constrain time, force focus.

Example agenda:
- 10 minutes: Present design
- 15 minutes: Discuss database choice
- 15 minutes: Discuss service boundaries
- 10 minutes: Discuss migration strategy
- 10 minutes: Make decisions and document

[Time-boxing prevents endless discussion]

### The Parking Lot Technique

The problem: Tangents derail the discussion.

The solution: "That's important, but it's out of scope for this review. Let's add it to the parking lot and address it separately."

Keep a visible parking lot: Whiteboard, shared doc, whatever works.

Follow up: Actually address parking lot items later, or people stop trusting the technique.

[The parking lot acknowledges concerns without derailing the meeting]

### Focus on High-Impact Decisions

The question: "What's the decision that's hardest to reverse?"

Prioritize: Irreversible decisions > reversible decisions

Example:
- Database choice: Hard to reverse (prioritize)
- API endpoint naming: Easy to reverse (deprioritize)
- Service boundaries: Hard to reverse (prioritize)
- Logging format: Easy to reverse (deprioritize)

[Focus energy where it matters most]

## Handling Disagreements Between Reviewers

This is the hard part. Two engineers disagree. Both have valid points. How do you facilitate?

### The Facilitator's Stance: Neutral

Your job: Help them reach a decision, not pick a side.

Even if you have an opinion: Set it aside while facilitating.

If you can't be neutral: Get someone else to facilitate.

[Neutrality is essential for trust]

### Facilitate Technical Debates

The structure:
1. "Let's hear both perspectives fully before discussing"
2. "Engineer A, explain your reasoning"
3. "Engineer B, explain your reasoning"
4. "What are the tradeoffs between these approaches?"
5. "What data would help us decide?"

The key: Make it about tradeoffs, not right vs wrong.

[Most technical decisions are tradeoffs, not absolutes]

### Find Common Ground

The question: "What do we agree on?"

Often: People agree on the problem, disagree on the solution.

Example:
- Agree: Need better scalability
- Disagree: Microservices vs optimized monolith
- Common ground: Need to handle 10x load within 6 months

The reframe: "We agree on the goal. Let's evaluate approaches against that goal."

[Common ground shifts from positions to interests]

### Escalation Criteria

Escalate when:
- Technical disagreement can't be resolved with data
- Decision requires business context the team doesn't have
- Decision has significant cost or risk implications
- Reviewers have equal authority and can't reach consensus

Don't escalate when:
- You just haven't tried hard enough to facilitate
- You're avoiding conflict
- You want someone else to make the hard call

How to escalate: "We've identified two viable approaches with different tradeoffs. We need leadership input on [specific question]."

[Escalation is a tool, not a cop-out]


## Decision-Making Frameworks

How do you actually decide? Here are three frameworks.

### Consensus vs Consent vs DACI

**Consensus**: Everyone agrees (rare, slow, often impossible)

**Consent**: No one has a blocking objection (more practical)

**DACI**: Driver, Approver, Contributors, Informed (clear roles)
- Driver: Runs the process, gathers input
- Approver: Makes the final decision
- Contributors: Provide input
- Informed: Kept in the loop

When to use each:
- Consensus: Small team, low-stakes decision, plenty of time
- Consent: Medium team, medium-stakes, need to move forward
- DACI: Large team, high-stakes, need clear accountability

[Most design reviews work best with consent]

### When to Decide vs When to Defer

Decide now when:
- You have enough information
- The decision is blocking other work
- Delaying has a cost
- The decision is reversible (can change later if wrong)

Defer when:
- Missing critical information
- Need to prototype or test assumptions
- Decision isn't blocking anything
- Emotions are high (let people cool down)

The key: Explicit decision to defer, with criteria for when to revisit.

[Deferring is a decision, not avoidance]

### The "Disagree and Commit" Principle

The scenario: Can't reach consensus, need to move forward.

The approach: "We've heard all perspectives. We're going with approach A. If you disagree, I need you to commit to making it work anyway."

Why it works: Acknowledges disagreement, but prevents sabotage.

When to use: After genuine attempt to reach consensus, when decision needs to be made.

[This is Amazon's principle - it works]

## Documenting Outcomes

The meeting doesn't end when people leave the room.

### What to Document

**Decisions made**:
- What was decided
- Why (the reasoning)
- Who made the decision
- When it was made

**Alternatives rejected**:
- What options were considered
- Why they were rejected
- What tradeoffs were made

**Open questions**:
- What's still unresolved
- What needs more research
- What assumptions need validation

**Action items**:
- What needs to happen next
- Who's responsible
- When it's due

[Documentation is how decisions survive beyond the meeting]

### The ADR Format (Architecture Decision Record)

Structure:
- Title: Short noun phrase
- Status: Proposed, Accepted, Deprecated, Superseded
- Context: What's the issue we're addressing?
- Decision: What are we doing?
- Consequences: What are the results (good and bad)?

Example:
```
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need a database for the payment platform. Requirements:
- ACID guarantees for financial transactions
- Complex queries for reporting
- Horizontal scalability for growth

## Decision
We will use PostgreSQL with read replicas for scaling.

## Consequences
**Positive**:
- ACID guarantees meet compliance requirements
- Rich query capabilities support reporting
- Team has PostgreSQL expertise

**Negative**:
- Requires operational expertise for scaling
- Vertical scaling limits (mitigated by read replicas)
- More complex than managed NoSQL options

## Alternatives Considered
- DynamoDB: Rejected due to lack of complex query support
- MongoDB: Rejected due to weaker consistency guarantees
```

[ADRs create a decision history that survives team turnover]

### Send Follow-Up Within 24 Hours

Subject: "Design Review Follow-Up: [Topic]"

Body:
- Decisions made
- Action items (owner, deadline)
- Open questions
- Next steps

Why 24 hours: Memory is fresh, momentum is maintained.

[The follow-up email is where decisions become real]

## When You're Both Presenter and Facilitator

This is the hardest scenario. You're presenting YOUR design AND running the review.

The challenge: Hard to be neutral when it's your design being critiqued.

The solution: Explicitly separate the roles.

How:
1. Present your design (presenter mode)
2. "Now I'm switching to facilitator mode. I want to hear all concerns and objections."
3. Facilitate the discussion (facilitator mode)
4. If you need to defend a decision, say: "Let me switch back to presenter mode for a moment..."

The key: Make the role switch explicit and visible.

Alternative: Get someone else to facilitate while you present.

[This is hard but learnable - practice the role switch]


## Real-World Example: The Microservices Migration Review

Let me show you how this works in practice.

**The Setup**:
- Team wants to split monolith into microservices
- 6 attendees: 2 senior engineers, 2 mid-level, 1 junior, 1 architect
- 90-minute review
- Design doc sent 3 days prior

**Pre-Review Prep**:
- Objective: Decide on service boundary strategy (by domain vs by team)
- Key questions: How do we handle distributed transactions? What's migration strategy?
- Identified likely disagreement: Senior Engineer A prefers domain boundaries, Senior Engineer B prefers team boundaries

**The Review**:

**0-10 min: Set the stage**

Facilitator: "Our objective today: Decide on service boundary strategy. We have 90 minutes. Ground rules: Critique ideas, not people. Everyone's input matters. We'll use consent for decision-making—no blocking objections. Questions before we start?"

[Setting expectations upfront prevents confusion later]

**10-25 min: Present design**

Junior engineer presents proposed domain-based boundaries. Shows service map, data flow, migration strategy.

[Presentation is clear and focused]

**25-40 min: Discuss service boundaries**

Senior Engineer A: "Domain boundaries are cleaner architecturally. Each service owns a complete business capability."

Senior Engineer B: "Team boundaries are more practical. We have three teams, we should have three services. Otherwise we'll have coordination overhead."

Facilitator: "Let's hear both perspectives fully. Engineer A, explain your reasoning."

[Engineer A explains domain-driven design principles, bounded contexts, etc.]

Facilitator: "Engineer B, explain your reasoning."

[Engineer B explains Conway's Law, team autonomy, communication overhead]

Facilitator: "What are the tradeoffs?"

Mid-level engineer: "Domain boundaries are theoretically better, but team boundaries match our org structure."

Facilitator: "What data would help us decide?"

Mid-level engineer: "We should look at our team structure and roadmap. Are teams stable? Are they aligned with domains?"

[Review team structure - teams are stable, roughly aligned with domains but not perfectly]

Facilitator: "Based on this, it seems team boundaries are more practical for our current org structure. We can refactor to domain boundaries later if teams reorganize. Any blocking objections?"

[Silence]

Facilitator: "Hearing none. Decision: Team-based service boundaries."

[Document decision in shared doc]

**40-55 min: Discuss distributed transactions**

Junior engineer (who's been quiet): "How do we handle transactions that span multiple services?"

Facilitator: "Great question. What are our options?"

[Discussion of saga pattern, 2PC, eventual consistency]

Senior Engineer A: "We should use the saga pattern. It's the standard approach for distributed transactions."

Facilitator: "Any concerns with saga pattern?"

Mid-level engineer: "It's complex to implement. We'll need to handle compensation logic for every transaction."

Facilitator: "What's the alternative?"

Senior Engineer B: "We could avoid distributed transactions entirely by keeping related data in the same service."

Facilitator: "Does that work with our service boundaries?"

[Discussion reveals some transactions will span services no matter how boundaries are drawn]

Facilitator: "Sounds like saga pattern is the right approach despite the complexity. Any blocking objections?"

[No objections]

Facilitator: "Decision: Saga pattern for distributed transactions. Action item: [Mid-level engineer] research saga pattern libraries and present options next week."

**55-70 min: Discuss migration strategy**

[Discussion of phased migration]

Architect: "We need to run both systems in parallel during migration. Otherwise we risk data loss."

Facilitator: "What's the risk?"

Senior Engineer A: "If we cut over all at once and something breaks, we can't roll back without losing data."

Facilitator: "How do we mitigate?"

Mid-level engineer: "We could do a phased migration. Migrate one service at a time. Run both systems in parallel for each phase."

Facilitator: "What about data consistency during parallel run?"

Senior Engineer B: "We'd need daily reconciliation. Compare data between old and new systems, flag discrepancies."

Facilitator: "That sounds like a solid mitigation. Any blocking objections to phased migration with parallel run and daily reconciliation?"

[No objections]

Facilitator: "Decision: Phased migration with parallel run and daily reconciliation."

**70-85 min: Open questions and parking lot**

Facilitator: "What questions are still open?"

[List open questions: monitoring strategy, testing approach, rollback procedure]

Facilitator: "What's in the parking lot?"

[List parking lot items: API versioning strategy, service mesh evaluation]

Facilitator: "For open questions, who's taking what?"

[Assign owners and deadlines for each open question]

**85-90 min: Document and wrap**

Facilitator: "Let me summarize decisions..."

[Read back three decisions: service boundaries, distributed transactions, migration strategy]

Facilitator: "Action items..."

[Read back action items with owners and deadlines]

Facilitator: "I'll send follow-up within 24 hours with ADRs for each decision. Thanks everyone."

**The Follow-Up**:

Sent within 24 hours:
- 3 ADRs documented (service boundaries, distributed transactions, migration strategy)
- Action items with owners and deadlines
- Open questions listed with owners
- Parking lot items scheduled for separate discussion

**Why it worked**:
- Clear objective and time-boxing kept discussion focused
- Psychological safety (everyone contributed, including junior engineer)
- Facilitated disagreement productively (heard both perspectives, evaluated tradeoffs)
- Made decisions with consent (no blocking objections)
- Documented outcomes immediately (ADRs within 24 hours)

[This is what good facilitation looks like]

## The Design Review Checklist

**Before the Review**:
- ☐ Design doc sent 3+ days in advance
- ☐ Clear objective and decision to make
- ☐ Required attendees identified (5-6 max)
- ☐ Discussion questions prepared
- ☐ Time-boxed agenda created

**During the Review**:
- ☐ Set the stage (objective, ground rules, decision-making process)
- ☐ Present design clearly
- ☐ Facilitate discussion (not advocate)
- ☐ Draw out quiet participants
- ☐ Manage time and prevent tangents
- ☐ Facilitate disagreements productively
- ☐ Drive to decisions
- ☐ Document outcomes

**After the Review**:
- ☐ Send follow-up within 24 hours
- ☐ Document decisions in ADRs
- ☐ Assign action items with owners and deadlines
- ☐ Schedule follow-up for open questions
- ☐ Address parking lot items

## Key Takeaways

- Facilitating is different from presenting—you're guiding the process, not advocating for an outcome
- Design reviews fail due to bikeshedding, loud voices, analysis paralysis, design by committee, and missing context
- Your job: set the stage, guide discussion, draw out concerns, manage conflict, drive to decisions, document outcomes
- Create psychological safety by separating ideas from identity and encouraging dissent
- Keep discussions productive with time-boxing, parking lot technique, and focus on high-impact decisions
- Handle disagreements by staying neutral, facilitating debates, and finding common ground
- Use decision frameworks: consensus vs consent vs DACI
- Document outcomes in ADRs with decisions, rationale, and alternatives rejected
- When you're both presenter and facilitator, explicitly separate the roles

## What's Next

In Part 6, we'll explore **Writing Technical Documents That Non-Technical People Actually Read**.

We'll cover:
- The one-page executive summary
- RFC structure and templates
- Architecture Decision Records (ADRs)
- Writing for different audiences
- Visual communication that clarifies

---

Target: ~2,500 words (v2 rough draft with mix of prose and bullets)
