---
title: "The Day AWS Went Down: Building Systems That Survive Infrastructure Apocalypse"
subtitle: "December 7, 2021. AWS us-east-1 goes dark. Netflix, Disney+, Robinhood go offline. Except... some don't. What did they know that you don't?"
series: "Resilience Engineering Part 5"
reading-time: "8-10 minutes"
target-audience: "Software architects, platform engineers, CTOs, SREs"
keywords: "multi-region architecture, disaster recovery, AWS outage, infrastructure resilience, geographic redundancy"
status: "v1-brainstorming-outline"
created: "2026-03-08"
author: "Daniel Stauffer"
---

# The Day AWS Went Down: Building Systems That Survive Infrastructure Apocalypse

Part 5 of my series on Resilience Engineering. Last time, we explored graceful degradation — what to do when all your fallbacks fail simultaneously. This time: what happens when your entire cloud provider goes dark, and how to build systems that survive infrastructure disasters. Follow along for more deep dives into building systems that don't fall apart.

## Opening Hook - The AWS Apocalypse

December 7, 2021. 10:45 AM EST. AWS us-east-1 starts having "issues" (their word, not mine).

Within minutes:
- Netflix: Down
- Disney+: Down  
- Robinhood: Down
- Ring doorbells: Not working
- Roomba vacuums: Stuck
- Thousands of websites: Gone

[Need exact numbers here - how many services affected? How long? Total economic impact?]

But here's the interesting part: Some companies stayed up. Amazon.com kept selling. AWS Console (ironically) kept working. Some Netflix services stayed online.

What did they know that everyone else didn't?

[Maybe start with a Slack message: "us-east-1 is down. Are we down?" "Nope, we're fine." "How?"]

## The us-east-1 Problem (Why Everyone Uses It)

Here's the dirty secret about AWS: us-east-1 is special.

It's not just another region. It's THE region. The one where:
- New services launch first (sometimes exclusively for months)
- Control plane APIs live (even for other regions)
- IAM is global but... lives in us-east-1
- Route 53 health checks originate
- CloudFront has special integration
- Pricing is cheapest (by like 10-20%)

[Is this still true? Need to verify current state]

So everyone uses us-east-1. Even if you're "multi-region," you probably depend on us-east-1 for something.

This is the hidden single point of failure in "cloud-native" architecture.

## Real Disaster Stories (The Hall of Shame)

### AWS us-east-1 Outage (December 7, 2021)

[Need details:
- What actually failed? (Was it networking? Power? API?)
- How long? (I think 4-5 hours?)
- What services were affected?
- Which companies went down?
- Which stayed up and how?
- Total economic impact?]

The kicker: This wasn't even the first time. us-east-1 has gone down multiple times. And it will happen again.

### The OVH Datacenter Fire (March 10, 2021)

A datacenter in Strasbourg, France literally caught fire and burned down.

[Need details:
- How many servers lost?
- How many companies affected?
- Data recovery stats?
- Companies that lost everything vs companies that survived?]

The lesson: "The cloud" is just someone else's computer. And computers can catch fire.

### Azure DNS Outage (April 1, 2021)

Azure's DNS service went down globally. Not April Fools.

[Need details:
- Duration?
- Global impact?
- Why DNS is the ultimate single point of failure?]

If DNS is down, nothing works. Your multi-region architecture doesn't matter if nobody can find it.

### GCP Networking Outage (June 2, 2019)

Google's network configuration change took down YouTube, Gmail, and half the internet.

[Need details:
- What was the configuration change?
- How long?
- Cascading effects?]

Even Google, who literally invented modern distributed systems, can take themselves down with a config change.

## Why "Multi-Region" Doesn't Mean What You Think

Marketing says: "We're multi-region! We're resilient!"

Reality: "We have servers in multiple regions, but they all depend on us-east-1 for IAM, and our database is in one region, and our control plane is in us-east-1, and..."

Let me show you the hidden dependencies that make "multi-region" a lie:

### Hidden Dependency #1: Control Plane vs Data Plane

Your application runs in us-west-2 (data plane). Great!

