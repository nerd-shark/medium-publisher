---
title: "The Design Review Playbook: Facilitating Technical Discussions That Actually Work"
subtitle: "TBD - something about facilitation vs presenting"
series: "Communication Part 5"
reading-time: "TBD"
target-audience: "Senior engineers, tech leads, engineering managers"
keywords: "design review, facilitation, technical discussions, decision-making, engineering leadership"
status: "v1-outline"
created: "2026-03-13"
author: "Daniel Stauffer"
---

# The Design Review Playbook: Facilitating Technical Discussions That Actually Work

Part 5 of my series on Technical Communication. Last time: surviving architecture reviews by preparing your thinking, not just your slides. This time: running design reviews when YOU'RE the facilitator, not the presenter.

## Opening Hook - The Design Review That Went Sideways

- 2-hour design review scheduled
- 15 minutes in, two senior engineers are arguing about database choices
- 30 minutes later, still arguing
- Other attendees checking Slack, clearly disengaged
- No decisions made, meeting ends with "let's schedule a follow-up"
- Real story: microservices design review that turned into MongoDB vs PostgreSQL holy war
- The presenter (junior engineer) just sat there watching senior engineers fight
- Nobody was facilitating, everyone was advocating
- This is what happens when you don't have a facilitator

**The Core Problem**: Design reviews fail when there's no facilitator, only advocates

## The Facilitator vs Presenter Distinction

**Key insight**: When you're running the review, you're not presenting. You're facilitating.

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

**The shift**: Part 4 was about being the presenter (defending your architecture). Part 5 is about being the facilitator (helping others reach decisions).

**When you're both**: Sometimes you're presenting YOUR design AND facilitating the review. That's the hardest scenario. We'll cover that too.

## Why Design Reviews Fail (The Common Patterns)

### Pattern 1: Bikeshedding (Parkinson's Law of Triviality)

- Spend 5 minutes on the critical database architecture decision
- Spend 45 minutes arguing about variable naming conventions
- Why? Variable names are easy to have opinions about, database architecture requires expertise
- Real example: Spent entire review arguing about whether to use "userId" or "user_id"
- Meanwhile, nobody questioned the decision to use a single database for 10 microservices

**The problem**: People focus on what they understand, not what matters

### Pattern 2: The Loudest Voice Wins

- Senior engineer dominates discussion
- Junior engineers stay quiet even when they have valid concerns
- Decision gets made based on seniority, not merit
- Real example: Principal engineer pushed for event sourcing because "it's the right way"
- Nobody challenged it because he's the principal
- Six months later: debugging nightmare, team regrets it

**The problem**: Hierarchy kills honest feedback

### Pattern 3: Analysis Paralysis

- Every decision requires "more research"
- "Let's evaluate 5 more options before deciding"
- "We need to prototype all approaches"
- Meeting ends with action items, no decisions
- Real example: Spent 3 months evaluating message queues (Kafka, RabbitMQ, SQS, Kinesis, Pulsar)
- By the time they decided, requirements had changed

**The problem**: Fear of making the wrong decision prevents making any decision

### Pattern 4: Design by Committee

- Everyone has input
- Design becomes a Frankenstein of compromises
- Nobody is happy with the result
- Real example: API design that tried to satisfy 5 different teams
- Result: Inconsistent, confusing, nobody liked it

**The problem**: Too many cooks, no clear decision-maker

### Pattern 5: The Missing Context

- Reviewer suggests approach that was already tried and failed
- Or suggests approach that doesn't fit constraints
- Or questions decisions that were already made by leadership
- Real example: Architect suggested multi-region deployment
- Didn't know budget was already cut, multi-region was off the table

**The problem**: Reviewers don't have the full context

## The Facilitator's Job (What You're Actually Doing)

**Your job as facilitator**:

1. **Set the stage**: Clear objectives, ground rules, decision-making process
2. **Guide the discussion**: Keep it focused, prevent tangents, manage time
3. **Draw out concerns**: Get quiet people to speak, surface hidden objections
4. **Manage conflict**: Facilitate debates, prevent personal attacks, find common ground
5. **Drive to decisions**: Recognize when enough discussion has happened, call for decision
6. **Document outcomes**: Capture decisions, rationale, action items, open questions

