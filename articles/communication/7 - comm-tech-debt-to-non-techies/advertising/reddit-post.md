# Reddit Post

**Article**: Communicating Technical Debt to Non-Technical Stakeholders
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Suggested Subreddits
- r/ExperiencedDevs
- r/programming
- r/cscareerquestions
- r/softwarearchitecture
- r/engineering
- r/agile
- r/LeadDev

## Post Title
How I got stakeholders to fund technical debt paydown by talking about money instead of code

## Post Body

Every engineering team I've worked with has this same problem. Velocity is declining, stakeholders are frustrated, and nobody can get time for debt paydown. The conversation always goes:

Engineer: "We need to refactor the payment module."
Stakeholder: "We need features, not rewrites."

I watched this play out at a fintech company last year. Team went from 45 story points per sprint to 28 in 18 months. Same people, same hours. VP of Product was in the EM's office every other day asking why everything was slow. EM kept asking for more headcount.

They didn't need more people. They needed 6 weeks to pay down debt. But every time someone said "refactoring" the conversation died.

The problem isn't that stakeholders don't care. It's that we describe the problem in engineering terms and expect a business response.

**What worked for me: the interest payment metaphor**

Here's how I pitched it to the VP of Product: "Remember when we took a shortcut on the payment module to hit Q3? Saved us 2 weeks. Good call at the time. But since then, every feature that touches payments takes an extra 3 days. We've shipped 14 payment features. That's 42 extra engineering days — roughly $84,000."

"We're paying $84,000 in interest on a $20,000 loan. It's time to pay it off."

His expression changed. He got it immediately. Not because I explained the code. Because I explained the money.

**Quantifying with real data**

Metaphors open the door. Numbers close the deal. I pulled data from our own tools:

- **Velocity**: 45 story points/sprint in Q1 → 28 in Q4. Same team, 38% less output. Plotted on a chart with a trendline.
- **Bug rate**: 3 bugs/feature in Q1 → 7 in Q4. Each bug costs ~6 hours (engineering + QA).
- **Incidents**: 2/month in January → 8 in October. Average revenue impact: $12K/incident.
- **Workaround time**: Surveyed the team — 40% of time spent working around existing code rather than building new functionality.

Real data from your own systems is infinitely more persuasive than industry benchmarks.

**Framing as ROI**

Don't ask for permission to refactor. Ask for investment in velocity.

"6-week investment: $120K in engineering time (3 engineers × 6 weeks). Expected return: 40% faster feature delivery, 60% fewer bugs, $200K/year in recovered engineering capacity. Payback period: 4 months."

Compare cost of action vs inaction: "Option A: invest $120K now, recover $200K/year. Option B: do nothing, lose an additional $200K/year. Over 2 years, Option A saves $280K."

**The 20% allocation**

Don't propose "stop features for 3 months." Propose 20% of each sprint for debt paydown. Small enough that features keep shipping. Large enough to make meaningful progress. Sustainable indefinitely.

**Prioritization**

High pain + low effort = fix immediately (quick wins, build credibility)
High pain + high effort = plan as projects
Low pain + low effort = fix opportunistically (boy scout rule)
Low pain + high effort = don't fix (seriously, leave it alone)

**Celebrating wins**

After every paydown effort, measure and communicate: "Refactored payment module. Feature delivery: 14 days → 5 days. Bugs: 7/feature → 2/feature." Visible results → more funding → more paydown → better velocity → more trust.

The article covers the full playbook: interest payment metaphor, quantification techniques, visualization strategies (velocity charts, heat maps, cost projections), building the business case, prioritization frameworks, and celebrating wins.

[ARTICLE URL]

Part 7 of my Technical Communication series. Happy to discuss specific strategies for getting debt paydown funded.

---

**Format**: No hashtags, experience-driven, discussion-focused
