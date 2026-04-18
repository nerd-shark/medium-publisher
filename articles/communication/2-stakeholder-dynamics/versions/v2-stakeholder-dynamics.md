---
document-title: Communication Series
document-subtitle: Navigating Executive Disagreement
document-type: Medium Article Draft
document-date: 2025-02-17
document-revision: 3.0
document-author: Daniel Stauffer
author-email: daniel_stauffer@jabil.com
author-org: Enterprise Architecture
review-cycle: Per Article
changes-from-v2: Updated case study to reflect actual ESG optimization experience from previous company
---
# When Executives Disagree in Front of You: A Technical Guide to Stakeholder Dynamics

Part 2 of my series on Technical Communication. Last time, we explored speaking executive — the foundational principles of C-suite communication. This time: navigating stakeholder dynamics when executives disagree in front of you. Follow along for more deep dives into technical leadership communication.

---

You're 10 minutes into your chaos engineering presentation. You've done everything right—started with business impact, kept it high-level, used the Pyramid Principle from Part 1.

Then the CTO interrupts: "This is exactly what we need. Netflix does this. We should start running chaos experiments in production next week."

The VP of Operations jumps in: "Absolutely not. You want to break production ON PURPOSE? That's insane. We're not Netflix."

The VP of Product leans forward: "I don't care what we do, but if you cause an outage during peak season, we're losing millions. Can you guarantee that won't happen?"

All three are now looking at you. Waiting.

Welcome to the hardest part of technical leadership: navigating stakeholder dynamics when executives disagree.

Here's what most engineers do wrong: They try to solve the technical problem. They explain why chaos engineering works, or how they'll control the blast radius, or why Netflix's approach is proven.

But here's the truth: **It's not about your proposal. It's about alignment.**

When executives disagree in front of you, your job isn't to pick a side. Your job is to facilitate a conversation that gets everyone to the same place.

## Reading the Room: The Five Stakeholder Types

Before we talk about strategies, you need to understand who's in the room.

### The Decision Maker

This person has final say. Often the most senior person, but not always. They might stay quiet and let others debate, then make the call at the end.

**How to identify**: Watch who others defer to. Listen for "What do you think?" directed at them.

### The Influencer

This person shapes opinions. They don't have final authority, but the Decision Maker listens to them. Often a trusted advisor or domain expert.

**How to identify**: The Decision Maker asks them questions. Others reference their opinions.

### The Blocker

This person can veto your proposal. They might not have final say, but they have enough power to stop things. Often controls budget, resources, or compliance.

**How to identify**: They use words like "we can't," "that won't work," "I won't approve."

### The Champion

This person supports your proposal. They'll advocate for you, even when you're not in the room. Gold.

**How to identify**: They defend your proposal, ask supportive questions, build on your ideas.

### The Skeptic

This person questions everything. Not necessarily opposed, but needs convincing. Often asks the hardest questions.

**How to identify**: "What about...?" "Have you considered...?" "How do you know...?"

In our chaos engineering scenario:

