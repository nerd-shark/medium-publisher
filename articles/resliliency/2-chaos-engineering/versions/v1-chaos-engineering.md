---
document-title: Resilience Engineering Series
document-subtitle: Chaos Engineering in Production
document-type: Medium Article Draft
document-date: 2025-02-08
document-revision: 1.0
document-author: Daniel Stauffer
author-email: daniel_stauffer@jabil.com
author-org: Enterprise Architecture
review-cycle: Per Article
---

# Chaos Engineering in Production: Breaking Things on Purpose (So They Don't Break by Accident)

*Part 2 of the Resilience Engineering Series*

In 2011, Netflix was migrating from their data center to AWS. They had circuit breakers, redundancy, failover mechanisms—all the resilience patterns you'd expect from a company streaming video to millions of customers.

Then someone asked the uncomfortable question: "Do we actually know if any of this works?"

They didn't. Nobody did. The circuit breakers had never been tested in production. The failover mechanisms had only been tested in staging. The redundancy was theoretical.

So Netflix did something radical: They built a tool that randomly killed production servers. They called it Chaos Monkey.

Engineers were horrified. "You want to break production ON PURPOSE?"

Yes. Because if you don't break it on purpose, it'll break by accident—at 3 AM on Black Friday when you're least prepared.

Today, Netflix runs thousands of chaos experiments every year. Their availability is 99.99%. And they haven't had a major streaming outage in years.

This is chaos engineering: breaking things on purpose, in controlled ways, to find weaknesses before they cause real incidents.

## Why Staging Tests Are Lying to You

Every engineer has lived this nightmare: Your code works perfectly in staging. All tests pass. You deploy to production. Everything explodes.

Why? Because staging is a lie.

**Staging is too clean**. It doesn't have:
- Real traffic patterns (spiky, unpredictable, malicious)
- Real data volumes (billions of rows, not thousands)
- Real failure modes (network partitions, cascading failures, resource exhaustion)
- Real dependencies (third-party APIs that go down at the worst time)
- Real humans (who do unexpected things)

**Staging is too small**. You can't replicate:
- 10,000 requests per second
- 500 microservices talking to each other
- Distributed transactions across 3 data centers
- The emergent behaviors that only appear at scale

**Staging is too perfect**. It doesn't have:
- Servers that randomly die
- Networks that randomly partition
- Databases that randomly slow down
- Caches that randomly expire

Production is messy, chaotic, and full of surprises. Staging is neat, predictable, and boring.

If you want to know if your resilience patterns actually work, you have to test them where it matters: in production.

## The Four Principles of Chaos Engineering

Chaos engineering isn't just "break random stuff and see what happens." It's a disciplined approach to finding weaknesses.

### 1. Build a Hypothesis

Before you break anything, predict what SHOULD happen.

**Example**: "When we kill the primary database, the circuit breaker should open, traffic should route to the read replica, and users should see slightly stale data but no errors."

Not: "Let's kill the database and see what happens."

### 2. Define the Blast Radius

Start small. Expand gradually. Never risk the entire system.

**Example**: 
- Week 1: Kill one server in one availability zone, affecting 1% of traffic
- Week 2: Kill all servers in one AZ, affecting 10% of traffic
- Week 3: Kill an entire region, affecting 30% of traffic

Not: "Let's kill everything and see if we survive."

### 3. Run Experiments in Production

Staging won't tell you the truth. Production will.

But production experiments need safety controls:
- **Canary**: Start with 1% of traffic
- **Time-box**: Auto-rollback after 5 minutes
- **Kill switch**: Abort button for emergencies
- **Monitoring**: Watch metrics like a hawk

### 4. Measure and Learn

Did the system behave as expected? If yes, great—your resilience patterns work. If no, you just found a weakness before it caused a real incident.

**Metrics to track**:
- Error rates (did they spike?)
- Latency (did it increase?)
- Circuit breaker state (did it open?)
- Fallback usage (did fallbacks activate?)
- Customer impact (did users notice?)

## Failure Injection Techniques

What can you break? Pretty much anything.

### Network Failures

**Latency injection**: Add 500ms delay to all requests to a service
```yaml
# AWS FIS experiment: Inject latency
apiVersion: fis.aws.amazon.com/v1
kind: Experiment
metadata:
  name: inject-latency
spec:
  targets:
    - resourceType: aws:ec2:instance
      selectionMode: PERCENT(10)
      filters:
        - path: tag:Environment
          values: [production]
  actions:
    - name: InjectLatency
      actionId: aws:network:disrupt-connectivity
      parameters:
        duration: PT5M
        delayMilliseconds: 500
```

