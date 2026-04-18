---
title: "The Day AWS Went Down: Building Systems That Survive Infrastructure Apocalypse"
subtitle: "December 7, 2021. AWS us-east-1 goes dark. Netflix, Disney+, Robinhood go offline. Except... some don't. What did they know that you don't?"
series: "Resilience Engineering Part 5"
reading-time: "9 minutes"
target-audience: "Software architects, platform engineers, CTOs, SREs"
keywords: "multi-region architecture, disaster recovery, AWS outage, infrastructure resilience, geographic redundancy"
status: "v2-detailed-outline"
created: "2026-03-08"
author: "Daniel Stauffer"
---

# The Day AWS Went Down: Building Systems That Survive Infrastructure Apocalypse

Part 5 of my series on Resilience Engineering. Last time, we explored graceful degradation — what to do when all your fallbacks fail simultaneously. This time: what happens when your entire cloud provider goes dark, and how to build systems that survive infrastructure disasters.

## The AWS Apocalypse

December 7, 2021. 10:45 AM EST. AWS us-east-1 starts having "issues."

Within 30 minutes, the internet is on fire. Netflix goes dark. Disney+ stops streaming. Robinhood freezes trading. Ring doorbells stop recording. Even Roomba vacuums lose connection to their cloud brains. Thousands of websites return 503 errors. The AWS status page (ironically hosted in us-east-1) struggles to load.

The outage lasts 5 hours. Estimated economic impact: over $100 million in lost revenue across affected companies. Customer trust damage: immeasurable.

But here's what's interesting: Some companies stayed online. Amazon.com kept selling products. Parts of Netflix continued streaming. AWS Console (the tool you use to manage AWS) mostly worked. These companies had something the others didn't: real multi-region architecture.

