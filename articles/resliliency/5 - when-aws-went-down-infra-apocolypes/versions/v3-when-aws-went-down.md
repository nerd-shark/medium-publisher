---
title: "The Day AWS Went Down: Building Systems That Survive Infrastructure Apocalypse"
subtitle: "December 7, 2021. AWS us-east-1 goes dark. Netflix, Disney+, Robinhood go offline. Except... some don't. What did they know that you don't?"
series: "Resilience Engineering Part 5"
reading-time: "9 minutes"
target-audience: "Software architects, platform engineers, CTOs, SREs"
keywords: "multi-region architecture, disaster recovery, AWS outage, infrastructure resilience, geographic redundancy, active-active, active-passive"
status: "v3-full-prose"
created: "2026-03-08"
author: "Daniel Stauffer"
---

# The Day AWS Went Down: Building Systems That Survive Infrastructure Apocalypse

Part 5 of my series on Resilience Engineering. Last time, we explored graceful degradation — what to do when all your fallbacks fail simultaneously. This time: what happens when your entire cloud provider goes dark, and how to build systems that survive infrastructure disasters. Follow along for more deep dives into building systems that don't fall apart.

## The AWS Apocalypse

December 7, 2021. 10:45 AM EST. AWS us-east-1 starts having "issues."

Within 30 minutes, the internet is on fire. Netflix goes dark. Disney+ stops streaming. Robinhood freezes trading. Ring doorbells stop recording. Even Roomba vacuums lose connection to their cloud brains. Thousands of websites return 503 errors. The AWS status page — ironically hosted in us-east-1 — struggles to load.

The outage lasts 5 hours. Estimated economic impact: over $100 million in lost revenue across affected companies. Customer trust damage: immeasurable.

But here's what's interesting: Some companies stayed online. Amazon.com kept selling products. Parts of Netflix continued streaming. AWS Console (the tool you use to manage AWS) mostly worked. These companies had something the others didn't: real multi-region architecture.

This wasn't AWS's first rodeo. us-east-1 has gone down multiple times before. It won't be the last. The question isn't "will your cloud provider fail?" It's "when it fails, will you survive?"

## The us-east-1 Problem

Here's the dirty secret about AWS: us-east-1 isn't just another region. It's THE region.

Everyone uses us-east-1 because new services launch here first (sometimes exclusively for 6-12 months), pricing is cheapest (10-20% less than other regions), and it has the lowest latency to major US population centers. It's the oldest, most mature infrastructure with the best third-party integration support.

But us-east-1 is also dangerous. Control plane APIs for many services live here. IAM is "global" but actually runs in us-east-1. Route 53 health checks originate primarily from us-east-1. CloudFront has special dependencies on us-east-1. Many AWS services have hidden us-east-1 dependencies that aren't documented.

So even if you think you're "multi-region," you probably depend on us-east-1 for something critical. This is the hidden single point of failure in cloud-native architecture.

Your architecture diagram shows applications running in three regions. But all three regions have arrows pointing back to us-east-1 for IAM, control plane APIs, and shared services. When us-east-1 goes down, everything goes down.

## Real Disaster Stories

### AWS us-east-1 Outage (December 7, 2021)

AWS's internal network device management system failed. A routine automation to scale capacity triggered a bug that cascaded through the network control plane. The failure lasted 5 hours for full recovery, though some services were impacted for over 11 hours.

Thousands of websites and services went offline. Major companies affected included Netflix, Disney+, Robinhood, Coinbase, and Epic Games. Services that use AWS but don't advertise it — Ring doorbells, Roomba vacuums, countless IoT devices — all stopped working. Even AWS's own services struggled. The Console, CloudWatch, and some API endpoints were partially or completely unavailable.

Who stayed up? Companies with true active-active multi-region architectures that didn't depend on the us-east-1 control plane for runtime operations. Amazon.com retail stayed mostly functional. Netflix's CDN edge services continued serving cached content to users.

The lesson: Control plane versus data plane matters. Your application might run in us-west-2, but if it depends on us-east-1 APIs for anything at runtime, you're vulnerable.

### The OVH Datacenter Fire (March 10, 2021)

A datacenter in Strasbourg, France literally caught fire and burned down. Not a metaphor. Actual fire. The building was destroyed.

The impact was catastrophic for unprepared companies. 3.6 million websites went offline. Complete data loss for customers without backups. Some companies lost everything — no backups, no disaster recovery, no business. An estimated 464,000 domains were affected.

