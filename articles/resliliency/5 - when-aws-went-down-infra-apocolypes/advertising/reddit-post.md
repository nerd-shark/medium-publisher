# Reddit Post

**Article**: The Day AWS Went Down: Building Systems That Survive Infrastructure Apocalypse
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Suggested Subreddits

- r/aws
- r/devops
- r/sre
- r/programming
- r/softwarearchitecture
- r/cloudcomputing
- r/kubernetes
- r/sysadmin
- r/webdev
- r/ExperiencedDevs

---

## Post Title

The Day AWS Went Down: What Netflix and Amazon knew that cost others $100M

---

## Post Body

December 7, 2021. AWS us-east-1 goes down for 5 hours.

Netflix, Disney+, Robinhood, Ring doorbells, even Roomba vacuums — all offline. Economic impact: over $100 million in losses.

But Amazon.com kept selling. Parts of Netflix continued streaming. AWS Console mostly worked.

I wrote a deep dive into what actually happened and why "multi-region" architecture is usually a lie.

**Key points:**

**The us-east-1 trap:** Everyone uses it because new services launch here first, pricing is cheapest, and latency is lowest. But it's also where control plane APIs, IAM, Route 53, and CloudFront dependencies live. Even if you think you're multi-region, you probably depend on us-east-1 for something critical.

**Hidden dependencies that will take you down:**
1. Control plane vs data plane — your app runs in us-west-2, but you can't scale/deploy/monitor when us-east-1 is down
2. IAM lives in us-east-1 — new authentication fails, token refresh fails after ~1 hour
3. Single-region database — servers in 3 regions, database in 1, you're down everywhere
4. Shared services — Redis, message queue, Elasticsearch, monitoring in one region

**Active-active vs active-passive — the real costs:**
- Active-active: $22-25K/month, instant failover, complex consistency
- Active-passive: $13K/month, 5-60 min failover, simple consistency
- Single region: $10K/month, hours to days recovery

**The math:** If downtime costs $100K/hour, multi-region costs $10K/month extra. Break-even: prevent 6 minutes of downtime per month. If downtime costs $10K/hour, break-even is 1 hour per month. Most companies should focus on good backups and fast recovery before investing in multi-region.

**Real disasters covered:**
- AWS us-east-1 (Dec 2021): 5 hours, $100M+ losses
- OVH datacenter fire (Mar 2021): Building literally burned down, 3.6M sites offline
- Azure DNS (Apr 2021): 3 hours, global DNS failure
- GCP networking (Jun 2019): 4 hours, YouTube/Gmail down

**What Netflix and Stripe do differently:**
- Netflix: Active-active across 3 regions, stateless services, Cassandra for multi-region data, constant chaos engineering
- Stripe: Active-passive with fast failover, synchronous replication for payments, asynchronous for analytics

The article includes detailed breakdowns of:
- Data replication strategies (synchronous vs asynchronous)
- Traffic routing and failover (DNS, global load balancers, application-level)
- Cost analysis with real numbers
- Disaster recovery testing approaches
- When multi-region is worth it (and when it's not)

I've been building distributed systems for 15+ years and learned most of these lessons the expensive way. Happy to answer questions in the comments.

[ARTICLE URL]

---

**Format**: 
- No hashtags (Reddit doesn't use them)
- Conversational, authentic tone
- Detailed summary with specific takeaways
- Invites discussion
- Establishes credibility without being salesy
- Direct link to article

**Posting Strategy**:
- Post during peak hours (9-11 AM or 6-8 PM EST)
- Engage with comments within first hour
- Provide additional context/answers in comments
- Don't be defensive if criticized
- Share relevant experience in comment threads
