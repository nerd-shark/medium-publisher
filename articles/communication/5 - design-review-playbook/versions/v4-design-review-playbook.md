---
title: "The Design Review Playbook: Facilitating Technical Discussions That Actually Work"
subtitle: "Good design reviews aren't about finding flaws—they're about collaborative problem-solving. Here's how to facilitate decisions, not just debates."
series: "Communication Part 5"
reading-time: "12 minutes"
target-audience: "Senior engineers, tech leads, engineering managers"
keywords: "design review, facilitation, technical discussions, decision-making, engineering leadership, design review best practices, facilitating technical discussions"
tags: ["Engineering Leadership", "Technical Communication", "Design Reviews", "Facilitation", "Decision Making"]
status: "v4-publication-ready"
created: "2026-03-13"
author: "Daniel Stauffer"
seo-description: "Learn how to facilitate productive design reviews that lead to decisions, not endless debates. Practical techniques for tech leads and engineering managers."
---
# The Design Review Playbook: Facilitating Technical Discussions That Actually Work

## Good design reviews aren't about finding flaws—they're about collaborative problem-solving. Here's how to facilitate decisions, not just debates.

*Part 5 of my series on Technical Communication. Last time we covered [surviving architecture reviews](link-to-part-4) by preparing your thinking, not just your slides. This time we're flipping the script: what happens when YOU'RE the one running the design review, not presenting in it?

## The Design Review That Went Sideways

It's 2:15 PM on a Tuesday in Conference Room B. You're 15 minutes into what's supposed to be a 2-hour design review for a microservices migration that could save the company $200K annually in infrastructure costs.

The junior engineer presenting the design has just finished explaining the proposed service boundaries—three services aligned with the three product teams, clean separation of concerns, reasonable data boundaries. She's clicking to the next slide when a hand shoots up.

"Wait, why are we using MongoDB for the user service?" asks the Senior Backend Engineer, leaning forward in his chair, brow furrowed. "PostgreSQL would be way better for this use case. We need ACID guarantees for user data."

The Principal Engineer sitting across from him straightens up, closing his laptop with a soft thud. "MongoDB gives us the flexibility we need here. We don't even know what the final schema looks like yet. Schema-less is the right call."

"That's exactly the problem," the Backend Engineer shoots back, his voice rising slightly. "No schema means no data integrity. I've seen this movie before at my last company—it always ends with data corruption and angry customers filing support tickets."

"You're being dogmatic," the Principal responds, crossing his arms. His tone is measured but firm. "MongoDB is perfectly fine for this. We've used it successfully on three other projects. This isn't 2015 anymore."

"Those projects were different. This is user authentication data. We can't afford to—"

"We're not going to have data corruption. That's a strawman argument."

30 minutes later, they're still at it. The MongoDB vs PostgreSQL holy war is in full swing. The other four attendees have their laptops open, half-watching the debate while catching up on Slack messages and email. The junior engineer who's supposed to be presenting is just sitting there, pen frozen over her notebook, watching two senior engineers argue about databases like it's a tennis match she can't interrupt.

Nobody is facilitating. Everyone is advocating.

The meeting ends at 4:00 PM with the dreaded "let's schedule a follow-up to continue the discussion." No decisions made. No progress. Just two hours of everyone's time burned—12 person-hours at an average fully-loaded cost of $150/hour, that's $1,800 wasted. And a junior engineer who now thinks design reviews are pointless theater.

This is what happens when design reviews have no facilitator.

## The Facilitator vs Presenter Distinction

Here's the shift that changes everything: when you're running a design review, you're not presenting. You're facilitating.

When you're presenting (which we covered in [Part 4](link-to-part-4)), your job is to defend your design, answer questions, and convince others your approach is right. You're focused on your solution. You're attached to the outcome. When someone suggests a different approach, your instinct is to defend your choice. That's appropriate—you're the presenter.

When you're facilitating, your job is completely different. You're guiding the discussion, drawing out concerns, and helping the group reach a decision. You're focused on the process, not the outcome. You want a good decision, not necessarily YOUR decision. When someone suggests a different approach, your instinct should be to explore it: "Tell me more about that. What are the tradeoffs?"

The difference matters. A presenter advocates. A facilitator guides.

Think of it like being a referee in a soccer match. The referee doesn't score goals. The referee doesn't pick which team should win. The referee ensures the game is played fairly, enforces the rules, and keeps things moving. That's facilitation.

The hardest scenario? When you're both presenter AND facilitator. You're presenting YOUR design AND running the review. It's like being both player and referee. We'll tackle that later, because it requires explicitly separating the roles in a way that feels unnatural at first.

## The Four Types of Design Reviews (And When to Use Each)

Not all design reviews are created equal. Depending on the scope, risk, and complexity of your project, you might need one design review or four. Here's the progression I've seen work across multiple organizations.

### Requirements Design Review (Requirements DR)