Who survived? Companies with backups in different datacenters. Companies with multi-region architecture. Companies who took disaster recovery seriously and tested their recovery procedures.

The lesson: "The cloud" is just someone else's computer. And computers can catch fire. Physical disasters happen. If you don't have backups outside the datacenter, you can lose everything.

### Azure DNS Outage (April 1, 2021)

Azure's DNS service went down globally for 3 hours due to a configuration change. If DNS doesn't work, nothing works. Your multi-region architecture is useless if nobody can find it. Services were running fine, but users couldn't reach them because DNS resolution failed.

The lesson: DNS is the ultimate single point of failure. Even if your application is perfectly distributed across regions, DNS can take you down. You need DNS redundancy and monitoring.

### GCP Networking Outage (June 2, 2019)

Google's network configuration change caused a cascading failure across multiple regions. The outage lasted 4 hours. YouTube, Gmail, Google Cloud services, and many customer applications went offline.

The lesson: Even Google, who invented modern distributed systems, can take themselves down with a bad configuration change. Nobody is immune to infrastructure failures. The best engineers in the world still make mistakes.

## Why "Multi-Region" Is Usually a Lie

Your architecture diagram shows servers in three regions. Your marketing says "multi-region resilient architecture." Your status page promises "99.99% uptime."

Then us-east-1 goes down and you're completely offline. What happened?

### Hidden Dependency #1: Control Plane vs Data Plane

Your application code runs in us-west-2. This is the data plane — the part that serves customer requests. It's working fine.

But the control plane — the APIs that manage your infrastructure — runs in us-east-1. When us-east-1 goes down, your app keeps running, but you can't scale (auto-scaling API is down), can't deploy (CI/CD uses control plane APIs), can't update security groups, can't create new resources, and can't even see what's happening (CloudWatch API is down).

Your app runs fine until something needs to change. Then you're stuck. It's like having a car that runs fine but you can't steer or brake. Great until you need to turn.

### Hidden Dependency #2: IAM Lives in us-east-1

IAM is "global," right? Not exactly. IAM's control plane lives in us-east-1. When us-east-1 goes down, existing authentication tokens work because they're cached. But new authentication fails because you can't reach IAM. Token refresh fails after the TTL expires (typically 1 hour for temporary credentials). Service-to-service authentication breaks.

Your services in us-west-2 can't authenticate to each other. You have about 1 hour before everything stops working.

### Hidden Dependency #3: Your Database Is in One Region

You have application servers in three regions. Excellent! Your database is in us-east-1. Not excellent.

When us-east-1 goes down, your servers in us-west-2 and eu-west-1 can't reach the database. You're down everywhere, despite having servers in multiple regions. This is the most common mistake: multi-region compute with single-region data.

### Hidden Dependency #4: Shared Services

Even if your app and database are multi-region, you probably have shared services in one region: Redis cache, message queue, Elasticsearch cluster, monitoring and logging infrastructure. Any single-region shared service is a single point of failure.

## Active-Active vs Active-Passive: The Real Tradeoffs

There are two ways to do multi-region: active-active (both regions serve traffic) and active-passive (one region on standby). Each has serious tradeoffs that nobody talks about.

### Active-Active: The Expensive Option

In active-active architecture, both regions run at full capacity and both serve production traffic. Traffic is distributed between them using DNS, global load balancers, or application-level routing.

The benefits are real. You get true redundancy — if one region dies, the other handles all traffic. There's no failover delay because traffic just shifts. You get better global latency because users hit the nearest region. And failover is tested constantly because both regions are always serving traffic.

But the costs are brutal. You're paying for 2x infrastructure because both regions run at full capacity. That's $20,000/month instead of $10,000. Data consistency becomes hard because two regions are writing to databases simultaneously. You need to handle split-brain scenarios where regions can't talk to each other. You need conflict resolution for when the same record is updated in both regions. And you're paying for cross-region data transfer every time regions need to sync.

A typical cost breakdown: single region costs $10,000/month. Active-active costs $20,000/month for infrastructure (100% increase) plus $2,000-5,000/month for cross-region data transfer. You're looking at $22,000-25,000/month total.

When should you use active-active? High-value services where downtime costs more than infrastructure. Financial services where minutes of downtime cost millions. E-commerce during peak season. SaaS products with strict SLAs and financial penalties for downtime.

When should you NOT use active-active? Cost-sensitive applications where infrastructure is a major expense. Write-heavy workloads with strong consistency requirements. Startups burning through runway where every dollar matters.

### Active-Passive: The Cheaper Option

