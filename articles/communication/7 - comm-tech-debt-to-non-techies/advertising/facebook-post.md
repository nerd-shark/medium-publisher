# Facebook Post

**Article**: Communicating Technical Debt to Non-Technical Stakeholders
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

Watched this happen at a fintech company I was working with last year.

18 months earlier, the team was a shipping machine. New API endpoint? Three days. UI change? One day. Sprint velocity was consistently around 45 story points. Product loved them.

By the time I got involved, the same endpoint took two weeks. Velocity had dropped to 28 points per sprint — same team, same people, same hours. The VP of Product was in the engineering manager's office every other day: "Why is everything taking so long?"

The EM kept asking for more headcount. They didn't need more people. They needed about six weeks to pay down the technical debt that had been piling up. But every time someone brought up refactoring, the conversation went nowhere.

"Technical debt" meant nothing to the business side. "Refactoring" sounded like "we want to rewrite things for fun." "Code quality" sounded like gold-plating.

The engineers weren't wrong about the problem. They were describing it in a language their stakeholders didn't speak.

**What finally worked — and I've used this at three companies now:**

"Remember when we took a shortcut on the payment module to hit the Q3 deadline? Saved us about two weeks. Good call at the time. But since then, every feature that touches payments takes an extra three days because engineers have to work around that shortcut. We've shipped 14 payment features since Q3. That's 42 extra engineering days — roughly $84,000 in engineering time."

"We're paying $84,000 in interest on a $20,000 loan. It's time to pay it off."

The VP's expression changed. He got it immediately. Not because I explained the code. Because I explained the money.

**Back it up with real data from your own tools:**

Velocity: 45 story points/sprint in Q1 → 28 in Q4. Same team, 38% less output. Plot the trendline.

Bug rate: 3 bugs per feature in Q1 → 7 in Q4. Each costs about 6 hours to fix.

Incidents: 2 per month in January → 8 in October. Average revenue impact: $12K per incident.

Real data from your own systems hits completely different than industry benchmarks.

**Frame as ROI, not cleanup:**

"6-week investment: $120K in engineering time. Expected return: 40% faster feature delivery, 60% fewer bugs. Recovered capacity: $200K/year. Payback period: 4 months."

Don't ask for permission to refactor. Ask for investment in velocity.

**The 20% allocation** is the sweet spot. 20% of each sprint for debt paydown. Small enough that features keep shipping. Big enough to make real progress. Sustainable indefinitely.

And celebrate wins loudly. "Refactored payment module. Feature delivery: 14 days → 5 days. Bugs: 7/feature → 2." Visible results build trust. Trust gets you more time.

Full guide with quantification techniques and prioritization frameworks:

[ARTICLE URL]

Part 7 of my Technical Communication series.

#TechnicalDebt #EngineeringLeadership #TechnicalCommunication #Refactoring #SoftwareEngineering #CodeQuality #TechLeadership #StakeholderManagement

---

**Character count**: ~2,500
**Hashtags**: 8