- **CTO**: Champion (excited about the idea)
- **VP Operations**: Blocker (can veto on stability grounds)
- **VP Product**: Skeptic (needs proof it won't hurt customers)

## The 8 Core Strategies for Navigating Disagreement

When executives clash in front of you, most engineers freeze or pick a side. Neither works. What you need is a playbook—specific strategies you can deploy in the moment to turn conflict into alignment. These eight strategies have saved me in countless high-stakes meetings, and they'll work for you too.

### Strategy 1: The Neutral Facilitator

The moment executives start disagreeing, you'll feel pressure to take a side. Resist it. Your power comes from staying neutral and helping everyone find common ground. The second you become an advocate, you lose half the room.

When executives disagree, your instinct is to pick a side. Don't.

**Wrong**: "I agree with the CTO—chaos engineering is clearly the right approach. Netflix proved it works."

**Right**: "I'm hearing three important concerns: improving our resilience, protecting production stability, and ensuring zero customer impact. Let me see if I can address all three."

**Why this works**: Picking a side makes you an advocate, not a facilitator. Advocates have enemies. Facilitators have stakeholders.

**The technique**: Use "What I'm hearing is..." to reflect back concerns without judgment.

### Strategy 2: Acknowledge All Concerns Explicitly

People need to feel heard before they'll compromise. A simple nod isn't enough—you need to verbalize each person's concern out loud. This single technique defuses more tension than anything else in your toolkit.

Don't just nod. Say it out loud.

**The script**:

- "CTO, you want to adopt chaos engineering to improve our resilience and find weaknesses before they cause real incidents."
- "VP Operations, you're concerned about intentionally breaking production and risking stability."
- "VP Product, you need absolute certainty that we won't cause customer-facing outages, especially during peak season."

**Why this works**: Acknowledgment ≠ agreement, but it shows you heard them. People who feel heard are more willing to compromise.

**The mistake**: Ignoring concerns or dismissing them as "not technical." Every concern is valid to the person raising it.

### Strategy 3: Find the Common Ground

Executives rarely disagree on the goal—they disagree on the path. Your job is to identify what everyone actually wants (not what they're arguing about) and reframe the conversation around that shared objective.

What do all stakeholders actually want? Usually, it's not what they're arguing about.

**In our scenario**:

- CTO wants: Better resilience and fewer production incidents
- VP Operations wants: Production stability and no outages
- VP Product wants: Zero customer impact

**The common ground**: "We all want to improve system reliability without risking customer experience."

**The reframe**: "Let me propose a phased approach that improves resilience, maintains stability, and protects customers..."

**Why this works**: You've shifted from "who's right?" to "how do we achieve our shared goal?"

### Strategy 4: Ask Clarifying Questions

The stated objection is rarely the real objection. Someone says "we need six months of testing" when they really mean "I'm scared of another outage." Ask questions that get to the underlying concern, not the surface-level demand.

Often, the stated concern isn't the real concern.

**VP Operations says**: "We can't break production on purpose."

**You ask**: "Help me understand—what's the specific risk you're worried about?"

**VP Operations reveals**: "Last year we had a deployment that took down the entire site for 4 hours. I can't let that happen again."

**Aha**: The real concern isn't "chaos engineering is bad"—it's "we've been burned before and I need proof this is safe." Now you can address the actual problem.

**Questions that reveal truth**:

- "What would success look like for you?"
- "What's the worst-case scenario you're worried about?"
- "What would need to be true for you to feel comfortable?"
- "Help me understand your concern about..."

### Strategy 5: The Offline Alignment

Some disagreements are too heated to resolve in the room. When emotions run high or positions are entrenched, the smartest move is to retreat, meet with stakeholders individually, and build consensus offline before reconvening.

Sometimes, disagreements are too heated to resolve in the room.

**The retreat**: "I'm hearing strong opinions on all sides. Let me take this feedback, explore some options, and come back with a proposal that addresses everyone's concerns."

**Then**: Meet with each stakeholder individually. Understand their real concerns. Build consensus offline.

**Why this works**: People are more honest one-on-one. They'll tell you what they really care about without posturing for the group.

**The follow-up**:

- Meet with VP Operations: "What safety controls would make you comfortable with chaos experiments?"
- Meet with VP Product: "What's the maximum customer impact you can accept during experiments?"
- Meet with CTO: "Which resilience improvements are must-haves vs nice-to-haves?"

**The result**: You come back with a proposal that already has buy-in from each stakeholder.

### Strategy 6: Leverage Your Champion

You don't have to fight every battle alone. If you have a Champion in the room—someone with political capital who supports your proposal—use them strategically. They can say things you can't and advocate when you need to stay neutral.

If you have a Champion in the room, use them.

**Before the meeting**: "CTO, I know you support chaos engineering. If there's pushback on the approach, would you be willing to speak to the benefits you've seen at other companies?"

**In the meeting**: When VP Operations pushes back, the CTO (your Champion) says: "I understand the stability concern. But the reason Netflix has 99.99% uptime is BECAUSE they do chaos engineering, not in spite of it. They find problems before they become incidents."

**Why this works**: Champions have political capital you don't. They can say things you can't. They can advocate when you need to stay neutral.

**The mistake**: Expecting your Champion to do all the work. You still need to facilitate.

### Strategy 7: The "Parking Lot" Technique

Meetings derail when someone raises a tangential issue that sparks a new debate. Don't let it happen. Acknowledge the concern, promise to address it later, and steer back to the main topic. Then actually follow up.

Meetings derail when people debate tangential issues.

**VP Product**: "While we're talking about resilience, we should also discuss our disaster recovery strategy."

**You**: "That's important, and I want to make sure we give it proper attention. Can we park that for now and discuss it after we align on the chaos engineering approach?"

**Why this works**: You've acknowledged the concern without letting it derail the meeting. You'll follow up later.

**The follow-up**: Actually discuss the parked item later. Don't let it disappear.

### Strategy 8: Know When to Retreat

Not every disagreement can be resolved in one meeting. Sometimes pushing for a decision makes things worse. Learn to recognize when you're losing the room and have the courage to retreat, regroup, and come back with a better approach.

Some disagreements can't be resolved in one meeting. Recognize when you're making it worse.

**Signs you should retreat**:

- Voices are raised
- People are repeating themselves
- Body language is closed (crossed arms, looking away)
- The Decision Maker looks frustrated
- You're going in circles

**The retreat**: "I'm hearing that we need more time to align on this. Let me take the feedback, explore some options, and schedule a follow-up."

**Why this works**: Strategic patience beats forcing a decision. Bad decisions made under pressure are worse than delayed decisions.

## Stakeholder Mapping: Do Your Homework

Before you walk into a multi-stakeholder meeting, map your stakeholders.

**Template**:

| Stakeholder   | Role       | Primary Concern        | Success Metric       | Likely Objection          | Ally or Blocker? |
| ------------- | ---------- | ---------------------- | -------------------- | ------------------------- | ---------------- |
| CTO           | Champion   | Resilience improvement | Fewer incidents      | None expected             | Ally             |
| VP Operations | Blocker    | Production stability   | Zero outages         | Risk of chaos experiments | Blocker          |
| VP Product    | Skeptic    | Customer experience    | Zero customer impact | Timeline concerns         | Neutral          |
| Director SRE  | Influencer | Operational excellence | MTTR reduction       | Resource constraints      | Ally             |

**How to use this**:

1. **Identify concerns**: Prepare responses for each stakeholder's primary concern
2. **Anticipate objections**: Have answers ready
3. **Leverage allies**: Ask Champions to advocate for specific points
4. **Address blockers**: Meet with Blockers before the meeting to understand concerns

## Real-World Example: The Chaos Engineering Resolution

Let's go back to our scenario. Here's how it actually played out when I published the chaos engineering article.

**In the meeting**:

- I acknowledged all three concerns explicitly
- I asked clarifying questions to understand the real issues
- I found common ground: "We all want better reliability without risking customers"
- I proposed a phased approach:
  - **Phase 1**: Chaos experiments in non-production environments only (prove the concept)
  - **Phase 2**: Tiny production experiments during off-peak hours with 1% traffic (minimal risk)
  - **Phase 3**: Scheduled "game days" with full team monitoring and kill switches (controlled chaos)
  - **Phase 4**: Automated chaos experiments with blast radius controls (mature program)

**The result**:

- CTO got chaos engineering adoption (resilience improvement)
- VP Operations got safety controls and gradual rollout (stability protection)
- VP Product got customer impact guarantees (1% blast radius, off-peak timing)

**The lesson**: Nobody got exactly what they wanted, but everyone got what they needed.

**The proof**: The article I published about this approach got picked up by the engineering community because it addressed the exact concerns every organization has about chaos engineering.

## Politics vs Effectiveness: A Reframe

Most engineers hate "politics." They see it as manipulation, ass-kissing, or playing games.

But here's a better way to think about it: **Political skills are effectiveness skills at scale.**

When you're a junior engineer, effectiveness is writing good code. When you're a senior engineer, effectiveness is getting things done through people who disagree.

Understanding stakeholder dynamics isn't manipulation—it's facilitation. It's helping people with different priorities find common ground.

The best technical leaders aren't the ones with the best technical ideas. They're the ones who can get diverse stakeholders aligned on a path forward.

## What's Next

In Part 3, we'll cover **The Technical Presentation Playbook: Tailoring Your Message to Every Audience**.

We'll dive into:

- Adapting presentations for executives, stakeholders, and technical peers
- The complete demo playbook (executive, stakeholder, technical)
- Handling mixed audiences (when everyone's in the room)
- Architecture review presentation strategies

Navigating stakeholder dynamics is one skill. Adapting your presentation style to any audience is another. Together, they make you unstoppable.

## The Bottom Line

When executives disagree in front of you, it's not about your proposal—it's about alignment.

Stay neutral. Acknowledge all concerns. Find common ground. Ask clarifying questions. Retreat when needed. Leverage your champions. Park tangents. Know when to regroup.

These aren't political games. They're facilitation skills. And they're the difference between proposals that get approved and proposals that die in committee.

**Question for you**: What's the most challenging stakeholder conflict you've faced? How did you navigate it? What would you do differently now?

---

## Series Navigation

**Previous Article**: [Speaking Executive: A Technical Guide to C-Suite Communication](link-to-part-1)

**Next Article**: [The Technical Presentation Playbook: Tailoring to Every Audience](link) *(Coming soon!)*

**Coming Up**: Architecture reviews, design reviews, technical writing, technical debt

---

*Daniel Stauffer is an Enterprise Architect specializing in technical communication and stakeholder management. This is Part 2 of the Communication series. Read [Part 1: Speaking Executive](#) for the foundation of executive communication.*

**Tags**: #TechnicalLeadership #StakeholderManagement #ExecutiveCommunication #EngineeringLeadership #SoftwareArchitecture #PoliticalSkills

---

**Word Count**: ~2,000 words | **Reading Time**: ~7 minutes