In active-passive architecture, the primary region serves all traffic while the secondary region is on standby. The standby can be warm (running minimal resources) or cold (shut down until needed). You failover to the secondary when the primary fails.

The benefits are cost and simplicity. The standby region runs at 20-30% capacity, so you're only paying $13,000/month instead of $20,000. Data consistency is simpler because only one region writes. You don't have split-brain scenarios. The architecture is easier to reason about and debug.

But failover takes time. Warm standby might take 5-10 minutes to scale up and start serving traffic. Cold standby might take 30-60 minutes. Failover is either manual (slow, error-prone) or automated (fast, but scary when it triggers unexpectedly). The standby might not work when you need it — when did you last test it? And there's data replication lag, so the standby is always slightly behind the primary.

A typical cost breakdown: single region costs $10,000/month. Active-passive costs $13,000/month total — $10,000 for primary, $2,000 for standby at minimal capacity, $1,000 for data replication.

When should you use active-passive? Cost-sensitive applications where infrastructure is a major expense. Applications where minutes to hours of downtime is acceptable. Infrequent failures where the cost of active-active isn't justified. Write-heavy workloads where active-active would create consistency nightmares.

When should you NOT use active-passive? Zero-downtime requirements where even minutes of downtime is unacceptable. High-frequency trading or real-time systems. Services where minutes of downtime cost millions in lost revenue.

## Data Replication: The Hard Part

Multi-region compute is easy. Spin up servers in multiple regions. Done. Multi-region data is hard. Really hard.

### Synchronous Replication: Strong Consistency

In synchronous replication, a write goes to both regions before acknowledging success. The transaction commits only when both regions confirm they've written the data.

The benefit is zero data loss. Both regions are always in sync. You get strong consistency — reads always see the latest writes. You don't need conflict resolution because there are no conflicts.

But the cost is latency. Every write waits for a cross-region network round trip. us-east-1 to us-west-2 is about 70ms round trip. us-east-1 to eu-west-1 is about 90ms. us-east-1 to ap-southeast-1 is about 250ms. Every single write adds this latency.

If you're doing 100 writes per second, that's 100 operations each waiting 70ms. Your system's write throughput is now limited by cross-region latency. And if one region goes down, writes fail completely because you can't commit to both regions.

When should you use synchronous replication? Financial transactions where you absolutely cannot lose data. Inventory management where consistency is critical. Anything where data accuracy matters more than speed.

Examples include Google Spanner, CockroachDB, and AWS Aurora Global Database with synchronous replication enabled.

### Asynchronous Replication: Eventual Consistency

In asynchronous replication, a write goes to the primary region, acknowledges immediately, and replicates to the secondary in the background.

The benefit is low latency. Writes don't wait for replication. You get high availability because primary region failure doesn't block writes. And it's cheaper because you're doing less cross-region traffic.

But you have data loss risk. If the primary fails before replication completes, you lose any writes from the last few seconds. You get eventual consistency — reads might see stale data. And you need conflict resolution for when both regions get writes during a network partition.

Typical replication lag is 1-5 seconds under normal conditions. Under load, it might be 10-30 seconds. During network issues, it could be minutes to hours. If the primary region fails, you lose any writes from the last N seconds.

When should you use asynchronous replication? Social media posts where losing a few seconds of data is acceptable. Analytics data where eventual consistency is fine. Content management systems. Anything where speed matters more than perfect consistency.

Examples include DynamoDB Global Tables, MongoDB Atlas, and PostgreSQL logical replication.

### The CAP Theorem in Practice

The CAP theorem says you can't have Consistency, Availability, and Partition tolerance all at once. Pick two.

In multi-region architecture, you're always dealing with partitions because the network between regions can fail. So you choose between CP (Consistency + Partition Tolerance) or AP (Availability + Partition Tolerance).

CP systems like Google Spanner prioritize consistency. During a network partition, the system becomes unavailable rather than serving inconsistent data. This is right for bank account balances where showing the wrong balance is worse than showing an error.

AP systems like DynamoDB and Cassandra prioritize availability. During a network partition, the system stays available but data might be inconsistent. This is right for social media likes where showing a slightly wrong count is better than showing an error.

There's no "right" answer. It depends on your use case. Bank account balance? CP. Social media likes? AP. Shopping cart? Probably AP. Order confirmation? Probably CP.

## Traffic Routing and Failover

You have servers in multiple regions. How do users reach them? How do you failover when a region dies?

### DNS-Based Routing

