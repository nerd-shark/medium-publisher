# Incident Response: From Detection to Resolution in 10 Minutes

Part 8 of Resilience Engineering series. Previous articles covered patterns for preventing and containing failures. This one: what happens when the failure is already here and the clock is ticking.

## Opening Hook — The 3 AM Phone Call

- It's 3:07 AM. Phone buzzing. PagerDuty. "CRITICAL: Payment processing latency >10s"
- You're half asleep, fumbling for your laptop
- Slack is already on fire. 47 unread messages in #incidents
- Someone typed "is anyone looking at this?" 12 minutes ago
- Nobody responded. The alert fired 18 minutes ago. Customers have been failing for 18 minutes.
- The first 10 minutes of an incident determine whether it's a blip or a catastrophe
- Most teams waste those 10 minutes figuring out who's in charge and what to look at
- This article: how to not waste them

## The Incident Timeline (Why Speed Matters)

- MTTR is the metric that matters — Mean Time To Recovery
- Industry average MTTR: 197 minutes (almost 3.5 hours!) — that's from some study, need to find it
- Top-performing teams: under 60 minutes
- Elite teams (Google, Netflix): under 10 minutes for most incidents
- The cost curve is exponential, not linear
- First 5 minutes: maybe 100 users affected
- 15 minutes: 10,000 users, social media starts noticing
- 30 minutes: revenue impact measurable, executives asking questions
- 60 minutes: news articles, stock price impact for public companies
- Every minute of fumbling in the first 10 minutes costs you 10 minutes of total incident duration

## Severity Levels (Stop Arguing About This)

- Need a clear, pre-agreed severity framework
- SEV1: Revenue-impacting, customer-facing, widespread — all hands
- SEV2: Significant degradation, subset of customers — on-call team + leads
- SEV3: Minor impact, workaround available — on-call handles
- SEV4: No customer impact, internal only — next business day
- The key: severity determines the RESPONSE, not the root cause
- Don't waste time debating severity during the incident. Pick one. Adjust later if needed.

## The First 10 Minutes (The Playbook)

- Minute 0-1: Acknowledge the alert. Literally just say "I'm looking at this" in the channel
- Minute 1-3: Triage. What's broken? Who's affected? What changed recently?
- Minute 3-5: Declare incident. Assign roles: Incident Commander, Communications Lead, Technical Lead
- Minute 5-10: First mitigation attempt. Rollback? Feature flag? Scale up? Failover?
- The goal of the first 10 minutes is NOT to find root cause. It's to STOP THE BLEEDING.
- Root cause comes later. Mitigation comes now.

## Incident Commander (The Most Important Role)

- Not the most senior person. Not the best engineer. The best COORDINATOR.
- IC doesn't debug. IC coordinates.
- IC responsibilities: assign tasks, track progress, make decisions, communicate status
- The IC asks: "What do we know? What are we trying? When's the next update?"
- Anti-pattern: the IC starts debugging. Now nobody's coordinating.
- Anti-pattern: no IC declared. Everyone debugs independently. Duplicate work. Missed signals.

## Communication During Incidents

- Internal: status updates every 15 minutes minimum, even if "still investigating"
- External: status page update within 5 minutes of SEV1 declaration
- Executive: brief summary every 30 minutes for SEV1
- Template: "What's broken, who's affected, what we're doing, when's the next update"
- The worst thing you can say during an incident: nothing
- Silence breeds panic. Regular updates — even "no change" — reduce anxiety

## Runbooks (Your 3 AM Brain Can't Think)

- Pre-written, step-by-step procedures for common failure scenarios
- Your 3 AM brain is operating at maybe 60% capacity. Runbooks compensate.
- Good runbook: "If payment latency >5s, check: 1) DB connection pool, 2) downstream payment gateway, 3) recent deployments"
- Bad runbook: "Investigate the issue and resolve it" — thanks, very helpful
- Runbooks should be tested. If you haven't run through it in the last quarter, it's probably wrong.
- Store them where people can find them at 3 AM. Not in a wiki nobody remembers the URL for.

## Mitigation vs Root Cause

- During the incident: MITIGATE. Stop the bleeding. Rollback. Feature flag. Failover.
- After the incident: ROOT CAUSE. Why did it happen? How do we prevent it?
- Teams that try to find root cause during the incident take 3x longer to resolve
- "But if we just rollback, we'll have to fix it later" — YES. THAT'S THE POINT.
- Fix it later when you're awake, caffeinated, and not losing $10K per minute

## Post-Incident Review (Blameless Post-Mortems)

- Within 48 hours of resolution
- Blameless — focus on systems, not people
- Timeline reconstruction: what happened, when, what actions were taken
- Contributing factors (not "root cause" — incidents rarely have a single cause)
- Action items with owners and deadlines
- The 5 Whys technique — but don't stop at the first satisfying answer
- Share widely. The whole point is organizational learning.

## Building the Muscle (Practice)

- Game days: scheduled incident simulations
- Wheel of Misfortune: random on-call scenarios for practice
- Chaos engineering (callback to Part 2) feeds into incident response readiness
- The team that practices incident response handles real incidents 40% faster — need source for this

## What to Do Monday Morning

- Week 1: Define severity levels. Get agreement. Write it down.
- Week 2: Write runbooks for your top 3 failure scenarios
- Week 3: Assign incident commander rotation. Train them.
- Week 4: Run a tabletop exercise. Simulate a SEV1. See what breaks in your process.

Target: ~500 words outline