**When:** Early in the project, before any design work begins
**Purpose:** Validate that we're solving the right problem
**Duration:** 60-90 minutes
**Attendees:** Product managers, tech leads, key stakeholders, domain experts

This is where you validate requirements before investing in design. You're asking: "Do we understand the problem? Are these the right requirements? What are we missing?"

Real example: A healthcare company was building a patient scheduling system. In the Requirements DR, a nurse practitioner pointed out that the requirements assumed patients would schedule their own appointments online. In reality, 60% of their patients were elderly and preferred phone scheduling. That insight changed the entire project scope before a single line of code was written.

**Key questions:**

- What problem are we solving, and for whom?
- What are the success criteria?
- What are the constraints (budget, timeline, compliance)?
- What assumptions are we making?
- What's out of scope?

**When to skip:** Small features, bug fixes, well-understood problems with clear requirements.

### Preliminary Design Review (Preliminary DR)

**When:** After requirements are validated, before detailed design
**Purpose:** Validate the high-level approach and architecture
**Duration:** 90-120 minutes
**Attendees:** Engineering team, architects, tech leads, senior engineers

This is where you validate the overall approach. You're asking: "Is this the right architecture? Are we using the right technologies? What are the major risks?"

You're working at the 30,000-foot level: microservices vs monolith, SQL vs NoSQL, synchronous vs asynchronous, cloud provider choice. You're NOT discussing implementation details like class names or API endpoint paths.

Real example: A fintech company was building a payment processing system. In the Preliminary DR, they decided on event-driven architecture with Kafka for audit trails and compliance. They also decided to use PostgreSQL for transactional data and DynamoDB for session data. These high-level decisions guided all subsequent work.

**Key questions:**

- What's the high-level architecture?
- What technologies are we using, and why?
- What are the major technical risks?
- How does this integrate with existing systems?
- What's the deployment strategy?

**When to skip:** Incremental features that fit within existing architecture, minor enhancements that don't change the system design.

### Detailed Design Review (Detailed DR)

**When:** After preliminary design is approved, before implementation
**Purpose:** Validate the detailed design and implementation plan
**Duration:** 2-3 hours (or multiple sessions)
**Attendees:** Engineering team implementing the feature, relevant domain experts

This is where you get into the weeds. You're asking: "How exactly will this work? What are the data models? What are the APIs? How do we handle edge cases?"

You're working at the 1,000-foot level: database schemas, API contracts, class hierarchies, error handling, state machines. This is where you catch implementation issues before they become code.

Real example: An e-commerce company was building a new checkout flow. In the Detailed DR, they walked through the state machine for order processing: pending → payment_processing → payment_confirmed → fulfillment → shipped → delivered. They identified 8 edge cases (payment timeout, inventory depletion, address validation failure) and designed error handling for each. This prevented production bugs.

**Key questions:**

- What are the data models and schemas?
- What are the API contracts?
- How do we handle errors and edge cases?
- What are the performance characteristics?
- How do we test this?
- What's the rollback plan?

**When to skip:** Proof of concepts, prototypes, exploratory work where you expect to throw away the code.

### Final Design Review (Final DR)

**When:** After implementation, before production deployment
**Purpose:** Validate that the implementation matches the design and is production-ready
**Duration:** 60-90 minutes
**Attendees:** Engineering team, SRE/operations, security team, tech leads

This is the production readiness review. You're asking: "Is this ready to ship? Have we addressed all the concerns from previous reviews? What could go wrong in production?"

You're reviewing: monitoring and alerting, security considerations, performance testing results, rollback procedures, runbooks, documentation.

Real example: A SaaS company was deploying a new authentication service. In the Final DR, the SRE team identified that there was no alerting for failed login attempts (potential security issue) and no runbook for password reset failures (operational issue). Both were added before deployment.

**Key questions:**

- Does the implementation match the approved design?
- Have we addressed all concerns from previous reviews?
- What's our monitoring and alerting strategy?
- What's the rollback plan if something goes wrong?
- Do we have runbooks for common issues?
- Have we done load testing?
- What are the security implications?

**When to skip:** Internal tools, low-risk features, features with gradual rollout where you can monitor and iterate.

### Choosing the Right Reviews for Your Project

**High-risk, high-complexity projects** (new systems, major architecture changes, compliance-critical features):

- All four reviews: Requirements DR → Preliminary DR → Detailed DR → Final DR
- Example: Building a new payment processing system

**Medium-risk, medium-complexity projects** (new features, significant refactoring):

- Two or three reviews: Preliminary DR → Detailed DR → Final DR (skip Requirements DR if requirements are clear)
- Example: Adding multi-region support to an existing service

**Low-risk, low-complexity projects** (incremental features, bug fixes):

- One review: Detailed DR or Final DR (skip early reviews)
- Example: Adding a new API endpoint to an existing service

**Prototypes and experiments:**

- Zero or one review: Maybe a Preliminary DR to validate approach, skip the rest
- Example: Proof of concept for a new technology