DNS-based routing uses Route 53, CloudFlare, or similar services to return different IP addresses based on health checks and routing policies.

The benefits are simplicity and cost. It's simple to implement, works with any application, requires no code changes, and is cheap. You just configure DNS records with health checks and failover policies.

But DNS caching makes failover slow. DNS records have a TTL (Time To Live). Even if you set TTL to 60 seconds, clients might cache longer. Browsers cache. Operating systems cache. Applications cache. Health checks take 30-60 seconds to detect failure. Total failover time is typically 1-5 minutes.

Here's a basic Route 53 configuration:

```yaml
HealthCheck:
  Type: HTTPS
  ResourcePath: /health
  FailureThreshold: 3
  RequestInterval: 30
  
RecordSet:
  Type: A
  SetIdentifier: Primary
  Failover: PRIMARY
  HealthCheckId: !Ref HealthCheck
  TTL: 60
```

Lower TTL means faster failover but more DNS queries (higher cost and load). Higher TTL means slower failover but fewer queries.

When should you use DNS-based routing? Simple applications where 1-5 minutes of failover time is acceptable. Cost-sensitive applications where every dollar matters. Applications without complex routing requirements.

### Global Load Balancers

Global load balancers like AWS Global Accelerator use Anycast routing to send traffic to the nearest healthy region. Traffic goes to AWS edge locations, then gets routed to healthy backends over the AWS backbone network.

The benefits are speed and reliability. Failover happens in 30-60 seconds, not minutes. There are no DNS caching issues. Health checks happen at the network layer. And you get better performance because traffic uses the AWS backbone network instead of the public internet.

But it's more expensive. AWS Global Accelerator costs $0.025/hour plus $0.015/GB of data transfer. For a service transferring 10TB/month, that's $18/month for the accelerator plus $150/month for data transfer. And it's AWS-specific, so you're locked into AWS.

When should you use global load balancers? Applications with low-latency requirements. Applications where fast failover is critical. AWS-committed architectures where vendor lock-in isn't a concern.

### Application-Level Routing

Application-level routing means your application code or service mesh decides which region to use based on health, latency, user affinity, or custom logic.

The benefits are control and speed. You have the most control with custom routing logic. Failover happens in milliseconds to seconds. You can do smart routing like sending users to the region where their data lives. You can route different requests differently based on business logic.

But it's the most complex option. It requires code changes or deploying a service mesh. It's harder to test because routing logic is distributed. And there's more operational burden because you're managing routing yourself.

When should you use application-level routing? Complex routing requirements that DNS or load balancers can't handle. Need for user affinity where users should stick to specific regions. Microservices architectures with service mesh already deployed.

## Cost Analysis: The Honest Numbers

Let's talk real numbers. Multi-region is expensive, and most companies underestimate the cost.

### Infrastructure Costs

Single region: $10,000/month baseline. All resources in one region.

Active-passive: $13,000/month (+30%). Primary region at full capacity ($10,000), standby region at 20% capacity ($2,000), data replication ($1,000).

Active-active: $20,000/month (+100%). Both regions at full capacity ($10,000 each).

### Data Transfer Costs

This is where costs explode. AWS charges $0.02/GB for cross-region data transfer.

Asynchronous replication with 1TB/day of changes: 30TB/month = $600/month.

Synchronous replication with 1TB/day (round trip): 60TB/month = $1,200/month.

Active-active with 10TB/day of traffic between regions: 300TB/month = $6,000/month.

If you're doing active-active with high traffic, data transfer can cost more than compute.

### Break-Even Analysis

When is multi-region worth it? Do the math.

If downtime costs $100,000/hour and multi-region costs $10,000/month extra ($120,000/year), you break even by preventing 1.2 hours of downtime per year. That's 6 minutes per month.

If downtime costs $10,000/hour, you break even by preventing 12 hours per year. That's 1 hour per month.

If downtime costs $1,000/hour, you break even by preventing 120 hours per year. That's 10 hours per month.

The decision: If your downtime costs less than $10,000/hour, multi-region probably isn't worth it. Focus on good backups and fast recovery instead.

## Disaster Recovery Testing

You can't know if your multi-region architecture works until you test it. And I mean really test it, not just check that servers are running.

### Regional Failover Drills

Run quarterly failover drills. Announce the drill so you don't surprise your team or customers. Block traffic to the primary region using firewall rules (don't actually shut it down). Observe what breaks — monitoring, logs, customer reports. Fix what breaks and update runbooks. Document lessons learned in a post-mortem. Then do it again next quarter because systems change and new dependencies appear.