**What you're NOT doing**:
- Advocating for a specific approach (unless you're also the presenter)
- Making the decision yourself (unless you're the decision-maker)
- Letting the meeting run itself

## Pre-Review Preparation (The Setup)

### Distribute Design Doc Early

- Send design doc at least 3 days before review
- Include: problem statement, proposed solution, alternatives considered, open questions
- Real format: RFC (Request for Comments) or ADR (Architecture Decision Record)
- If people show up without reading it, reschedule (seriously)

**Why this matters**: Can't have productive discussion if people are reading the doc during the meeting

### Set Clear Objectives

**Bad objective**: "Review the microservices design"

**Good objective**: "Decide: Do we split the monolith into microservices? If yes, what's the service boundary strategy?"

**The difference**: Specific decision to make, not vague "review"

### Identify Required vs Optional Attendees

**Required**: People who need to approve or have critical context
**Optional**: People who want to stay informed

**Why this matters**: 10-person design review is a disaster. Keep it to 5-6 max.

### Prepare Discussion Questions

- What are the 3-5 key questions we need to answer?
- What are the likely points of disagreement?
- What context do reviewers need?

**Example questions**:
- "What's the service boundary strategy? By domain? By team? By data?"
- "How do we handle distributed transactions?"
- "What's the migration strategy from monolith?"

## Creating Psychological Safety (The Foundation)

**The core principle**: People won't share honest feedback if they fear consequences

### Separate Ideas from Identity

**Bad**: "Your design is wrong"
**Good**: "I'm concerned about the scalability of this approach"

**The shift**: Critique the idea, not the person

### Encourage Dissent

**Explicitly say**: "I want to hear concerns and objections. That's why we're here."

**Ask directly**: "What are we missing? What could go wrong?"

**Reward dissent**: "That's a great point. I hadn't thought of that."

### Handle Senior Engineers Who Dominate

**The problem**: Principal engineer speaks first, everyone else falls in line

**The solution**: "Let's hear from everyone before we discuss. [Junior engineer], what's your take?"

**Or**: "I want to hear from people who haven't spoken yet."

**Or**: "Let's do a round-robin. Everyone shares one concern."

### Draw Out Quiet Participants

**The problem**: Introverts stay quiet even when they have valuable input

**The solution**: "I notice you're quiet. What's your take on this?"

**Or**: "You worked on the legacy system. What concerns do you have about migration?"

**Or**: Use written feedback (Slack, Google Doc comments) before the meeting

## Keeping Discussions Productive (The Facilitation Techniques)

### Recognize and Stop Bikeshedding

**The signal**: Discussion is going in circles, people are debating minor details

**The intervention**: "This feels like bikeshedding. Let's table this and focus on the critical decisions."

**Or**: "We've spent 20 minutes on naming. Let's move to the database architecture decision."

**The key**: Name it explicitly, redirect to high-impact decisions

### Time-Box Discussions

**The technique**: "We have 15 minutes for this decision. Let's focus."

**Why it works**: Parkinson's Law - work expands to fill time. Constrain time, force focus.

**Example**: 
- 10 minutes: Present design
- 15 minutes: Discuss database choice
- 15 minutes: Discuss service boundaries
- 10 minutes: Discuss migration strategy
- 10 minutes: Make decisions and document

### The Parking Lot Technique

**The problem**: Tangents derail the discussion

**The solution**: "That's important, but it's out of scope for this review. Let's add it to the parking lot and address it separately."

**Keep a visible parking lot**: Whiteboard, shared doc, whatever

**Follow up**: Actually address parking lot items later (or people stop trusting the technique)

### Focus on High-Impact Decisions

**The question**: "What's the decision that's hardest to reverse?"

**Prioritize**: Irreversible decisions > reversible decisions

**Example**:
- Database choice: Hard to reverse (prioritize)
- API endpoint naming: Easy to reverse (deprioritize)
- Service boundaries: Hard to reverse (prioritize)
- Logging format: Easy to reverse (deprioritize)

## Handling Disagreements Between Reviewers (The Hard Part)

### The Facilitator's Stance: Neutral

**Your job**: Help them reach a decision, not pick a side

**Even if you have an opinion**: Set it aside while facilitating

**If you can't be neutral**: Get someone else to facilitate

### Facilitate Technical Debates

**The structure**:
1. "Let's hear both perspectives fully before discussing"
2. "Engineer A, explain your reasoning"
3. "Engineer B, explain your reasoning"
4. "What are the tradeoffs between these approaches?"
5. "What data would help us decide?"

**The key**: Make it about tradeoffs, not right vs wrong

### Find Common Ground

**The question**: "What do we agree on?"

**Often**: People agree on the problem, disagree on the solution

**Example**:
- Agree: Need better scalability
- Disagree: Microservices vs optimized monolith
- Common ground: Need to handle 10x load within 6 months

**The reframe**: "We agree on the goal. Let's evaluate approaches against that goal."

### Escalation Criteria (When to Involve Leadership)

**Escalate when**:
- Technical disagreement can't be resolved with data
- Decision requires business context the team doesn't have
- Decision has significant cost or risk implications
- Reviewers have equal authority and can't reach consensus

**Don't escalate when**:
- You just haven't tried hard enough to facilitate
- You're avoiding conflict
- You want someone else to make the hard call

**How to escalate**: "We've identified two viable approaches with different tradeoffs. We need leadership input on [specific question]."

## Decision-Making Frameworks (How to Actually Decide)

### Consensus vs Consent vs DACI

**Consensus**: Everyone agrees (rare, slow, often impossible)

**Consent**: No one has a blocking objection (more practical)

**DACI**: Driver, Approver, Contributors, Informed (clear roles)

**When to use each**:
- Consensus: Small team, low-stakes decision, plenty of time
- Consent: Medium team, medium-stakes, need to move forward
- DACI: Large team, high-stakes, need clear accountability

### When to Decide vs When to Defer

**Decide now when**:
- You have enough information
- The decision is blocking other work
- Delaying has a cost
- The decision is reversible (can change later if wrong)

**Defer when**:
- Missing critical information
- Need to prototype or test assumptions
- Decision isn't blocking anything
- Emotions are high (let people cool down)

**The key**: Explicit decision to defer, with criteria for when to revisit

### The "Disagree and Commit" Principle

**The scenario**: Can't reach consensus, need to move forward

**The approach**: "We've heard all perspectives. We're going with approach A. If you disagree, I need you to commit to making it work anyway."

**Why it works**: Acknowledges disagreement, but prevents sabotage

**When to use**: After genuine attempt to reach consensus, when decision needs to be made

## Documenting Outcomes (The Follow-Through)

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

### The ADR Format (Architecture Decision Record)

**Structure**:
- Title: Short noun phrase
- Status: Proposed, Accepted, Deprecated, Superseded
- Context: What's the issue we're addressing?
- Decision: What are we doing?
- Consequences: What are the results (good and bad)?

**Example**:
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

### Send Follow-Up Within 24 Hours

**Subject**: "Design Review Follow-Up: [Topic]"

**Body**:
- Decisions made
- Action items (owner, deadline)
- Open questions
- Next steps

**Why 24 hours**: Memory is fresh, momentum is maintained

## When You're Both Presenter and Facilitator (The Hardest Scenario)

**The challenge**: You're presenting YOUR design AND running the review

**The conflict**: Hard to be neutral when it's your design being critiqued

**The solution**: Explicitly separate the roles

**How**:
1. Present your design (presenter mode)
2. "Now I'm switching to facilitator mode. I want to hear all concerns and objections."
3. Facilitate the discussion (facilitator mode)
4. If you need to defend a decision, say: "Let me switch back to presenter mode for a moment..."

**The key**: Make the role switch explicit and visible

**Alternative**: Get someone else to facilitate while you present

## Real-World Example: The Microservices Migration Review

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
- "Our objective: Decide on service boundary strategy. We have 90 minutes."
- "Ground rules: Critique ideas, not people. Everyone's input matters."
- "Decision-making: We'll use consent - no blocking objections."

**10-25 min: Present design**
- Presenter walks through proposed domain-based boundaries
- Shows service map, data flow, migration strategy

**25-40 min: Discuss service boundaries**
- Senior Engineer A: "Domain boundaries are cleaner architecturally"
- Senior Engineer B: "Team boundaries are more practical for our org structure"
- Facilitator: "Let's hear both perspectives fully. Engineer A, explain your reasoning."
- [Both explain]
- Facilitator: "What are the tradeoffs?"
- [Discussion of tradeoffs]
- Facilitator: "What data would help us decide?"
- Mid-level engineer: "We should look at our team structure and roadmap"
- [Review team structure]
- Facilitator: "Based on this, team boundaries seem more practical. Any blocking objections?"
- [No blocking objections]
- **Decision: Team-based boundaries**

**40-55 min: Discuss distributed transactions**
- Junior engineer (quiet): "How do we handle transactions across services?"
- Facilitator: "Great question. What are our options?"
- [Discussion of saga pattern, 2PC, eventual consistency]
- Senior Engineer A: "We should use saga pattern"
- Facilitator: "Any concerns with saga pattern?"
- Mid-level engineer: "It's complex to implement"
- Facilitator: "What's the alternative?"
- [Discussion]
- Facilitator: "Sounds like saga pattern is the right approach despite complexity. Any blocking objections?"
- [No blocking objections]
- **Decision: Saga pattern for distributed transactions**

**55-70 min: Discuss migration strategy**
- [Discussion of phased migration]
- Architect: "We need to run both systems in parallel during migration"
- Facilitator: "What's the risk?"
- [Discussion of data consistency risks]
- Facilitator: "How do we mitigate?"
- [Discussion of reconciliation strategy]
- **Decision: Phased migration with parallel run and daily reconciliation**

**70-85 min: Open questions and parking lot**
- Facilitator: "What questions are still open?"
- [List open questions: monitoring strategy, testing approach, rollback procedure]
- Facilitator: "What's in the parking lot?"
- [List parking lot items: API versioning strategy, service mesh evaluation]

**85-90 min: Document and wrap**
- Facilitator: "Let me summarize decisions..."
- [Read back decisions]
- Facilitator: "Action items..."
- [Assign owners and deadlines]
- Facilitator: "I'll send follow-up within 24 hours with ADRs"

**The Follow-Up**:
- Sent within 24 hours
- 3 ADRs documented (service boundaries, distributed transactions, migration strategy)
- Action items with owners and deadlines
- Open questions listed
- Parking lot items scheduled for separate discussion

**Why it worked**:
- Clear objective and time-boxing
- Psychological safety (everyone contributed)
- Facilitated disagreement productively
- Made decisions with consent
- Documented outcomes immediately

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

- Facilitating is different from presenting - you're guiding the process, not advocating for an outcome
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

Target: ~2,000 words when complete (this is v1 outline, flesh out in v2)