The key is matching the review process to the risk. Over-reviewing wastes time. Under-reviewing creates production incidents.

## Why Design Reviews Fail: The Five Deadly Patterns

Before we talk about how to facilitate well, let's understand why design reviews fail. I've facilitated over 100 design reviews across fintech, healthcare, and e-commerce companies. I've seen five patterns repeatedly, and once you recognize them, you can't unsee them.

### Pattern 1: Bikeshedding (Parkinson's Law of Triviality)

The team spends 5 minutes on the critical database architecture decision that will determine whether the system can scale to 10 million users. Then they spend 45 minutes arguing about whether to use `userId` or `user_id` in the API.

Why? Because variable naming is easy to have opinions about. Everyone understands it. You don't need to be a database expert to have a strong opinion about camelCase vs snake_case. Database architecture requires expertise that not everyone in the room has, so people stay quiet.

This is Parkinson's Law of Triviality: people focus on what they understand, not what matters.

Real example from a fintech company I consulted with in 2024: The team spent an entire 90-minute design review debating REST vs GraphQL for their public API. Passionate arguments about over-fetching, under-fetching, type safety, tooling maturity. Meanwhile, nobody questioned the decision to use a single PostgreSQL database for 10 microservices. That decision caused production incidents six months later when the database became a bottleneck during a traffic spike, costing them $50K in lost transactions. The API choice? Didn't matter. They could have flipped a coin.

The problem isn't that people are stupid. It's that bikeshedding feels productive. You're having a technical discussion, making points, feeling smart. But you're optimizing the wrong thing.

### Pattern 2: The Loudest Voice Wins

A Principal Engineer dominates the discussion. Junior engineers stay quiet even when they have valid concerns. The decision gets made based on seniority, not merit.

I watched this happen at a Series B startup in Seattle. The Principal Engineer pushed hard for event sourcing because "it's the right architectural pattern for this domain." He drew diagrams on the whiteboard, cited Martin Fowler, talked about immutability and audit trails. Nobody challenged it. He was the principal, after all—he must know what he's talking about.

Six months later, the team was drowning in debugging complexity. Every bug required replaying thousands of events to figure out what went wrong. A simple "why is this user's balance incorrect?" question turned into hours of event replay and analysis. The junior engineer who had stayed quiet in that review? She had worked at a company that tried event sourcing and abandoned it after 8 months. She knew it was a bad fit for their use case. But she didn't speak up because she was junior and he was principal.

The problem isn't that senior engineers are wrong. It's that hierarchy kills honest feedback. When the most senior person in the room has a strong opinion, everyone else calculates the social cost of disagreeing. Usually, they decide it's not worth it.

### Pattern 3: Analysis Paralysis

Every decision requires "more research." The team needs to "evaluate 5 more options before deciding." They need to "prototype all approaches." The meeting ends with action items, no decisions.

I saw a team at a healthcare company spend 3 months evaluating message queues. Kafka, RabbitMQ, SQS, Kinesis, Pulsar. They created comparison matrices with 20 criteria. They built prototypes. They read whitepapers. They attended conference talks. By the time they finally decided on Kafka, the requirements had changed—they needed real-time processing, not just message queuing—and they needed a different solution entirely.

The problem isn't that research is bad. It's that fear of making the wrong decision prevents making any decision. And in software, not deciding IS a decision—it's a decision to keep the status quo, which often has its own costs. That team's 3-month delay meant they missed a critical product launch window.

### Pattern 4: Design by Committee

Everyone has input. The design becomes a Frankenstein of compromises. Nobody is happy with the result.

Real example from an e-commerce platform: An API design that tried to satisfy 5 different teams. The mobile team wanted REST because that's what their SDK supported. The web team wanted GraphQL because they needed flexible queries. The IoT team wanted gRPC because they needed performance. The result? A REST API with GraphQL-style nested queries and gRPC-style error codes. Inconsistent, confusing, and nobody liked it. The mobile team still had to write custom parsing logic. The web team still had to make multiple requests. The IoT team still had performance issues.

The problem isn't that input is bad. It's that too many cooks with no clear decision-maker leads to designs that try to please everyone and end up pleasing no one.

### Pattern 5: The Missing Context

A reviewer suggests an approach that was already tried and failed. Or suggests an approach that doesn't fit constraints. Or questions decisions that were already made by leadership.

I watched an architect spend 20 minutes in a design review advocating for multi-region deployment for better availability. Great idea—99.99% uptime, disaster recovery, lower latency for global users. Except the budget had been cut two weeks earlier and multi-region was off the table. The CFO had made it clear: single region only, optimize for cost. Nobody had told the architect. He was suggesting something that wasn't even an option.

The problem isn't that reviewers are out of touch. It's that context doesn't spread evenly. The presenter has been living with this problem for weeks, attending stakeholder meetings, understanding constraints. The reviewers are seeing it for the first time. That context gap creates friction.

