# Reddit Post - Design Review Playbook

## r/ExperiencedDevs

**Title:** What I learned facilitating 100+ design reviews: The facilitator's playbook

**Post:**

Your design review just turned into a 2-hour MongoDB vs PostgreSQL holy war. No decisions made. Everyone's frustrated. The junior engineer who was supposed to be presenting is just sitting there watching two senior engineers argue.

Sound familiar?

I've been there. I've facilitated over 100 design reviews across fintech, healthcare, and e-commerce companies. I've seen the same patterns repeatedly, and I finally wrote down what actually works.

**The core problem:** Nobody is facilitating. Everyone is advocating.

Here's what I mean: When you're presenting your design, your job is to defend it. When you're facilitating, your job is to guide the discussion and help the group reach a decision. Most people try to do both, and that's where things go sideways.

**The 4 types of design reviews:**

1. **Requirements DR** (60-90 min): Validate we're solving the right problem before any design work
2. **Preliminary DR** (90-120 min): Validate high-level architecture and technology choices
3. **Detailed DR** (2-3 hours): Validate implementation details, data models, APIs, edge cases
4. **Final DR** (60-90 min): Validate production readiness before deployment

High-risk projects need all 4. Medium-risk projects need 2-3. Low-risk projects need 1. The key is matching the review process to the risk.

**The 5 patterns that kill design reviews:**

1. **Bikeshedding**: 45 minutes on variable naming, 5 minutes on database architecture
2. **Loud voices**: Principal engineer dominates, juniors stay quiet even when they have valid concerns
3. **Analysis paralysis**: "Let's evaluate 5 more options" (spoiler: you never decide)
4. **Design by committee**: Everyone compromises, nobody's happy with the Frankenstein result
5. **Missing context**: Reviewers suggest things that were already tried and failed

**How to facilitate disagreements:**

This is the hard part. Two senior engineers disagree. Both have valid points. How do you facilitate without picking a side?

- Stay neutral (even if you have an opinion)
- Structure the debate: "Let's hear both perspectives fully before discussing"
- Find common ground: "What do we agree on?"
- Focus on tradeoffs, not right vs wrong
- Know when to escalate (and when not to)

**Decision frameworks:**

- **Consensus**: Everyone agrees (rare, slow, often impossible)
- **Consent**: No blocking objections (more practical)
- **DACI**: Driver, Approver, Contributors, Informed (clear roles)

Most design reviews work best with consent. You're not trying to make everyone happy—you're trying to make a decision that no one finds unacceptable.

**The hardest scenario:** When you're BOTH presenter and facilitator.

You're presenting YOUR design AND running the review. It's like being both player and referee.

Solution: Explicitly separate the roles. "I'm in facilitator mode now. I want to hear all concerns." Then switch back when needed: "Let me switch to presenter mode to explain why we chose PostgreSQL..."

It feels awkward at first, but it works.

**Document everything:**

Use ADRs (Architecture Decision Records):
- What was decided
- Why (the reasoning)
- Alternatives rejected
- Consequences (good and bad)

Send follow-up within 24 hours or decisions evaporate.

**Real example:** I facilitated a 90-minute microservices migration review. We made 3 decisions (service boundaries, distributed transactions, migration strategy), everyone contributed including the junior engineer, and I documented everything in ADRs within 24 hours. That's what good facilitation looks like.

I wrote up the full playbook with examples, checklists, and techniques: [LINK]

What's your biggest challenge with design reviews? I'd love to hear what's worked (or hasn't worked) for you.

---

## r/softwarearchitecture

**Title:** The Design Review Playbook: Requirements DR, Preliminary DR, Detailed DR, Final DR

**Post:**

After facilitating 100+ design reviews, I've noticed most teams either over-review (wasting time) or under-review (creating production incidents).

The solution: Match the review process to the risk.

**The 4 types of design reviews:**

**1. Requirements DR (60-90 min)**
- When: Before any design work
- Purpose: Validate we're solving the right problem
- Attendees: Product, tech leads, stakeholders
- Key questions: What problem? What constraints? What's out of scope?
- Skip for: Small features, well-understood problems

**2. Preliminary DR (90-120 min)**
- When: After requirements validated
- Purpose: Validate high-level architecture
- Attendees: Engineering team, architects, senior engineers
- Key questions: Right architecture? Right technologies? Major risks?
- Skip for: Incremental features within existing architecture

**3. Detailed DR (2-3 hours)**
- When: Before implementation
- Purpose: Validate detailed design
- Attendees: Engineering team implementing the feature
- Key questions: Data models? APIs? Error handling? Edge cases?
- Skip for: Prototypes, exploratory work

**4. Final DR (60-90 min)**
- When: Before production deployment
- Purpose: Validate production readiness
- Attendees: Engineering, SRE, security
- Key questions: Monitoring? Rollback plan? Load testing? Runbooks?
- Skip for: Internal tools, low-risk features

**Choosing the right reviews:**

- **High-risk** (new systems, major architecture changes): All 4 reviews
- **Medium-risk** (new features, significant refactoring): 2-3 reviews
- **Low-risk** (incremental features, bug fixes): 1 review
- **Prototypes**: 0-1 review

Real example: Building a new payment processing system? All 4 reviews. Adding a new API endpoint? Just Detailed DR or Final DR.

I also cover facilitation techniques, decision frameworks, and how to handle disagreements in the full article: [LINK]

Do you use a similar review structure? What works for your team?

---

## r/programming

**Title:** Design reviews fail when there's no facilitator, only advocates

**Post:**

I just watched a 2-hour design review end with "let's schedule a follow-up to continue the discussion."

No decisions made. No progress. Just 12 person-hours wasted ($1,800 at $150/hour fully-loaded cost).

The problem? Two senior engineers spent 30 minutes arguing about MongoDB vs PostgreSQL. Nobody was facilitating. Everyone was advocating.

After facilitating 100+ design reviews, I've seen this pattern repeatedly. Here's what actually works:

**Facilitating ≠ Presenting**

- Presenter: Defend your design, convince others
- Facilitator: Guide discussion, help group decide

Most people try to do both. That's the problem.

**The 5 patterns that kill reviews:**

1. Bikeshedding (45 min on naming, 5 min on architecture)
2. Loud voices (hierarchy kills honest feedback)
3. Analysis paralysis ("let's evaluate 5 more options")
4. Design by committee (Frankenstein compromises)
5. Missing context (reviewers don't have full picture)

**How to facilitate:**

- Set the stage (clear objectives, ground rules, decision process)
- Stay neutral (even if you have an opinion)
- Draw out quiet participants
- Time-box discussions
- Use parking lot for tangents
- Drive to decisions (don't end with "let's think about it")
- Document in ADRs within 24 hours

**Decision frameworks:**

- Consensus: Everyone agrees (rare, slow)
- Consent: No blocking objections (practical)
- DACI: Clear roles (use for high-stakes)

Most reviews work best with consent.

Full playbook with examples: [LINK]

What's your experience with design reviews?

---

## Subreddit Selection

**Primary targets:**
- r/ExperiencedDevs (most relevant, high engagement)
- r/softwarearchitecture (architecture focus)
- r/programming (broader audience)

**Secondary targets:**
- r/cscareerquestions (career development angle)
- r/TechLead (leadership focus)
- r/ExperiencedDevs (weekly discussion threads)