**Packet loss**: Drop 10% of packets to simulate flaky network

**Network partition**: Isolate a service from its dependencies

### Service Failures

**Kill processes**: Terminate random instances
```python
# Chaos Toolkit: Kill random pods
{
  "type": "action",
  "name": "terminate-pod",
  "provider": {
    "type": "python",
    "module": "chaosk8s.pod.actions",
    "func": "terminate_pods",
    "arguments": {
      "label_selector": "app=api-server",
      "qty": 1,
      "ns": "production"
    }
  }
}
```

**Resource exhaustion**: Fill disk, exhaust memory, max out CPU

**Connection pool exhaustion**: Open connections until pool is full

### Infrastructure Failures

**Terminate instances**: Kill EC2 instances, Kubernetes nodes

**Fill disks**: Write garbage data until disk is full

**Throttle I/O**: Slow down disk reads/writes

### Dependency Failures

**Third-party API outage**: Block requests to external APIs

**Database slowdown**: Inject latency into database queries

**Cache expiration**: Flush cache to test cold-start behavior

## Tools for Chaos Engineering

### AWS Fault Injection Simulator (FIS)

**Best for**: AWS-native infrastructure

**What it does**: Injects failures into EC2, ECS, RDS, EKS

**Example**: Terminate 20% of EC2 instances in an Auto Scaling group

**Pros**: Native AWS integration, safe by default, good blast radius controls

**Cons**: AWS-only, limited failure types

### Gremlin

**Best for**: Enterprise chaos engineering programs

**What it does**: Comprehensive failure injection (network, resource, state)

**Example**: Inject CPU load, network latency, disk I/O throttling

**Pros**: Easy to use, great UI, excellent safety controls, multi-cloud

**Cons**: Commercial (paid), can be expensive at scale

### Chaos Toolkit

**Best for**: Open source, scriptable chaos

**What it does**: Python-based chaos experiments, extensible

**Example**: Kill Kubernetes pods, inject HTTP errors, simulate cloud outages

**Pros**: Free, flexible, scriptable, large community

**Cons**: Requires more setup, less polished UI

### LitmusChaos

**Best for**: Kubernetes-native chaos

**What it does**: Chaos experiments as Kubernetes CRDs

**Example**: Pod deletion, network chaos, node drain

**Pros**: Kubernetes-native, GitOps-friendly, CNCF project

**Cons**: Kubernetes-only, steeper learning curve

## Game Days: Chaos as a Team Sport

The best chaos engineering isn't done alone. It's done as a team, on a schedule, with everyone watching.

**Game Day Format**:
1. **Pre-game** (1 week before):
   - Announce the game day
   - Define the scenario (e.g., "Region failure")
   - Set success criteria
   - Prepare monitoring dashboards

2. **Game time** (2 hours):
   - Inject the failure
   - Watch the system respond
   - Measure impact
   - Document observations

3. **Post-game** (1 hour):
   - Retrospective: What worked? What didn't?
   - Action items: What needs to be fixed?
   - Celebrate: What resilience patterns worked?

**Example Game Day**: "Database Primary Failure"
- **Scenario**: Kill the primary database at 2 PM
- **Hypothesis**: Circuit breaker opens, traffic routes to read replica, users see stale data
- **Reality**: Circuit breaker opened, but connection pool wasn't released, causing 30 seconds of errors
- **Action Item**: Fix connection pool cleanup in circuit breaker logic
- **Result**: Found and fixed a bug before it caused a real incident

## Building Organizational Buy-In

The hardest part of chaos engineering isn't technical—it's political.

**Common objections**:
- "We can't risk breaking production"
- "We don't have time for this"
- "Our systems are already reliable"
- "What if we cause a real outage?"

**How to overcome them**:

### Start Small
Don't ask to kill the production database on day one. Start with:
- Non-critical systems
- Off-peak hours
- Tiny blast radius (1% of traffic)
- Short duration (5 minutes)

### Demonstrate Value
After your first chaos experiment, show:
- "We found a bug that would have caused a P1 incident"
- "We validated our circuit breakers actually work"
- "We discovered a hidden dependency we didn't know about"

### Celebrate Wins
When chaos engineering prevents an incident, make noise about it:
- "Chaos experiment last month found this bug"
- "Our MTTR improved by 40% after chaos testing"
- "We haven't had a cascading failure since we started chaos"

### Make it Safe
Show that you have controls:
- Blast radius limits
- Automatic rollback
- Kill switches
- Monitoring and alerting

## Measuring Resilience Improvements

How do you know chaos engineering is working?

