---
title: "Communicating Technical Debt to Non-Technical Stakeholders"
subtitle: "Your codebase is rotting. Your velocity is dropping. Your stakeholders think you're just slow. Here's how to make invisible work visible."
series: "Technical Communication Part 7"
reading-time: "9 minutes"
target-audience: "Engineers, tech leads, engineering managers advocating for refactoring"
keywords: "technical debt, refactoring, business case, engineering leadership, stakeholder communication, velocity, code quality"
tags: "Technical Communication, Engineering Leadership, Technical Debt, Refactoring, Stakeholder Management"
status: "v4-publishable"
created: "2026-03-29"
updated: "2026-03-31"
author: "Daniel Stauffer"
changes-from-v3: "Publishable polish pass. Tightened prose throughout, refined section transitions, added nuance to prioritization and business case sections, sharpened closing, verified subtitle punch."
---

# Communicating Technical Debt to Non-Technical Stakeholders

Part 7 of my series on Technical Communication. Last time, we explored [writing technical documents that non-technical people actually read](link) — layered documents, executive summaries, and the inverted pyramid. This time: the hardest communication challenge in engineering. Making invisible work visible, and convincing people who can't see the problem to fund the fix. Follow along for more deep dives into communicating technical work effectively.

## The Velocity Death Spiral

I watched this happen to a team I was working with at a fintech company in 2024. Eighteen months earlier, they were shipping machines. New API endpoint? Three days. UI change? One day. Sprint velocity was consistently around 45 story points. Product loved them.

By the time I got involved, the same API endpoint took two weeks. Same UI change, four days. Velocity had dropped to 28 points per sprint — same team, same people, same hours. The VP of Product was in the engineering manager's office every other day asking "why is everything taking so long?" The engineering manager kept saying they needed more headcount. HR started a recruiting pipeline.

They didn't need more people. They needed about six weeks to pay down the technical debt that had been accumulating for a year and a half. But every time someone brought up refactoring, the conversation stalled. "Technical debt" meant nothing to the business side. "Refactoring" sounded like "we want to rewrite things for fun instead of building features." "Code quality" sounded like gold-plating.

The engineers weren't wrong about the problem. They were describing it in a language their stakeholders didn't speak. Technical debt isn't a technical problem — it's a business risk. Until you frame it that way, you'll keep losing the argument.

## The Interest Payment Metaphor

The metaphor that finally landed — and I've used it at three different companies since — is the one Ward Cunningham originally intended: financial debt. Not because it's clever, but because the people controlling your budget already think in these terms.

Here's how I pitched it to that fintech VP of Product: "Remember when we took a shortcut on the payment processing module to hit the Q3 deadline? That saved us about two weeks. Good call at the time. But since then, every feature that touches payments takes an extra three days because engineers have to work around that shortcut. We've shipped 14 payment features since Q3. That's 42 extra engineering days — roughly $84,000 in engineering time — spent working around a shortcut that saved us 10 days."

I watched his expression change. Then I said: "We're paying $84,000 in interest on a $20,000 loan. It's time to pay it off."

He got it immediately. Not because I explained the code. Because I explained the money.

The compound interest angle makes it even more pressing. "Every new feature we build on top of this shortcut adds more interest. The payment module touches 30% of our codebase now. If we don't address it this quarter, the interest payment grows from $84,000 to roughly $200,000 over the next year. And that's a conservative estimate."

## Quantifying the Cost of Inaction

Metaphors open the door. Numbers close the deal. You need concrete data showing what technical debt is actually costing the business right now — not in theory, but in dollars and lost capacity.

Velocity trends are the most visible metric. Track story points per sprint over the last 6-12 months. If velocity is declining while team size stays constant, something is consuming engineering capacity that isn't feature work. Plot it on a chart. Show the trendline. "We delivered 45 story points per sprint in Q1. We're delivering 28 in Q4. Same team, same hours, 38% less output. Here's where the time is going."

Bug rate trends tell a compelling story. Track bugs per feature over time. If the bug rate is climbing, it means the codebase is getting harder to change safely. "We shipped 3 bugs per feature in Q1. We're shipping 7 per feature in Q4. Each bug costs an average of 4 engineering hours to fix plus 2 hours of QA time. That's 24 extra hours per feature just in bug fixing."