[Need to verify which specific Netflix services stayed up - I think it was their CDN/edge services that survived because they're truly distributed]

This wasn't AWS's first rodeo. us-east-1 has gone down multiple times. It won't be the last. The question isn't "will your cloud provider fail?" It's "when it fails, will you survive?"

## The us-east-1 Problem

Here's the dirty secret about AWS: us-east-1 isn't just another region. It's THE region.

**Why everyone uses us-east-1:**
- New services launch here first (sometimes exclusively for 6-12 months)
- Cheapest pricing (10-20% less than other regions)
- Lowest latency to major US population centers
- Most mature infrastructure (it's the oldest region)
- Best third-party integration support

**Why us-east-1 is dangerous:**
- Control plane APIs for many services live here
- IAM is "global" but actually runs in us-east-1
- Route 53 health checks originate primarily from us-east-1
- CloudFront has special dependencies on us-east-1
- Many AWS services have hidden us-east-1 dependencies

So even if you think you're "multi-region," you probably depend on us-east-1 for something critical. This is the hidden single point of failure in cloud-native architecture.

[Draw diagram: "Your Multi-Region Architecture" showing apps in 3 regions, all with arrows pointing to us-east-1 for IAM, control plane, etc.]

## Real Disaster Stories

### AWS us-east-1 Outage (December 7, 2021)

**What Failed**: AWS's internal network device management system. A routine automation to scale capacity triggered a bug that cascaded through the network control plane.

**Duration**: 5 hours for full recovery, though some services were impacted for 11+ hours

**Impact**: 
- Thousands of websites and services offline
- Major companies affected: Netflix, Disney+, Robinhood, Coinbase, Epic Games
- Services that use AWS but don't advertise it: Ring, Roomba, many IoT devices
- Even AWS's own services struggled (Console, CloudWatch, some API endpoints)

**Who Stayed Up**: Companies with true active-active multi-region architectures that didn't depend on us-east-1 control plane for runtime operations. Amazon.com retail stayed mostly functional. Netflix's CDN edge services continued serving cached content.

**The Lesson**: Control plane vs data plane matters. Your application might run in us-west-2, but if it depends on us-east-1 APIs for anything runtime, you're vulnerable.

### The OVH Datacenter Fire (March 10, 2021)

**What Failed**: A datacenter in Strasbourg, France literally caught fire and burned down. Not a metaphor. Actual fire.

**Duration**: Permanent. The datacenter was destroyed.

**Impact**:
- 3.6 million websites offline
- Complete data loss for customers without backups
- Some companies lost everything (no backups, no disaster recovery)
- Estimated 464,000 domains affected

**Who Survived**: Companies with backups in different datacenters. Companies with multi-region architecture. Companies who took disaster recovery seriously.

**The Lesson**: "The cloud" is just someone else's computer. And computers can catch fire. Physical disasters happen.

### Azure DNS Outage (April 1, 2021)

**What Failed**: Azure's DNS service went down globally due to a configuration change.

**Duration**: 3 hours

**Impact**: If DNS doesn't work, nothing works. Your multi-region architecture is useless if nobody can find it.

**The Lesson**: DNS is the ultimate single point of failure. Even if your application is perfectly distributed, DNS can take you down.

### GCP Networking Outage (June 2, 2019)

**What Failed**: Google's network configuration change caused a cascading failure across multiple regions.

**Duration**: 4 hours

**Impact**: YouTube, Gmail, Google Cloud services, and many customer applications went offline.

**The Lesson**: Even Google, who invented modern distributed systems, can take themselves down with a bad config change. Nobody is immune.

## Why "Multi-Region" Is Usually a Lie

Your architecture diagram shows servers in three regions. Your marketing says "multi-region resilient architecture." Your status page says "99.99% uptime."

Then us-east-1 goes down and you're completely offline.

What happened?

### Hidden Dependency #1: Control Plane vs Data Plane

**Data Plane**: Your application code, serving customer requests. This runs in us-west-2.

**Control Plane**: The APIs that manage your infrastructure. This runs in us-east-1.

When us-east-1 goes down:
- Your app keeps running (data plane is fine)
- But you can't scale (auto-scaling API is down)
- Can't deploy (CI/CD uses control plane APIs)
- Can't update security groups (control plane)
- Can't create new resources (control plane)
- Can't even see what's happening (CloudWatch API is down)

Your app runs fine... until something needs to change. Then you're stuck.

[This is like having a car that runs fine but you can't steer or brake. Great until you need to turn]

### Hidden Dependency #2: IAM Lives in us-east-1

IAM is "global," right? Not exactly.

IAM's control plane lives in us-east-1. When us-east-1 goes down:
- Existing authentication tokens work (they're cached)
- New authentication fails (can't reach IAM)
- Token refresh fails after TTL expires (typically 1 hour for temporary credentials)
- Service-to-service authentication breaks
- Your services in us-west-2 can't authenticate to each other

You have about 1 hour before everything stops working.

### Hidden Dependency #3: Your Database Is in One Region

You have application servers in three regions. Excellent!

Your database is in us-east-1. Not excellent.

When us-east-1 goes down, your servers in us-west-2 and eu-west-1 can't reach the database. You're down everywhere, despite having servers in multiple regions.

[This is the most common mistake. Multi-region compute, single-region data]

### Hidden Dependency #4: Shared Services

Even if your app and database are multi-region, you probably have shared services:
- Redis cache (one region)
- Message queue (one region)
- Elasticsearch cluster (one region)
- Monitoring/logging (one region)

Any single-region shared service is a single point of failure.

## Active-Active vs Active-Passive

There are two ways to do multi-region: active-active (both regions serve traffic) and active-passive (one region on standby).

### Active-Active: The Expensive Option

**How It Works**: Both regions run at full capacity, both serve production traffic, traffic is distributed between them.

**Pros**:
- True redundancy (if one region dies, the other handles all traffic)
- No failover delay (traffic just shifts)
- Better global latency (users hit nearest region)
- Failover is tested constantly (both regions always serving traffic)

**Cons**:
- 2x infrastructure cost (both regions at full capacity)
- Data consistency is hard (two regions writing to databases)
- Split-brain scenarios (regions can't talk to each other)
- Conflict resolution needed (same record updated in both regions)
- Cross-region latency for data access

**Cost Example**:
- Single region: $10,000/month
- Active-active: $20,000/month (100% increase)
- Plus cross-region data transfer: $2,000-5,000/month

**When to Use**: High-value services where downtime costs more than infrastructure. Financial services, e-commerce during peak season, SaaS with strict SLAs.

**When NOT to Use**: Cost-sensitive applications, write-heavy workloads with strong consistency requirements, startups burning through runway.

### Active-Passive: The Cheaper Option

**How It Works**: Primary region serves all traffic, secondary region is on standby (warm or cold), failover when primary fails.

**Pros**:
- Lower cost (standby region runs minimal resources)
- Simpler data consistency (only one region writes)
- No split-brain scenarios
- Easier to reason about

**Cons**:
- Failover takes time (minutes to hours depending on warm vs cold)
- Failover is manual or scary-automated
- Standby might not work (when did you last test it?)
- Data replication lag (standby is behind primary)
- Wasted capacity (standby sits idle)

**Cost Example**:
- Single region: $10,000/month
- Active-passive: $13,000/month (30% increase)
  - Primary: $10,000
  - Standby: $2,000 (minimal compute, full data)
  - Replication: $1,000

**When to Use**: Cost-sensitive applications, acceptable downtime (minutes to hours), infrequent failures, write-heavy workloads.

**When NOT to Use**: Zero-downtime requirements, high-frequency trading, real-time systems, services where minutes of downtime cost millions.

[Need decision matrix table here: Cost vs Downtime Tolerance vs Consistency Requirements]

## Data Replication: The Hard Part

Multi-region compute is easy. Multi-region data is hard.

### Synchronous Replication: Strong Consistency

**How It Works**: Write goes to both regions before acknowledging success. Transaction commits only when both regions confirm.

**Pros**:
- Zero data loss (both regions always in sync)
- Strong consistency (reads always see latest writes)
- No conflict resolution needed

**Cons**:
- High latency (wait for cross-region network round trip)
- Reduced availability (if one region is down, writes fail)
- Expensive (cross-region bandwidth costs)

**Latency Impact**:
- us-east-1 to us-west-2: ~70ms round trip
- us-east-1 to eu-west-1: ~90ms round trip
- us-east-1 to ap-southeast-1: ~250ms round trip

Every write adds this latency. For a database with 100 writes/second, that's 100 * 70ms = 7 seconds of added latency per second. Your system is now 7x slower.

[Math doesn't quite work that way with parallelism, but the point stands - it's slow]

**When to Use**: Financial transactions, inventory management, anything where consistency matters more than speed.

**Examples**: Google Spanner, CockroachDB, AWS Aurora Global Database with synchronous replication.

### Asynchronous Replication: Eventual Consistency

**How It Works**: Write goes to primary region, acknowledges immediately, replicates to secondary in background.

**Pros**:
- Low latency (don't wait for replication)
- High availability (primary region failure doesn't block writes)
- Cheaper (less cross-region traffic)

**Cons**:
- Data loss risk (if primary fails before replication completes)
- Eventual consistency (reads might see stale data)
- Conflict resolution needed (what if both regions get writes during partition?)

**Replication Lag**:
- Typical: 1-5 seconds
- Under load: 10-30 seconds
- During network issues: minutes to hours

If primary region fails, you lose any writes from the last N seconds.

**When to Use**: Social media posts, analytics data, content management, anything where speed matters more than perfect consistency.

**Examples**: DynamoDB Global Tables, MongoDB Atlas, PostgreSQL logical replication.

### The CAP Theorem in Practice

You've probably heard of the CAP theorem: you can't have Consistency, Availability, and Partition tolerance all at once. Pick two.

In multi-region architecture, you're always dealing with partitions (network between regions can fail). So you choose:

**CP (Consistency + Partition Tolerance)**: Strong consistency, but system becomes unavailable during network partitions. Example: Google Spanner.

**AP (Availability + Partition Tolerance)**: System stays available during partitions, but data might be inconsistent. Example: DynamoDB, Cassandra.

There's no "right" answer. It depends on your use case.

[Need examples: bank account balance (CP) vs social media likes (AP)]

## Traffic Routing and Failover

You have servers in multiple regions. How do users reach them? How do you failover when a region dies?

### DNS-Based Routing (Route 53, CloudFlare)

**How It Works**: DNS returns different IP addresses based on health checks and routing policies.

**Pros**:
- Simple to implement
- Works with any application
- No code changes needed
- Cheap

**Cons**:
- DNS caching (TTL means slow failover)
- Client-side caching (browsers, OS, apps)
- Health check delays (30-60 seconds to detect failure)

**Failover Time**: 1-5 minutes (depends on TTL)

**Configuration**:
```yaml
# Route 53 Health Check
HealthCheck:
  Type: HTTPS
  ResourcePath: /health
  FailureThreshold: 3
  RequestInterval: 30
  
# Failover Routing Policy
RecordSet:
  Type: A
  SetIdentifier: Primary
  Failover: PRIMARY
  HealthCheckId: !Ref HealthCheck
  TTL: 60  # Lower TTL = faster failover, more DNS queries
```

**When to Use**: Simple applications, acceptable failover time (minutes), cost-sensitive.

### Global Load Balancers (AWS Global Accelerator)

**How It Works**: Anycast routing to nearest healthy region. Traffic goes to AWS edge locations, then routed to healthy backend.

**Pros**:
- Fast failover (seconds, not minutes)
- No DNS caching issues
- Health checks at network layer
- Better performance (AWS backbone network)

**Cons**:
- More expensive ($0.025/hour + $0.015/GB)
- AWS-specific (vendor lock-in)
- More complex setup

**Failover Time**: 30-60 seconds

**When to Use**: Low-latency requirements, fast failover needed, AWS-committed architecture.

### Application-Level Routing (Service Mesh)

**How It Works**: Application code or service mesh decides which region to use based on health, latency, user affinity.

**Pros**:
- Most control (custom routing logic)
- Fastest failover (milliseconds)
- Can do smart routing (user affinity, data locality)
- Can route different requests differently

**Cons**:
- Most complex
- Requires code changes or service mesh
- Harder to test
- More operational burden

**Failover Time**: Milliseconds to seconds

**When to Use**: Complex routing requirements, need for user affinity, microservices architecture with service mesh.

## Cost Analysis: The Honest Numbers

Let's talk real numbers. Multi-region is expensive.

### Infrastructure Costs

| Architecture | Monthly Cost | Increase | Notes |
|--------------|--------------|----------|-------|
| Single Region | $10,000 | Baseline | All resources in one region |
| Active-Passive | $13,000 | +30% | Standby at 20% capacity |
| Active-Active | $20,000 | +100% | Both regions at full capacity |

### Data Transfer Costs

Cross-region data transfer is where costs explode:

| Scenario | Data Transfer | Monthly Cost |
|----------|---------------|--------------|
| Async replication (1TB/day) | 30TB/month | $600 |
| Sync replication (1TB/day) | 60TB/month | $1,200 |
| Active-active (10TB/day) | 300TB/month | $6,000 |

AWS charges $0.02/GB for cross-region transfer. If you're doing active-active with high traffic, data transfer can cost more than compute.

### Break-Even Analysis

**Question**: When is multi-region worth it?

**Math**:
- Multi-region cost: $10,000/month extra (active-passive)
- Downtime cost: $X per hour
- Break-even: If you prevent Y hours of downtime per year

If downtime costs $100,000/hour:
- Multi-region costs $120,000/year
- Break-even: Prevent 1.2 hours of downtime per year
- That's 6 minutes per month

If downtime costs $10,000/hour:
- Break-even: Prevent 12 hours per year
- That's 1 hour per month

If downtime costs $1,000/hour:
- Break-even: Prevent 120 hours per year
- That's 10 hours per month

**The Decision**: If your downtime costs less than $10K/hour, multi-region probably isn't worth it. Focus on good backups and fast recovery instead.

## Disaster Recovery Testing

You can't know if your multi-region architecture works until you test it. And I mean really test it.

### Regional Failover Drills

**The Process**:
1. **Announce the drill** (don't surprise your team or customers)
2. **Block traffic to primary region** (firewall rules, not actual shutdown)
3. **Observe what breaks** (monitoring, logs, customer reports)
4. **Fix what breaks** (update runbooks, fix dependencies)
5. **Document lessons learned** (post-mortem, action items)
6. **Repeat quarterly** (systems change, new dependencies appear)

**What You'll Discover**:
- Hidden dependencies on primary region
- Services that don't failover correctly
- Data replication lag issues
- Monitoring blind spots (alerts that don't fire)
- Runbook gaps (steps that don't work)
- Team knowledge gaps (who knows how to failover?)

**Real Example**: A company did their first failover drill and discovered their secondary region's database was 3 hours behind primary. They thought it was real-time replication. It wasn't. They found out during a drill, not during a real outage.

### Chaos Engineering for Regions

Use AWS Fault Injection Simulator or similar tools to:
- Terminate all instances in a region
- Block network traffic between regions
- Simulate DNS failures
- Inject latency in cross-region calls
- Fail over databases

[Reference Part 2 on chaos engineering for more details]

## Real-World Multi-Region Architectures

### Netflix: Global Active-Active

Netflix runs active-active across three AWS regions (us-east-1, us-west-2, eu-west-1).

**Their Strategy**:
- Stateless services (no session affinity needed)
- Cassandra for multi-region data (eventual consistency)
- EVCache for distributed caching
- Zuul for intelligent routing
- Chaos engineering to validate resilience

**During us-east-1 Outage**: Their edge services (CDN, API gateway) continued working because they're truly distributed. Some backend services failed, but customer-facing services stayed up.

**The Lesson**: Stateless architecture makes multi-region easier. Push state to the edges (CDN, client-side).

### Stripe: Payment Processing Across Regions

Stripe runs active-passive with fast failover.

**Their Strategy**:
- Primary region handles all writes
- Secondary region ready for fast failover
- Synchronous replication for payment data (can't lose transactions)
- Asynchronous replication for analytics data
- Automated failover with manual approval

**The Lesson**: Different data needs different replication strategies. Critical data (payments) gets sync replication. Non-critical data (analytics) gets async.

## The Tradeoffs Nobody Talks About

Let me be honest: Multi-region is hard, expensive, and often not worth it.

**When You Need Multi-Region**:
- Downtime costs >$50K/hour
- Regulatory requirements (data residency)
- Global user base (latency matters)
- High-profile service (reputation matters)
- SLAs with financial penalties

**When You Don't Need Multi-Region**:
- Startup with <$5M revenue
- Internal tools
- Downtime is annoying but not catastrophic
- Budget constraints
- Small team (can't manage complexity)

**The Middle Ground**:
- Start single-region
- Build for multi-region (but don't deploy it yet)
- Have good backups and disaster recovery plan
- Test recovery quarterly
- Deploy multi-region when revenue justifies cost

Most companies should focus on good backups, fast recovery, and graceful degradation before investing in multi-region.

## Conclusion

The day AWS went down, some companies survived and some didn't. The difference wasn't luck. It was architecture.

But multi-region isn't a silver bullet. It's expensive, complex, and often overkill. The question isn't "should we be multi-region?" It's "what level of resilience do we actually need?"

**Start here**:
1. Calculate your downtime cost (be honest)
2. Identify hidden single points of failure
3. Implement good backups and test recovery
4. Build graceful degradation (Part 4)
5. Consider multi-region only when the math makes sense

**Coming up**: In Part 6, we'll explore rate limiting and backpressure — how to protect your systems from themselves when traffic spikes.

Target: ~2,500 words (this is getting fleshed out, will be complete in v3)