What you'll discover: hidden dependencies on the primary region, services that don't failover correctly, data replication lag issues, monitoring blind spots where alerts don't fire, runbook gaps where documented steps don't work, and team knowledge gaps where nobody knows how to failover.

Real example: A company did their first failover drill and discovered their secondary region's database was 3 hours behind primary. They thought it was real-time replication. It wasn't. They found out during a drill, not during a real outage. The drill saved them from a disaster.

### Chaos Engineering for Regions

Use AWS Fault Injection Simulator or similar tools to inject failures. Terminate all instances in a region. Block network traffic between regions. Simulate DNS failures. Inject latency in cross-region calls. Fail over databases.

The goal isn't to break things. It's to discover what breaks before customers do. Every failure you find in testing is a failure you won't have in production.

## Real-World Multi-Region Architectures

### Netflix: Global Active-Active

Netflix runs active-active across three AWS regions: us-east-1, us-west-2, and eu-west-1.

Their strategy: stateless services with no session affinity needed. Cassandra for multi-region data with eventual consistency. EVCache for distributed caching. Zuul for intelligent routing. And constant chaos engineering to validate resilience.

During the us-east-1 outage, their edge services (CDN, API gateway) continued working because they're truly distributed. Some backend services failed, but customer-facing services stayed up. Most users didn't notice.

The lesson: Stateless architecture makes multi-region easier. Push state to the edges (CDN, client-side) and keep services stateless.

### Stripe: Payment Processing Across Regions

Stripe runs active-passive with fast failover.

Their strategy: primary region handles all writes. Secondary region is ready for fast failover. Synchronous replication for payment data because they can't lose transactions. Asynchronous replication for analytics data. Automated failover with manual approval for safety.

The lesson: Different data needs different replication strategies. Critical data (payments) gets synchronous replication. Non-critical data (analytics) gets asynchronous replication.

## The Tradeoffs Nobody Talks About

Let me be honest: Multi-region is hard, expensive, and often not worth it.

When you need multi-region: Downtime costs more than $50,000/hour. Regulatory requirements mandate data residency in multiple regions. You have a global user base where latency matters. You're a high-profile service where reputation matters. You have SLAs with financial penalties for downtime.

When you don't need multi-region: You're a startup with less than $5 million in revenue. You're building internal tools. Downtime is annoying but not catastrophic. You have budget constraints. You have a small team that can't manage the complexity.

The middle ground: Start single-region. Build your architecture to be multi-region capable (stateless services, externalized configuration, no hard-coded region dependencies) but don't deploy it yet. Have good backups and a disaster recovery plan. Test recovery quarterly. Deploy multi-region when revenue justifies the cost.

Most companies should focus on good backups, fast recovery, and graceful degradation (see Part 4) before investing in multi-region.

## What to Do Monday Morning

The day AWS went down, some companies survived and some didn't. The difference wasn't luck. It was architecture.

But multi-region isn't a silver bullet. It's expensive, complex, and often overkill. The question isn't "should we be multi-region?" It's "what level of resilience do we actually need?"

Start here:

First, calculate your downtime cost. Be honest. How much revenue do you lose per hour of downtime? How much does it cost to recover? How much customer trust do you lose?

Second, identify hidden single points of failure. Map your dependencies. What happens if us-east-1 goes down? What happens if your database region fails? What happens if DNS fails?

Third, implement good backups and test recovery. Can you restore from backup? How long does it take? When did you last test it?

Fourth, build graceful degradation. When things fail, can you serve cached data? Can you operate in read-only mode? Can you show users something instead of nothing?

Fifth, consider multi-region only when the math makes sense. If downtime costs justify the expense, do it. If not, focus on faster recovery.

The goal isn't to survive every possible disaster. It's to survive the disasters that are likely to happen and recover quickly from the ones you can't prevent.

---

**Coming up**: In Part 6, we'll explore rate limiting and backpressure — how to protect your systems from themselves when traffic spikes 10x overnight.

**Resources**:
- AWS Well-Architected Framework: Reliability Pillar
- Google SRE Book: Chapter on Managing Load
- Netflix Tech Blog: Multi-Region Architecture
- Stripe Engineering Blog: Payment System Resilience

---

*This is Part 5 of the Resilience Engineering series. Read [Part 1: Cell-Based Architecture](link), [Part 2: Chaos Engineering](link), [Part 3: The $10M Blind Spot](link), and [Part 4: When Everything Fails](link).*