But when us-east-1 goes down:
- Can't create new resources (control plane in us-east-1)
- Can't update security groups (control plane)
- Can't scale (auto-scaling API in us-east-1)
- Can't deploy (CI/CD depends on us-east-1 APIs)

Your app keeps running... until something needs to change. Then you're stuck.

### Hidden Dependency #2: IAM is "Global" (But Not Really)

IAM is global, right? Wrong.

IAM lives in us-east-1. When us-east-1 goes down:
- Existing tokens work (cached)
- New authentication fails
- Token refresh fails after TTL expires
- Service-to-service auth breaks

[How long do IAM tokens last? Need to check - I think 1 hour for temporary credentials?]

### Hidden Dependency #3: DNS and Health Checks

Route 53 health checks originate from... us-east-1 (mostly).

When us-east-1 goes down, health checks fail, Route 53 thinks your healthy regions are dead, routes traffic to... nowhere.

[Is this still true? Need to verify current Route 53 architecture]

### Hidden Dependency #4: Your Database is Still in One Region

You have servers in 3 regions. Great!

Your database is in us-east-1. Not great.

When us-east-1 goes down, your servers in other regions can't reach the database. You're down everywhere.

[This is where we talk about data replication strategies - but that's complex enough for its own section]

## Active-Active vs Active-Passive (The Tradeoffs Nobody Talks About)

### Active-Active: Both Regions Serve Traffic

**The Promise**: Full redundancy! If one region dies, the other keeps serving!

**The Reality**: 
- 2x infrastructure cost (running both regions at full capacity)
- Data consistency nightmares (how do you keep databases in sync?)
- Split-brain scenarios (what if regions can't talk to each other?)
- Conflict resolution (two users update the same record in different regions)
- Cross-region latency (users in US hitting EU database)

**When It Works**: Read-heavy workloads, eventually consistent data, high-value services where cost doesn't matter

**When It Doesn't**: Write-heavy workloads, strong consistency requirements, cost-sensitive applications

### Active-Passive: One Region on Standby

**The Promise**: Cheaper than active-active! Failover when needed!

**The Reality**:
- Standby region is cold (or warm at best)
- Failover takes time (minutes to hours)
- Failover is manual (or automated but scary)
- Standby might not work (when did you last test it?)
- Data replication lag (standby is behind primary)

**When It Works**: Cost-sensitive applications, infrequent failures, acceptable downtime (minutes to hours)

**When It Doesn't**: High-availability requirements, zero-downtime requirements, real-time data needs

[Need a decision matrix here - when to use which approach]

## Data Replication Strategies (The Hard Part)

This is where multi-region gets really complicated.

### Synchronous Replication: Strong Consistency, High Latency

Write goes to both regions before acknowledging success.

**Pros**: 
- No data loss (both regions always in sync)
- Strong consistency (reads always see latest writes)

**Cons**:
- High latency (wait for cross-region network)
- Reduced availability (if one region is down, writes fail)
- Expensive (cross-region bandwidth costs)

**Example**: Financial transactions, inventory management, anything where consistency matters more than speed

[What's the latency? us-east-1 to us-west-2 is like 60-80ms round trip?]

### Asynchronous Replication: Low Latency, Eventual Consistency

Write goes to primary region, replicates to secondary in background.

**Pros**:
- Low latency (don't wait for replication)
- High availability (primary region failure doesn't block writes)
- Cheaper (less cross-region traffic)

**Cons**:
- Data loss risk (if primary fails before replication)
- Eventual consistency (reads might see stale data)
- Conflict resolution needed (what if both regions get writes?)

**Example**: Social media posts, analytics data, anything where speed matters more than consistency

[How much lag is typical? Seconds? Minutes?]

### The CAP Theorem in Practice

You can't have all three:
- Consistency (all nodes see same data)
- Availability (system always responds)
- Partition tolerance (works despite network failures)

Pick two. In multi-region, you're always dealing with partitions (network between regions can fail).

So you choose: Consistency (CP) or Availability (AP)?

[Need examples of each - maybe DynamoDB (AP) vs Spanner (CP)?]

## Traffic Routing and Failover (How to Actually Do This)

### DNS-Based Routing (Route 53, CloudFlare)

**How It Works**: DNS returns different IPs based on health checks

**Pros**: Simple, works with any application, no code changes

**Cons**: DNS caching (TTL means slow failover), health check delays, client-side caching

**Failover Time**: Minutes (due to DNS TTL)

[What's a reasonable TTL? 60 seconds? Lower?]

### Global Load Balancers (AWS Global Accelerator, Azure Front Door)

**How It Works**: Anycast routing to nearest healthy region

**Pros**: Fast failover (seconds), no DNS caching issues, health checks at network layer

**Cons**: More expensive, more complex, vendor lock-in

**Failover Time**: Seconds

### Application-Level Routing (Service Mesh, API Gateway)

**How It Works**: Application code decides which region to use

**Pros**: Most control, can do smart routing (user affinity, data locality)

**Cons**: Most complex, requires code changes, harder to test

**Failover Time**: Milliseconds to seconds

[Need code examples for each approach]

## Regional Cell Design (Cells at Scale)

Remember cell-based architecture from Part 1? Now apply it at regional scale.

Each region is a cell:
- Complete isolation (compute, data, network)
- No cross-region dependencies (except replication)
- Independent failure domains
- Traffic routed to healthy regions only

[Draw this - region as cell, with internal cells inside each region]

But here's the complexity: cells within regions, regions as cells, how do they interact?

[This needs more thought - maybe a whole section on hierarchical cell design?]

## Cost Analysis (The Part Nobody Wants to Talk About)

Let's be honest: Multi-region is expensive.

### Infrastructure Costs

**Single Region**: $10,000/month
**Active-Passive Multi-Region**: $15,000/month (50% increase)
- Primary region: $10,000
- Standby region: $3,000 (minimal compute, full data)
- Replication: $2,000 (cross-region bandwidth)

**Active-Active Multi-Region**: $25,000/month (150% increase)
- Region 1: $10,000
- Region 2: $10,000
- Replication: $5,000 (bidirectional, more traffic)

[These are made-up numbers - need real examples]

### Data Transfer Costs

Cross-region data transfer is expensive:
- AWS: $0.02/GB (us-east-1 to us-west-2)
- If you're replicating 1TB/day: $600/month just for bandwidth
- If you're doing synchronous replication: double that (round trip)

[Verify current AWS pricing]

### Operational Costs

- 2x the infrastructure to manage
- 2x the monitoring and alerting
- 2x the deployment complexity
- More on-call burden (more things to break)
- More testing needed (failover drills)

### When It's Worth It

Do the math:
- Downtime cost: $100,000/hour
- Multi-region cost: $15,000/month extra
- Break-even: If you prevent 9 minutes of downtime per month, it pays for itself

If your downtime costs less than $100K/hour, multi-region might not be worth it.

[Need a calculator or decision tree here]

## Disaster Recovery Testing (Game Days for Regions)

You can't know if your multi-region architecture works until you test it.

### Regional Failover Drills

**The Scenario**: Simulate us-east-1 complete failure

**The Process**:
1. Announce drill (don't surprise people)
2. Block all traffic to us-east-1 (firewall rules)
3. Observe what breaks
4. Fix what breaks
5. Document lessons learned
6. Repeat quarterly

**What You'll Discover**:
- Hidden dependencies on us-east-1
- Services that don't failover correctly
- Data replication lag issues
- Monitoring blind spots
- Runbook gaps

[Need example of a real drill - what broke, how they fixed it]

### Chaos Engineering for Regions

Use AWS Fault Injection Simulator (or similar) to:
- Terminate all instances in a region
- Block network traffic between regions
- Simulate DNS failures
- Inject latency in cross-region calls

[Reference Part 2 on chaos engineering]

## Real-World Multi-Region Architectures

### Netflix: Global Active-Active

[Need details:
- How do they do it?
- What's their data strategy?
- How do they handle consistency?
- What did they do during us-east-1 outage?]

### Amazon: Regional Partitioning

[Need details:
- How do they partition by region?
- How do they handle cross-region orders?
- What's their failover strategy?]

### Stripe: Payment Processing Across Regions

[Need details:
- How do they ensure payment consistency?
- What's their replication strategy?
- How do they handle regional failures?]

### Google: Spanner's Global Consistency

[Need details:
- How does Spanner do global consistency?
- What's the latency cost?
- When is it worth it?]

## The "Nuclear Bunker" Approach (When Cloud Isn't Enough)

What if AWS just... stopped existing?

[This might be too paranoid, but some companies actually do this]

### Multi-Cloud Strategies (AWS + Azure + GCP)

**The Promise**: No vendor lock-in! Ultimate resilience!

**The Reality**:
- 3x the complexity
- 3x the cost
- 3x the operational burden
- Different APIs, different tools, different everything
- Data consistency across clouds is a nightmare

**When It's Worth It**: Regulated industries, government contracts, paranoid CTOs

**When It's Not**: Everyone else

### The "Eject Button" Architecture

Design your system so you can run it anywhere:
- Containerized (Kubernetes)
- Cloud-agnostic storage (S3-compatible APIs)
- Portable databases (PostgreSQL, not Aurora)
- Infrastructure as code (Terraform, not CloudFormation)

**The Tradeoff**: You give up cloud-specific features (managed services, serverless, etc.) for portability

[Is this worth it? Probably not for most companies]

### Offline Backups and Cold Storage

The ultimate fallback: backups you can restore anywhere

- Daily snapshots to S3 (and Glacier)
- Copy snapshots to different cloud provider
- Test restoration quarterly
- Paper runbooks for "start from scratch" scenario

[How long would it take to restore from cold storage? Days? Weeks?]

## Regulatory and Data Sovereignty Constraints

Sometimes multi-region isn't a choice - it's a requirement.

### GDPR and Data Residency

EU data must stay in EU. Can't replicate to US.

**The Challenge**: How do you do multi-region when you can't replicate data?

**The Solution**: Regional partitioning (EU users in EU region, US users in US region)

[What about users who travel? VPN? This gets complicated]

### Financial Services Regulations

Banks have specific requirements for disaster recovery:
- RTO (Recovery Time Objective): How long can you be down?
- RPO (Recovery Point Objective): How much data can you lose?

[Need examples of actual requirements - I think some banks require <1 hour RTO?]

### Healthcare Compliance (HIPAA)

Healthcare data has specific requirements:
- Encryption at rest and in transit
- Audit logging
- Access controls
- Backup and recovery

[How does this affect multi-region? Need to research]

## Implementation Patterns (How to Actually Build This)

[This section needs code examples, architecture diagrams, step-by-step guides]

### Pattern 1: DNS-Based Failover with Route 53

[Code example: Route 53 health checks, failover routing]

### Pattern 2: Global Load Balancer with AWS Global Accelerator

[Code example: Global Accelerator setup, health checks]

### Pattern 3: Application-Level Routing with Service Mesh

[Code example: Istio/Linkerd multi-region routing]

### Pattern 4: Database Replication with RDS Cross-Region

[Code example: RDS read replicas, promotion to primary]

### Pattern 5: DynamoDB Global Tables

[Code example: Global tables setup, conflict resolution]

## The Honest Tradeoffs (What Nobody Tells You)

Let me be real: Multi-region is hard, expensive, and often not worth it.

**When You Need It**:
- Downtime costs >$100K/hour
- Regulatory requirements
- Global user base (latency matters)
- High-profile service (reputation matters)

**When You Don't**:
- Startup with <$1M revenue
- Internal tools
- Downtime is annoying but not catastrophic
- Budget constraints

**The Middle Ground**:
- Start single-region
- Build for multi-region (but don't deploy it yet)
- Have a disaster recovery plan
- Test failover quarterly
- Deploy multi-region when revenue justifies cost

## Conclusion (What to Do Monday Morning)

[Summary of key patterns, actionable next steps, teaser for next article]

Target: ~2,000 words when complete (this is the skeleton, flesh out in v2)

---

## Notes for v2

- Need to research all the disaster stories (exact numbers, dates, details)
- Need real cost analysis (not made-up numbers)
- Need code examples for each implementation pattern
- Need architecture diagrams (regional cells, data replication, traffic routing)
- Need decision matrices (when to use which approach)
- Consider splitting into two articles? (This might be too long)
- Maybe focus more on AWS since that's what most people use?
- Or make it cloud-agnostic? (AWS, Azure, GCP examples)