## The Facilitator's Job: Six Core Responsibilities

Your job as facilitator isn't to make the decision. It's to help the group make a good decision.

Specifically, you're doing six things:

**1. Set the stage.** Before the discussion even starts, you're establishing clear objectives, ground rules, and the decision-making process. "Our objective today is to decide on the service boundary strategy. We have 90 minutes. Ground rules: critique ideas, not people. Everyone's input matters. We'll use consent for decision-making—meaning we move forward unless someone has a blocking objection. Questions before we start?"

**2. Guide the discussion.** You're keeping it focused, preventing tangents, and managing time. When someone brings up API versioning in a discussion about database choice, you're the one saying "That's important, but let's add it to the parking lot and stay focused on the database decision."

**3. Draw out concerns.** You're getting quiet people to speak. You're surfacing hidden objections. You're asking "What are we missing? What could go wrong?" and actually waiting for answers. You're noticing when the junior engineer looks like she wants to say something but hesitates.

**4. Manage conflict.** You're facilitating debates, preventing personal attacks, and finding common ground. When two engineers disagree, you're not picking a side—you're helping them articulate their reasoning and evaluate tradeoffs.

**5. Drive to decisions.** You're recognizing when enough discussion has happened and calling for a decision. You're not letting the meeting end with "let's think about it and reconvene." You're saying "We've heard both perspectives. Let's decide."

**6. Document outcomes.** You're capturing decisions, rationale, action items, and open questions. You're sending the follow-up email within 24 hours so decisions don't evaporate into the ether.