Incident frequency connects directly to revenue. Track production incidents per month and their business impact. "We had 2 production incidents in January. We had 8 in October. Average incident duration: 45 minutes. Average revenue impact: $12,000 per incident. That's $96,000 in October alone — up from $24,000 in January."

Developer time on workarounds is the hidden cost most teams overlook. Survey your team: "What percentage of your time is spent working around existing code rather than building new functionality?" The answer is usually 30-50% for teams carrying significant technical debt. "Our engineers spend 40% of their time working around existing code. That's 4 out of 10 engineers effectively doing maintenance instead of building features. At our fully-loaded engineering cost, that's $480,000 per year in workaround time."

These numbers aren't estimates — they're measurements. Pull them from your project management tool, your incident tracker, and your bug database. Real data from your own systems is far more persuasive than industry benchmarks or gut feelings.

## Visualizing the Invisible

Data tells the story. Visuals make it land.

A velocity trend chart with a declining trendline is the single most effective visual for communicating technical debt to non-engineers. Plot story points per sprint over 12 months. Add a trendline. The downward slope is hard to argue with. Label the inflection points: "Shipped payment shortcut here. Velocity started declining here."

A heat map of code complexity shows where the debt lives. Tools like CodeClimate, SonarQube, or even simple cyclomatic complexity analysis can generate heat maps showing which parts of the codebase are most complex and most frequently changed. Red zones are where debt is highest and where it hurts most.

A before/after comparison shows what paydown actually looks like in practice. "After refactoring the payment module last quarter, feature delivery time for payment features dropped from 14 days to 5 days. Bug rate dropped from 7 per feature to 2. Here's the chart." If you've done any debt paydown before, this is your strongest evidence.

A cost projection chart shows the future. "At current trajectory, engineering velocity will decline another 20% by Q3. Here's what that means in features not shipped and revenue not earned." Project the cost of inaction forward 6-12 months. Make the future cost visible today — because by the time stakeholders feel it, you've already lost months.

## Building the Business Case

The business case for technical debt paydown follows the same structure as any investment proposal: cost of the investment, expected return, timeline, and risk of not investing. The framing matters more than the content.

Frame it as ROI, not as cleanup. "We're proposing a 6-week investment in the payment processing module. Cost: $120,000 in engineering time (3 engineers × 6 weeks). Expected return: 40% faster feature delivery for all payment features, 60% fewer payment-related bugs, $200,000/year in recovered engineering capacity. Payback period: 4 months."

Compare the cost of action vs. inaction side by side. "Option A: Invest $120,000 now, recover $200,000/year in engineering capacity. Option B: Do nothing, lose an additional $200,000/year in engineering capacity and accept increasing bug rates and incident frequency. Over 2 years, Option A saves $280,000. Option B costs $400,000." When you lay it out like that, the decision becomes obvious — which is the point.

Propose incremental paydown, not a big-bang rewrite. Stakeholders are terrified of "we need to stop features for 3 months to refactor." Instead: "We'll dedicate 20% of each sprint to debt paydown — roughly 1 engineer per sprint. Features continue shipping. Velocity improves gradually. We'll show measurable improvement within 6 weeks."

The 20% allocation tends to be the sweet spot for most teams. It's small enough that stakeholders don't feel like features are being sacrificed. It's large enough to make meaningful progress. And it's sustainable — you can maintain it quarter after quarter rather than doing a burst of refactoring followed by months of neglect.

## Prioritization: What to Fix First

You can't fix everything at once, and you shouldn't try. Prioritize using two dimensions: pain (how much is this costing us?) and effort (how hard is it to fix?).

High pain, low effort — fix these immediately. These are the quick wins that build credibility with stakeholders and give your team early momentum. A missing database index that causes slow queries. A hardcoded configuration that requires a deployment to change. A duplicated function that causes bugs when one copy is updated but not the other.

