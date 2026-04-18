# Threads Post - Design Review Playbook

## Main Post

Your 2-hour design review just wasted $1,800 and made zero decisions.

The problem? No facilitator. Just advocates arguing.

After facilitating 100+ design reviews, here's what works:

🎯 4 types of design reviews (Requirements, Preliminary, Detailed, Final) - match to risk
🛑 5 patterns that kill reviews (bikeshedding, loud voices, analysis paralysis, design by committee, missing context)
⚖️ How to stay neutral when senior engineers disagree
📋 Decision frameworks that work (consent > consensus > DACI)

The hardest part? Being BOTH presenter and facilitator.

Solution: Explicitly separate the roles. "I'm in facilitator mode now."

Full playbook with examples and checklists: [LINK]

What's your biggest design review challenge?

---

## Thread Version

Your design review just turned into a 2-hour MongoDB vs PostgreSQL debate.

No decisions made. Everyone's frustrated. The junior engineer is just sitting there watching two senior engineers argue.

Nobody is facilitating. Everyone is advocating.

🧵 Here's what I learned facilitating 100+ design reviews:

---

First, understand the difference:

Presenter = Advocate for your solution
Facilitator = Guide the process, stay neutral

Most people try to do both. That's the problem.

When you're facilitating, you want a GOOD decision, not YOUR decision.

---

The 4 types of design reviews:

1️⃣ Requirements DR (60-90 min)
Validate the problem before design work
Skip for: Small features, well-understood problems

2️⃣ Preliminary DR (90-120 min)
Validate high-level architecture
Skip for: Incremental features

---

3️⃣ Detailed DR (2-3 hours)
Validate implementation details
Skip for: Prototypes

4️⃣ Final DR (60-90 min)
Validate production readiness
Skip for: Internal tools, low-risk features

High-risk projects need all 4. Low-risk projects need 1.

---

The 5 patterns that kill design reviews:

1. Bikeshedding
45 min on variable naming, 5 min on database architecture

2. Loud voices
Principal engineer dominates, juniors stay quiet

3. Analysis paralysis
"Let's evaluate 5 more options" (you never decide)

---

4. Design by committee
Everyone compromises, nobody's happy with the Frankenstein result

5. Missing context
Reviewers suggest things already tried and failed

Recognize these patterns? You can stop them.

---

How to facilitate disagreements:

Two senior engineers disagree. Both have valid points. How do you facilitate without picking a side?

• Stay neutral (even if you have an opinion)
• Structure the debate: "Let's hear both perspectives fully"
• Find common ground: "What do we agree on?"

---

• Focus on tradeoffs, not right vs wrong
• Know when to escalate (and when not to)

Most technical decisions are about tradeoffs, not absolutes.

Make it about evaluating options, not winning arguments.

---

Decision frameworks:

Consensus = Everyone agrees (rare, slow)
Consent = No blocking objections (practical)
DACI = Clear roles (Driver, Approver, Contributors, Informed)

Most design reviews work best with consent.

You're not trying to make everyone happy—you're trying to make a decision no one finds unacceptable.

---

The hardest scenario:

You're BOTH presenter and facilitator. You're presenting YOUR design AND running the review.

It's like being both player and referee.

Solution: Explicitly separate the roles.

"I'm in facilitator mode now. I want to hear all concerns."

---

Then switch back when needed:

"Let me switch to presenter mode for a moment to explain why we chose PostgreSQL..."

It feels awkward at first, but it works.

The key is making the role switch visible and explicit.

---

Document everything in ADRs (Architecture Decision Records):

• What was decided
• Why (the reasoning)
• Alternatives rejected
• Consequences (good and bad)

Send follow-up within 24 hours or decisions evaporate.

---

Real example:

90-minute microservices review
• Made 3 decisions (service boundaries, distributed transactions, migration strategy)
• Everyone contributed (including junior engineer)
• Documented in ADRs within 24 hours

That's what good facilitation looks like.

---

Key takeaway:

Facilitating ≠ Presenting

You're guiding the process, not advocating for an outcome.

Full playbook with examples, checklists, and techniques: [LINK]

What's your biggest design review challenge?

---

## Short Versions

**Version 1 (concise):**
Design reviews fail when there's no facilitator, only advocates.

After facilitating 100+ reviews:
• 4 types of DRs (match to risk)
• 5 patterns that kill reviews
• How to stay neutral
• Decision frameworks that work

Full playbook: [LINK]

**Version 2 (problem-focused):**
Your 2-hour design review:
• $1,800 wasted
• Zero decisions made
• Everyone frustrated

The problem? No facilitator.

Here's what works: [LINK]

**Version 3 (stat-focused):**
I've facilitated 100+ design reviews across fintech, healthcare, and e-commerce.

The pattern is clear: Reviews fail when there's no facilitator.

Here's the playbook: [LINK]

---

## Engagement Prompts

- What's the worst design review you've been in?
- How do you handle disagreements between senior engineers?
- Do you use Requirements/Preliminary/Detailed/Final DRs?
- What's your go-to decision framework?
- Ever been both presenter and facilitator? How did you handle it?