What you're NOT doing: advocating for a specific approach (unless you're also the presenter), making the decision yourself (unless you're the decision-maker), or letting the meeting run itself.

The facilitator is the person who cares more about the process than the outcome. You want a good decision, not a specific decision.

## Pre-Review Preparation: The Work Before the Work

The best design reviews happen before you walk into the room.

**Send the design doc at least 3 days before the review.** Use a standard format—RFC (Request for Comments) or ADR (Architecture Decision Record). Include the problem statement (what are we solving?), proposed solution (high-level approach), alternatives considered (what else did we evaluate?), and open questions (what do we need to decide?).

If people show up without reading it, reschedule. Seriously. I know a team at a SaaS company that rescheduled when 4 of 6 people hadn't read the doc. It felt awkward—"Sorry, we're not ready"—but it saved everyone's time. You can't have a productive discussion if people are reading the doc during the meeting, trying to catch up while others are already debating implementation details.

**Set clear objectives.** Not "Review the microservices design" but "Decide: Do we split the monolith into microservices? If yes, what's the service boundary strategy?" The difference is specificity. You're naming the decision to make, not just the topic to discuss.

Bad objective: "Discuss the new architecture"
Good objective: "Decide: PostgreSQL or DynamoDB for the user service, based on consistency requirements and query patterns"

**Identify required vs optional attendees.** Required people are those who need to approve or have critical context. Optional people are those who want to stay informed. Keep it to 5-6 people max. A 10-person design review is a disaster—too many voices, too much coordination overhead, too much time wasted. Use the "two pizza rule": if you can't feed the group with two pizzas, it's too big.

**Prepare discussion questions.** What are the 3-5 key questions we need to answer? What are the likely points of disagreement? What context do reviewers need? For a microservices migration, your questions might be: "What's the service boundary strategy—by domain, by team, or by data?" "How do we handle distributed transactions?" "What's the migration strategy from the monolith—big bang or phased?"

These questions guide the discussion and keep it focused. Without them, the discussion wanders into interesting but irrelevant territory.

## Creating Psychological Safety: Making Dissent Safe

People won't share honest feedback if they fear consequences. Your job as facilitator is to create an environment where dissent is safe.

**Separate ideas from identity.** When someone says "Your design is wrong," they're attacking the person. When they say "I'm concerned about the scalability of this approach," they're critiquing the idea. The shift is subtle but powerful. Model this language: "I have concerns about this approach" not "You're wrong."

**Explicitly encourage dissent.** Say it out loud at the start: "I want to hear concerns and objections. That's why we're here. If you see a problem, speak up." Ask directly: "What are we missing? What could go wrong?" And when someone raises a concern, reward it immediately: "That's a great point. I hadn't thought of that. Thank you."

When people see dissent rewarded, they're more likely to speak up. When they see dissent punished—even subtly, with a dismissive tone or a quick rebuttal—they shut down.

**Handle senior engineers who dominate.** The problem is real: the Principal Engineer speaks first with a strong opinion, and everyone else falls in line. The solution is to explicitly create space for other voices.

Try these techniques:

- "Let's hear from everyone before we discuss. [Junior engineer], what's your take?"
- "I want to hear from people who haven't spoken yet."
- "Let's do a round-robin. Everyone shares one concern, no discussion yet."
- "Before we hear from [Principal], let's get input from the team."

**Draw out quiet participants.** Introverts stay quiet even when they have valuable input. Call on them directly, but do it respectfully: "I notice you're quiet, [Name]. What's your take on this?" Or leverage their expertise: "You worked on the legacy system. What concerns do you have about this migration approach?"

Or use written feedback—Slack, Google Doc comments—before the meeting. Some people think better in writing than in real-time discussion. I've seen brilliant insights come from engineers who never spoke up in meetings but wrote detailed comments in the design doc.

## Keeping Discussions Productive: Techniques That Work

**Recognize and stop bikeshedding.** The signal: discussion is going in circles, people are debating minor details, energy is high but progress is low. The intervention: "This feels like bikeshedding. Let's table this and focus on the critical decisions." Or: "We've spent 20 minutes on naming conventions. Let's move to the database architecture decision, which is harder to reverse."

Name it explicitly. Don't let it continue. Redirect to high-impact decisions.

**Time-box discussions.** "We have 15 minutes for this decision. Let's focus." Why it works: Parkinson's Law—work expands to fill time. Constrain time, force focus.

Example agenda for a 90-minute review:

- 0-10 min: Set the stage, review objectives
- 10-25 min: Present design
- 25-40 min: Discuss database choice (time-boxed)
- 40-55 min: Discuss service boundaries (time-boxed)
- 55-70 min: Discuss migration strategy (time-boxed)
- 70-85 min: Make decisions and document
- 85-90 min: Review action items and next steps

**Use the parking lot technique.** When tangents derail the discussion: "That's important, but it's out of scope for this review. Let's add it to the parking lot and address it separately." Keep a visible parking lot—whiteboard, shared doc, whatever works.

And critically: actually address parking lot items later. Schedule a follow-up, assign an owner, set a deadline. If you don't, people stop trusting the technique. They'll think "parking lot" means "ignore forever."

**Focus on high-impact decisions.** Ask: "What's the decision that's hardest to reverse?" Prioritize irreversible decisions over reversible ones.

Examples:

- Database choice: Hard to reverse (prioritize)
- API endpoint naming: Easy to reverse (deprioritize)
- Service boundaries: Hard to reverse (prioritize)
- Logging format: Easy to reverse (deprioritize)
- Data model: Hard to reverse (prioritize)
- Variable naming: Easy to reverse (deprioritize)

Focus energy where it matters most. Let the easy-to-reverse decisions be made quickly or even deferred.

## Handling Disagreements: The Facilitator's Hardest Job

This is where facilitation gets real. Two engineers disagree. Both have valid points. Both are passionate. How do you facilitate without picking a side?

**Stay neutral.** Your job is to help them reach a decision, not pick a side. Even if you have an opinion—and you probably do—set it aside while facilitating. If you can't be neutral, get someone else to facilitate. Neutrality is essential for trust.

I've seen facilitators lose credibility in seconds by saying "I think approach A is better" while supposedly facilitating. The moment you pick a side, you're no longer facilitating—you're advocating.

**Facilitate technical debates with structure.** Don't let it devolve into an argument. Use this structure:

1. "Let's hear both perspectives fully before discussing."
2. "Engineer A, explain your reasoning. Everyone else, just listen."
3. "Engineer B, explain your reasoning. Everyone else, just listen."
4. "What are the tradeoffs between these approaches?"
5. "What data or criteria would help us decide?"

Make it about tradeoffs, not right vs wrong. Most technical decisions are tradeoffs, not absolutes. There's rarely a "correct" answer—there's usually "better for X, worse for Y."

**Find common ground.** Ask: "What do we agree on?" Often people agree on the problem but disagree on the solution.

Example:

- Agree: We need better scalability
- Disagree: Microservices vs optimized monolith
- Common ground: Need to handle 10x load within 6 months

Reframe: "We agree on the goal—10x load in 6 months. Let's evaluate both approaches against that goal. What's the fastest path to 10x? What's the lowest risk?"

**Know when to escalate.** Escalate when:

- Technical disagreement can't be resolved with data
- Decision requires business context the team doesn't have
- Decision has significant cost or risk implications
- Reviewers have equal authority and can't reach consensus

Don't escalate when:

- You just haven't tried hard enough to facilitate
- You're avoiding conflict
- You want someone else to make the hard call

How to escalate properly: "We've identified two viable approaches with different tradeoffs. Approach A optimizes for speed, approach B optimizes for cost. We need leadership input on whether speed or cost is the priority for this project."

## Decision-Making Frameworks: How to Actually Decide

**Consensus** means everyone agrees. It's rare, slow, and often impossible. Use it for small teams (2-3 people), low-stakes decisions, when you have plenty of time.

**Consent** means no one has a blocking objection. It's more practical. "Does anyone have a blocking objection to this approach?" Silence means consent. Use it for medium teams (4-6 people), medium-stakes decisions, when you need to move forward.

**DACI** assigns clear roles:

- Driver: Runs the process, gathers input
- Approver: Makes the final decision
- Contributors: Provide input
- Informed: Kept in the loop

Use it for large teams (7+ people), high-stakes decisions, when you need clear accountability.

Most design reviews work best with consent. You're not trying to make everyone happy—you're trying to make a decision that no one finds unacceptable.

**Know when to decide vs when to defer.** Decide now when: you have enough information, the decision is blocking other work, delaying has a cost, or the decision is reversible (you can change it later if wrong).

Defer when: you're missing critical information, you need to prototype or test assumptions, the decision isn't blocking anything, or emotions are high (let people cool down).

Make deferring an explicit decision with criteria for when to revisit: "We're deferring the database choice until we have load testing results. We'll reconvene next Tuesday with data."

**Use "disagree and commit"** when you can't reach consensus but need to move forward. This is Amazon's principle, and it works.

"We've heard all perspectives. We're going with approach A. If you disagree, I need you to commit to making it work anyway. Can everyone commit?"

This acknowledges disagreement but prevents sabotage. It says: "Your objection was heard and considered. The decision went a different way. Now we need you to support it."

## Documenting Outcomes: Making Decisions Stick

The meeting doesn't end when people leave the room. Without documentation, decisions evaporate.

**Document decisions made:** What was decided, why (the reasoning), who made the decision, when it was made.

**Document alternatives rejected:** What options were considered, why they were rejected, what tradeoffs were made. This prevents relitigating the same decision in 3 months when someone new joins and asks "why didn't we use X?"

**Document open questions:** What's still unresolved, what needs more research, what assumptions need validation.

**Document action items:** What needs to happen next, who's responsible, when it's due.

**Use the ADR format (Architecture Decision Record).** This is the gold standard for documenting technical decisions.

Structure:

- **Title:** Short noun phrase (e.g., "Use PostgreSQL for Primary Database")
- **Status:** Proposed, Accepted, Deprecated, Superseded
- **Context:** What's the issue we're addressing?
- **Decision:** What are we doing?
- **Consequences:** What are the results, good and bad?

Example:

```
# ADR-001: Use PostgreSQL for User Service Database

## Status
Accepted (2026-03-13)

## Context
We need a database for the user service. Requirements:
- ACID guarantees for financial transactions
- Complex queries for reporting (joins, aggregations)
- Horizontal scalability for growth (10M users in 2 years)
- Team has limited NoSQL experience

## Decision
We will use PostgreSQL 15 with read replicas for scaling.

## Consequences
**Positive:**
- ACID guarantees meet compliance requirements
- Rich query capabilities support reporting needs
- Team has 5 years PostgreSQL expertise
- Mature tooling and monitoring

**Negative:**
- Requires operational expertise for scaling
- Vertical scaling limits (mitigated by read replicas)
- More complex than managed NoSQL options
- Potential bottleneck if write load exceeds expectations

## Alternatives Considered
- **DynamoDB:** Rejected due to lack of complex query support, team would need to learn new technology
- **MongoDB:** Rejected due to weaker consistency guarantees, past data corruption issues
```

**Send follow-up within 24 hours.** Subject: "Design Review Follow-Up: [Topic]"

Body:

- Decisions made (with links to ADRs)
- Action items (owner, deadline)
- Open questions (owner, deadline)
- Next steps

Why 24 hours? Memory is fresh, momentum is maintained. The follow-up email is where decisions become real. Without it, people remember different things, and you'll be relitigating decisions in the next meeting.

## When You're Both Presenter and Facilitator

This is the hardest scenario. You're presenting YOUR design AND running the review. It's like being both player and referee in a soccer match.

The challenge: It's hard to be neutral when it's your design being critiqued. Your instinct is to defend, not facilitate.

The solution: Explicitly separate the roles. Make the role switch visible.

How:

1. Present your design (presenter mode): "Here's the proposed architecture. Three services, PostgreSQL for user data, Redis for caching."
2. Switch roles explicitly: "Now I'm switching to facilitator mode. I want to hear all concerns and objections. What are we missing?"
3. Facilitate the discussion (facilitator mode): Stay neutral, draw out concerns, manage conflict.
4. If you need to defend a decision, switch back: "Let me switch back to presenter mode for a moment. The reason we chose PostgreSQL is..."

Make the role switch explicit and visible. Say it out loud. It feels awkward at first, but it works.

Alternative: Get someone else to facilitate while you present. This is cleaner but not always possible. If you have a tech lead or engineering manager who can facilitate, use them.

This is hard but learnable. I've watched engineers get better at this over time. Practice the role switch. Get comfortable saying "I'm in facilitator mode now" and meaning it.

## Real-World Example: The 90-Minute Microservices Review That Actually Worked

Let me show you how this works in practice. This is a real design review I facilitated at a fintech company in 2025 (details anonymized).

**The Setup:**

- Team wants to split monolith into microservices to improve deployment velocity
- 6 attendees: 2 senior engineers, 2 mid-level, 1 junior, 1 architect
- 90-minute review scheduled for Tuesday 2 PM
- Design doc sent 3 days prior with RFC format
- Clear objective: Decide on service boundary strategy

**Pre-Review Prep:**

- Objective defined: "Decide: team-based vs domain-based service boundaries"
- Key questions identified: How do we handle distributed transactions? What's migration strategy?
- Likely disagreement anticipated: Senior Engineer A prefers domain boundaries (cleaner architecture), Senior Engineer B prefers team boundaries (matches org structure)

**The Review:**

**0-10 min: Set the stage**

I start: "Our objective today: decide on service boundary strategy. We have 90 minutes. Ground rules: critique ideas, not people. Everyone's input matters. We'll use consent for decision-making—no blocking objections. Questions before we start?"

One question about what "blocking objection" means. I clarify: "A blocking objection is when you believe the approach will cause significant harm and you can't support it. It's not just disagreement—it's 'this will fail and I can't be part of it.'"

**10-25 min: Present design**

The junior engineer presents the proposed domain-based boundaries. Shows service map, data flow, migration strategy. Clear, well-prepared. 15 minutes.

**25-40 min: Discuss service boundaries**

Senior Engineer A: "Domain boundaries are cleaner architecturally. Each service owns a complete business capability. That's the whole point of microservices."

Senior Engineer B: "Team boundaries are more practical. We have three teams, we should have three services. Otherwise we'll have coordination overhead every time we need to change something."

I facilitate: "Let's hear both perspectives fully. Engineer A, explain your reasoning."

Engineer A explains domain-driven design principles, bounded contexts, how domain boundaries lead to better encapsulation and fewer cross-service dependencies.

"Engineer B, explain your reasoning."

Engineer B explains Conway's Law (systems mirror org structure), team autonomy, how team boundaries reduce communication overhead and speed up delivery.

"What are the tradeoffs?" I ask.

Mid-level engineer: "Domain boundaries are theoretically better, but team boundaries match our org structure. If we do domain boundaries, we'll have multiple teams touching the same service."

"What data would help us decide?"

The team reviews their org structure. Teams are stable, roughly aligned with domains but not perfectly. Product team owns user features, payments team owns transactions, analytics team owns reporting.

I synthesize: "Based on this, it seems team boundaries are more practical for our current org structure. We can refactor to domain boundaries later if teams reorganize. Any blocking objections?"

Silence.

"Hearing none. Decision: team-based service boundaries. I'll document this in an ADR."

**40-55 min: Discuss distributed transactions**

The junior engineer, who's been quiet, raises her hand: "How do we handle transactions that span multiple services? Like when a user makes a payment and we need to update both the user service and the payment service?"

"Great question," I say. "What are our options?"

Discussion of saga pattern, 2PC, eventual consistency. Senior Engineer A advocates for saga pattern: "It's the standard approach for distributed transactions in microservices."

"Any concerns with saga pattern?" I ask.

Mid-level engineer: "It's complex to implement. We'll need to handle compensation logic for every transaction. That's a lot of code."

"What's the alternative?"

Senior Engineer B: "We could avoid distributed transactions entirely by keeping related data in the same service."

"Does that work with our service boundaries?"

Discussion reveals some transactions will span services no matter how boundaries are drawn. Payments need user data, analytics need both.

"Sounds like saga pattern is the right approach despite the complexity. Any blocking objections?"

No objections.

"Decision: saga pattern for distributed transactions. Action item: [Mid-level engineer] research saga pattern libraries—Temporal, Camunda, custom—and present options next week."

**55-70 min: Discuss migration strategy**

Architect: "We need to run both systems in parallel during migration. Otherwise we risk data loss."

"What's the risk?" I ask.

Senior Engineer A: "If we cut over all at once and something breaks, we can't roll back without losing data."

"How do we mitigate?"

Mid-level engineer: "We could do a phased migration. Migrate one service at a time. Run both systems in parallel for each phase."

"What about data consistency during parallel run?"

Senior Engineer B: "We'd need daily reconciliation. Compare data between old and new systems, flag discrepancies."

"That sounds like a solid mitigation. Any blocking objections to phased migration with parallel run and daily reconciliation?"

No objections.

"Decision: phased migration with parallel run and daily reconciliation."

**70-85 min: Open questions and parking lot**

"What questions are still open?"

List: monitoring strategy, testing approach, rollback procedure.

"What's in the parking lot?"

List: API versioning strategy, service mesh evaluation.

"For open questions, who's taking what?"

Assign owners and deadlines for each open question.

**85-90 min: Document and wrap**

"Let me summarize decisions..." I read back three decisions: service boundaries, distributed transactions, migration strategy.

"Action items..." I read back action items with owners and deadlines.

"I'll send follow-up within 24 hours with ADRs for each decision. Thanks everyone."

**The Follow-Up:**

Sent at 9 AM the next day:

- 3 ADRs documented (service boundaries, distributed transactions, migration strategy)
- Action items with owners and deadlines
- Open questions listed with owners
- Parking lot items scheduled for separate discussion

**Why It Worked:**

- Clear objective and time-boxing kept discussion focused
- Psychological safety meant everyone contributed, including the junior engineer
- Disagreement was facilitated productively—heard both perspectives, evaluated tradeoffs
- Decisions were made with consent—no blocking objections
- Outcomes were documented immediately—ADRs within 24 hours

This is what good facilitation looks like.

## The Design Review Checklist

**Before the Review:**

⬜ Design doc sent 3+ days in advance (RFC or ADR format)
⬜ Clear objective and specific decision to make
⬜ Required attendees identified (5-6 max, use two pizza rule)
⬜ Discussion questions prepared (3-5 key questions)
⬜ Time-boxed agenda created
⬜ Likely disagreements anticipated

**During the Review:**

⬜ Set the stage (objective, ground rules, decision-making process)
⬜ Present design clearly (or ensure presenter does)
⬜ Facilitate discussion (don't advocate unless you're also presenting)
⬜ Draw out quiet participants explicitly
⬜ Manage time and prevent tangents (use parking lot)
⬜ Facilitate disagreements productively (stay neutral, explore tradeoffs)
⬜ Drive to decisions (use consent, don't end with "let's think about it")
⬜ Document outcomes in real-time

**After the Review:**

⬜ Send follow-up within 24 hours
⬜ Document decisions in ADRs (with context, decision, consequences)
⬜ Assign action items with owners and deadlines
⬜ Schedule follow-up for open questions
⬜ Address parking lot items (schedule separate discussions)

## Key Takeaways

1. Facilitating is fundamentally different from presenting. You're guiding the process, not advocating for an outcome. Your job is to help the group make a good decision, not to make the decision yourself.
2. Design reviews fail for five predictable reasons: bikeshedding (focusing on trivial details), loud voices (hierarchy killing honest feedback), analysis paralysis (fear of deciding), design by committee (too many compromises), and missing context (reviewers don't have the full picture).
3. Your six core responsibilities as facilitator: set the stage with clear objectives and ground rules, guide the discussion and manage time, draw out concerns from quiet participants, manage conflict productively, drive to decisions when enough discussion has happened, and document outcomes so decisions don't evaporate.
4. Create psychological safety by separating ideas from identity, encouraging dissent explicitly, handling senior engineers who dominate, and drawing out quiet participants. People won't share honest feedback if they fear consequences.
5. Keep discussions productive by recognizing and stopping bikeshedding, time-boxing discussions to force focus, using the parking lot technique for tangents, and focusing on high-impact decisions that are hard to reverse.
6. Handle disagreements by staying neutral, facilitating technical debates with structure, finding common ground, and knowing when to escalate. Most technical decisions are about tradeoffs, not absolutes.
7. Use decision frameworks appropriately: consensus for small teams and low stakes, consent for medium teams and medium stakes, DACI for large teams and high stakes. Most design reviews work best with consent.
8. Document outcomes in ADRs with decisions, rationale, alternatives rejected, and consequences. Send follow-up within 24 hours with decisions, action items, open questions, and next steps.
9. When you're both presenter and facilitator, explicitly separate the roles. Make the role switch visible: "I'm in facilitator mode now" or "Let me switch back to presenter mode for a moment."

## What's Next

In Part 6, we'll explore **Writing Technical Documents That Non-Technical People Actually Read**.

We'll cover:

- The one-page executive summary that gets read
- RFC structure and templates that work
- Architecture Decision Records (ADRs) in depth
- Writing for different audiences (executives, engineers, product managers)
- Visual communication that clarifies instead of confuses

---

## Series Navigation

**Previous Article**: [The Architecture Review Survival Guide: How to Defend Your Technical Decisions](#) *(Part 4)*

**Next Article**: [Writing Technical Documents That Non-Technical People Actually Read](#) *(Part 6)*

**Coming Up**: Communicating technical debt to non-technical stakeholders, cross-functional collaboration between engineering, product, and design

---

*This is Part 5 of the Technical Communication series. Read [Part 1: Speaking Executive](#) to learn C-suite communication fundamentals, [Part 2: Navigating Executive Disagreement](#) for stakeholder dynamics, [Part 3: The Technical Presentation Playbook](#) for audience adaptation, and [Part 4: The Architecture Review Survival Guide](#) for defending your technical decisions.*

**About the Author:** Daniel Stauffer is a software engineer and technical leader with 15+ years of experience facilitating design reviews, architecture discussions, and technical decisions across fintech, healthcare, and e-commerce companies.

**Tags:** #EngineeringLeadership #TechnicalCommunication #DesignReviews #Facilitation #DecisionMaking #SoftwareArchitecture #TechLead #EngineeringManager