High pain, high effort — plan these as projects. These are the strategic investments that need their own timelines and resourcing. The monolithic module that needs to be split. The database schema that needs migration. The authentication system that needs replacement.

Low pain, low effort — fix these opportunistically. When you're already working in that area of the code, clean it up. The boy scout rule: leave the code better than you found it. No special allocation needed.

Low pain, high effort — don't fix these. Some technical debt isn't worth paying down. If a messy module works, rarely changes, and doesn't cause bugs, leave it alone. Spending three weeks refactoring something that costs you an hour a quarter is a bad trade. Your time is better spent elsewhere.

The key insight here is that prioritization is a communication tool, too. When you show stakeholders that you're being selective — that you're not asking to rewrite everything, just the parts that are actively costing money — you build trust. It signals that you're thinking about this as a business decision, not an engineering vanity project.

## Celebrating Wins

The fastest way to lose stakeholder support for debt paydown is to do it silently. If nobody sees the improvement, nobody believes it happened.

After every debt paydown effort, measure and communicate the results. "We refactored the payment module over the last 6 weeks. Results: feature delivery time dropped from 14 days to 5 days. Bug rate dropped from 7 per feature to 2. Last month's payment features shipped 3 days ahead of schedule."

Show the velocity chart with the improvement. Show the bug rate chart with the decline. Show the incident frequency chart with the reduction. Make the invisible visible — not just the problem, but the solution.

This builds a virtuous cycle. Stakeholders see results, so they fund more paydown. More paydown improves velocity. Improved velocity builds trust. Trust enables more investment. The team that communicates debt paydown results effectively earns more time to pay down debt. The team that does it silently gets asked why features are late.

## What to Do Monday Morning

Start with measurement. Pull your velocity data for the last 12 months. Pull your bug rates. Pull your incident frequency. Plot the trends. If the trends are declining, you have a story to tell.

Then have one conversation. Pick the stakeholder who's most frustrated with engineering speed. Show them the velocity chart. Use the interest payment metaphor. Quantify the cost. Propose 20% sprint allocation for debt paydown. Offer to show measurable improvement in 6 weeks.

Don't ask for permission to refactor. Ask for investment in engineering velocity. Don't describe the technical problem. Describe the business impact. Don't propose a rewrite. Propose incremental improvement with measurable results.

Technical debt is invisible to everyone except the engineers who work in it every day. Your job isn't to fix it in silence — it's to make it visible, quantify its cost, and build the case for paying it down. The stakeholders aren't the enemy. They just can't see what you see. Show them.

---

**Resources**:
- [Ward Cunningham: The WyCash Portfolio Management System (original technical debt metaphor)](http://wiki.c2.com/?WardExplainsDebtMetaphor)
- [Martin Fowler: Technical Debt Quadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html)
- [Google SRE Book: Eliminating Toil](https://sre.google/sre-book/eliminating-toil/)
- [CodeClimate: Code Quality Metrics](https://codeclimate.com/)
- [SonarQube: Continuous Code Quality](https://www.sonarqube.org/)

---

## Series Navigation

**Previous Article**: [Writing Technical Documents That Non-Technical People Actually Read](link) *(Part 6)*

**Next Article**: [Cross-Functional Communication: Engineering, Product, and Design](link) *(Part 8 — Series Finale, Coming soon!)*

**Coming Up**: The series finale — collaborating across disciplines with different languages and priorities

---

*This is Part 7 of the Technical Communication series. Read [Part 1: Speaking Executive](link), [Part 2: Navigating Executive Disagreement](link), [Part 3: The Technical Presentation Playbook](link), [Part 4: The Architecture Review Survival Guide](link), [Part 5: The Design Review Playbook](link), and [Part 6: Writing Technical Documents](link).*

**About the Author**: Daniel Stauffer is an Enterprise Architect who has successfully advocated for technical debt paydown across fintech, healthcare, and e-commerce organizations. He believes the best engineers are the ones who can explain why maintenance matters — in dollars, not jargon.

**Tags**: #TechnicalCommunication #EngineeringLeadership #TechnicalDebt #Refactoring #StakeholderManagement #SoftwareEngineering #CodeQuality #VelocityMetrics