**Before Chaos Engineering**:
- MTTR: 45 minutes (mean time to recovery)
- Incidents per month: 8
- Cascading failures: 3 per quarter
- Customer impact: High (every incident affects users)

**After 6 Months of Chaos Engineering**:
- MTTR: 12 minutes (73% improvement)
- Incidents per month: 3 (62% reduction)
- Cascading failures: 0 (100% elimination)
- Customer impact: Low (most incidents contained)

**Why the improvement?**:
- Circuit breakers actually tested and fixed
- Hidden dependencies discovered and addressed
- Fallback chains validated and improved
- Team muscle memory for incident response

## Real-World Chaos Experiments

### Experiment 1: Kill Database Primary

**Hypothesis**: Circuit breaker opens, traffic routes to read replica

**Reality**: Circuit breaker opened, but application didn't release connections, causing 30-second outage

**Fix**: Added connection pool cleanup to circuit breaker logic

**Result**: Next time database failed (for real), zero customer impact

### Experiment 2: Exhaust Connection Pool

**Hypothesis**: Circuit breaker opens when pool exhausted, requests queue

**Reality**: Circuit breaker never opened because pool exhaustion didn't trigger error threshold

**Fix**: Added connection pool saturation as circuit breaker trigger

**Result**: Prevented connection pool exhaustion incident 2 weeks later

### Experiment 3: Simulate AWS Region Failure

**Hypothesis**: Traffic fails over to backup region within 60 seconds

**Reality**: Failover took 5 minutes because DNS TTL was too long

**Fix**: Reduced DNS TTL from 300 seconds to 60 seconds

**Result**: Actual region failure 3 months later, failover in 90 seconds

## Validating Circuit Breakers from Part 1

Remember the circuit breakers we built in Part 1? Chaos engineering is how you prove they work.

**Chaos Experiments for Circuit Breakers**:
1. **Kill downstream service**: Does circuit breaker open?
2. **Inject latency**: Does circuit breaker open on timeout?
3. **Return errors**: Does circuit breaker open on error threshold?
4. **Test half-open state**: Does circuit breaker try to recover?
5. **Test fallback chain**: Do fallbacks activate correctly?

**Example**: Testing the credit risk circuit breaker from Part 1
- Inject 500ms latency into ML model API
- Circuit breaker should open after 5 timeouts
- Fallback to rules engine should activate
- Users should see slightly less accurate risk scores but no errors

**Result**: Circuit breaker worked, but fallback chain had a bug—rules engine wasn't properly initialized. Fixed before it caused a production incident.

## The Tradeoffs (Let's Be Honest)

Chaos engineering isn't free. Here's what you're trading:

### Risk of Real Incidents
Yes, you might cause a real outage. That's why you:
- Start with tiny blast radius
- Use automatic rollback
- Have kill switches
- Monitor constantly

### Complexity
Chaos infrastructure adds complexity:
- Chaos tools to maintain
- Experiments to write and update
- Monitoring to set up
- Team coordination

### Time Investment
Chaos engineering takes time:
- Writing experiments: 2-4 hours per experiment
- Running game days: 3-4 hours per game day
- Post-game analysis: 1-2 hours
- Fixing discovered issues: Varies

**When it's worth it**: High-availability systems, customer-facing services, anything where downtime is expensive

**When it's not**: Internal tools, low-traffic systems, anything where downtime is acceptable

## What's Next

In Part 3, we'll tackle **The $10M Blind Spot: Why Your Monitoring is Lying to You**.

We'll cover:
- Why "everything is green" doesn't mean your system works
- The metrics that actually predict outages
- Observability for chaos experiments
- Building dashboards that reveal truth, not theater

Chaos engineering finds weaknesses. Observability helps you see them. Together, they're the foundation of reliable systems.

## The Bottom Line

You don't know if your resilience patterns work until you test them in production. Staging is too clean, too small, and too perfect to tell you the truth.

Chaos engineering is how you find weaknesses before they cause real incidents. Start small, expand gradually, measure everything, and learn from every experiment.

Netflix proved it works. Thousands of companies have followed. The question isn't "Should we do chaos engineering?" It's "Can we afford NOT to?"

**Question for you**: What's the scariest failure you could inject into your system right now? What would happen? Do you actually know, or are you guessing?

---

*Daniel Stauffer is an Enterprise Architect specializing in resilience engineering and platform operations. This is Part 2 of the Resilience Engineering series. Read [Part 1: Cell-Based Architecture & Circuit Breakers](#) for the foundation of failure containment.*

**Tags**: #ChaosEngineering #SRE #Resilience #ProductionTesting #Netflix #DevOps #SystemReliability

---

**Word Count**: ~2,100 words | **Reading Time**: ~7 minutes
