# Incident Response: From Detection to Resolution in 10 Minutes

Part 8 of the Resilience Engineering series. We've spent seven articles building systems that contain failures, test for weaknesses, observe what's broken, degrade gracefully, survive infrastructure disasters, manage overload, and isolate failure domains. This one is about what happens when all of that isn't enough and the failure is already here.

## The 3 AM Phone Call

3:07 AM. Your phone buzzes. PagerDuty: "CRITICAL: Payment processing latency >10s, error rate 34%."

You fumble for your laptop, squinting at the screen. Slack is already on fire — 47 unread messages in #incidents. Someone typed "is anyone looking at this?" twelve minutes ago. Nobody responded. The alert fired eighteen minutes ago. Customers have been failing checkout for eighteen minutes.

You open Grafana. Payment latency is through the roof. Error rate climbing. The circuit breaker on the payment gateway hasn't tripped yet because the service isn't failing — it's just slow. Slow enough to time out half the requests but fast enough to keep the circuit breaker in its detection window.

[This is the scenario where bulkheads (Part 7) and circuit breakers (Part 1) help but don't solve the human coordination problem. The patterns contain the blast radius. But someone still needs to decide what to do.]

Eighteen minutes. In those eighteen minutes, roughly 2,700 checkout attempts failed. At an average order value of $85, that's about $230,000 in potentially lost revenue. And the clock is still running.

The first 10 minutes of an incident determine whether it's a 30-minute blip or a 4-hour catastrophe. Most teams waste those minutes figuring out who's in charge and what to look at first.

## Why the First 10 Minutes Matter More Than Everything Else

The industry average Mean Time To Recovery (MTTR) is around 197 minutes — over three hours. That number comes from a mix of detection time, triage time, coordination overhead, and actual fix time. Top-performing organizations get it under 60 minutes. Elite teams at places like Google and Netflix resolve most incidents in under 10 minutes.

The difference isn't that elite teams have better engineers. It's that they have better processes for the first 10 minutes.

The cost curve during an incident isn't linear — it's closer to exponential. In the first 5 minutes, maybe a few hundred users are affected. By 15 minutes, it's thousands, and social media starts noticing. By 30 minutes, the revenue impact is measurable and executives are asking questions. By 60 minutes, you're looking at news coverage for public companies and serious customer trust erosion.

[Every minute of fumbling in the first 10 minutes adds roughly 5-10 minutes to total incident duration. That's not a precise number — it varies wildly — but the pattern holds. Slow starts cascade into long incidents.]

## Severity Levels: Stop Arguing About This During the Incident

You need a pre-agreed severity framework. Debating severity while the system is on fire wastes time and creates confusion.

| Level | Criteria | Response | Examples |
|-------|----------|----------|----------|
| SEV1 | Revenue-impacting, customer-facing, widespread | All hands, war room, exec notification | Payment processing down, complete outage, data breach |
| SEV2 | Significant degradation, subset of customers | On-call team + engineering leads | Elevated error rates, partial feature outage, performance degradation |
| SEV3 | Minor impact, workaround available | On-call engineer handles | Single endpoint errors, non-critical feature broken, intermittent issues |
| SEV4 | No customer impact, internal only | Next business day | Internal tool broken, non-production environment issue |

The critical insight: severity determines the RESPONSE, not the root cause. You don't need to understand why payments are failing to know it's a SEV1. You just need to know payments are failing and customers are affected.

Pick a severity. Adjust later if the situation changes. Don't waste five minutes debating whether it's a SEV1 or SEV2 while customers can't check out.

## The First 10 Minutes: A Concrete Playbook

**Minutes 0-1: Acknowledge.** Say "I'm looking at this" in the incident channel. That's it. Just break the silence. The worst thing that happens during an incident is everyone assuming someone else is handling it. One message changes the dynamic entirely.

**Minutes 1-3: Triage.** Three questions: What's broken? (Payment processing.) Who's affected? (All customers attempting checkout.) What changed recently? (Check deployment history, config changes, dependency status.) The "what changed" question resolves about 40% of incidents immediately — it was a bad deploy, a config change, or a dependency went down.

**Minutes 3-5: Declare and assign roles.** Formally declare the incident and its severity. Assign three roles:
- **Incident Commander (IC)**: Coordinates the response. Does NOT debug.
- **Technical Lead**: Leads the debugging effort. Assigns investigation tasks.
- **Communications Lead**: Handles status updates — internal, external, executive.

**Minutes 5-10: First mitigation attempt.** The goal is NOT to find root cause. The goal is to stop the bleeding. Your options, roughly in order of speed:
1. **Rollback**: Was there a recent deployment? Roll it back. Don't investigate first. Just roll back.
2. **Feature flag**: Can you disable the broken feature? Do it.
3. **Failover**: Can you route traffic to a healthy region or backup system?
4. **Scale**: Is it a capacity issue? Add instances.
5. **Restart**: Sometimes the answer really is "turn it off and on again."

[The instinct to understand before acting is strong in engineers. Fight it during incidents. Mitigate first. Understand later. "But if we just rollback, we'll have to fix it later." Yes. That's the point. Fix it later when you're awake, caffeinated, and not losing money every minute.]

## The Incident Commander: Coordinator, Not Hero

The IC is the most important role during an incident, and it's the most misunderstood.

The IC is not the most senior person. Not the best debugger. The IC is the best coordinator — someone who can track multiple workstreams, make decisions under pressure, and keep communication flowing.

**What the IC does**:
- Assigns investigation tasks ("Sarah, check the database. Mike, check the payment gateway logs.")
- Tracks progress ("Sarah, what did you find? Mike, any update?")
- Makes decisions ("We're rolling back the 2:30 PM deployment. Do it now.")
- Communicates status ("Next update in 15 minutes. Current theory: bad deployment.")
- Escalates when needed ("We need the database team. Page them.")

**What the IC does NOT do**:
- Debug the issue personally
- Write code or run queries
- Get pulled into technical rabbit holes

[The anti-pattern I see most often: the IC starts debugging because they're curious or because they think they can solve it faster. The moment the IC starts debugging, nobody is coordinating. Parallel investigations happen without awareness of each other. Duplicate work. Missed signals. The incident drags on.]

## Communication: Silence Is the Enemy

During an incident, silence breeds panic. Regular updates — even "no change, still investigating" — reduce anxiety and prevent people from freelancing.

**Internal updates**: Every 15 minutes minimum during SEV1/SEV2. Post in the incident channel. Use a consistent format:

```
STATUS UPDATE — 3:45 AM
Incident: Payment processing degradation (SEV1)
Impact: ~34% of checkout attempts failing
Current action: Rolling back deployment from 2:30 PM
Next update: 4:00 AM
```

**External updates**: Status page update within 5 minutes of SEV1 declaration. Customers would rather see "We're aware of an issue affecting checkout and are working on it" than nothing at all.

**Executive updates**: Brief summary every 30 minutes for SEV1. Keep it to four things: what's broken, who's affected, what you're doing, when's the next update. Executives don't need technical details during the incident. They need confidence that someone competent is handling it.

## Runbooks: Because Your 3 AM Brain Can't Think

At 3 AM, you're operating at maybe 60% cognitive capacity. Runbooks compensate for the gap.

A good runbook is a step-by-step procedure for a specific failure scenario. Not "investigate and resolve" — that's not a runbook, that's a wish. A good runbook looks like:

```markdown
## Runbook: Payment Processing Latency > 5s

### Quick Checks (2 minutes)
1. Check recent deployments: `kubectl rollout history deployment/payment-service`
2. Check payment gateway status: https://status.paymentgateway.com
3. Check DB connection pool: Grafana dashboard → Payment DB → Active Connections

### If recent deployment (last 2 hours):
1. Rollback: `kubectl rollout undo deployment/payment-service`
2. Verify: Watch error rate for 5 minutes
3. If resolved: Document and schedule root cause analysis

### If payment gateway degraded:
1. Enable fallback payment processor: Feature flag `payment.fallback.enabled = true`
2. Monitor fallback error rate
3. Notify payment gateway vendor

### If DB connection pool exhausted:
1. Kill long-running queries: [link to query kill procedure]
2. Increase pool size temporarily: [link to config change procedure]
3. Check for connection leaks in recent code changes
```

Runbooks should be tested quarterly. If you haven't walked through a runbook in the last three months, assume it's at least partially wrong — services change, dashboards move, commands get deprecated.

Store them somewhere your on-call engineer can find at 3 AM without thinking. A pinned message in the incident channel. A bookmark in the on-call handbook. Not buried in a wiki that requires three clicks and a search.

## After the Fire: Blameless Post-Incident Review

Within 48 hours of resolution — while memories are fresh but emotions have cooled — run a post-incident review.

The word "blameless" matters. The goal is to understand what happened and improve systems, not to assign fault. If your post-incident reviews feel like interrogations, people will hide information, and you'll learn nothing.

**Timeline reconstruction**: What happened, when, and what actions were taken. Build this from logs, chat transcripts, and alert history — not from memory, which is unreliable under stress.

**Contributing factors**: Not "root cause." Incidents rarely have a single root cause. They have contributing factors — a combination of conditions that together produced the failure. The deployment was bad AND the canary analysis missed it AND the circuit breaker threshold was too high AND the on-call engineer was in a different timezone.

**Action items**: Specific, owned, and deadlined. "Improve monitoring" is not an action item. "Add latency P99 alert for payment service with 5-second threshold, owned by Sarah, due by April 15" is an action item.

**The 5 Whys**: A useful technique, but don't stop at the first satisfying answer. "Why did the deployment fail?" → "Bad config." That's not deep enough. Why was the bad config deployed? Why didn't the validation catch it? Why wasn't there a canary? Keep going until you hit systemic issues.

Share the post-incident review widely. The whole point is organizational learning. An incident that teaches only the people in the war room is a wasted incident.

## Building the Muscle: Practice Before You Need It

Incident response is a skill, and skills atrophy without practice.

**Game days**: Scheduled incident simulations where you inject a realistic failure and run through the full response process. Not just the technical fix — the coordination, communication, and decision-making.

**Tabletop exercises**: Lower-cost alternative. Gather the team, present a scenario on a whiteboard, and walk through the response. "It's 3 AM. Payment processing is down. The last deployment was 6 hours ago. What do you do?" No actual systems involved, but the coordination practice is real.

**Wheel of Misfortune**: Google's practice of randomly selecting an on-call engineer and presenting them with a past incident scenario. They have to triage, coordinate, and resolve it as if it were real. Great for building confidence and identifying process gaps.

Teams that practice incident response regularly handle real incidents significantly faster. The coordination patterns become muscle memory. The runbooks get tested and updated. The severity framework gets internalized. When the real 3 AM call comes, the response is automatic, not improvised.

## What to Do Monday Morning

**Week 1**: Define your severity levels. Get agreement from engineering leadership. Write them down. Post them in your incident channel.

**Week 2**: Write runbooks for your top 3 failure scenarios. The ones that have actually happened, or the ones that would hurt the most. Test them by walking through each step.

**Week 3**: Establish an incident commander rotation. Train at least 3-4 people. The IC role is a skill — it needs practice and explicit training, not just assignment.

**Week 4**: Run a tabletop exercise. Pick a realistic scenario. Walk through the first 10 minutes. See where the process breaks down. Fix those gaps before the next real incident.

Target: ~2,000 words when complete
