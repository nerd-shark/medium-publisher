# X/Twitter Post

**Article**: The Day AWS Went Down: Building Systems That Survive Infrastructure Apocalypse
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Main Post (280 characters)

December 7, 2021: AWS us-east-1 goes down for 5 hours. $100M+ in losses.

Netflix went dark. Amazon.com stayed up.

The difference? Real multi-region architecture.

Your "multi-region" setup probably has hidden us-east-1 dependencies 🧵

[ARTICLE URL]

#AWS #CloudArchitecture

---

**Character count**: 278
**Hashtags**: 2

---

## Thread

**Tweet 1** (Main post above)

**Tweet 2/12**
The us-east-1 problem:

• New services launch here first
• Cheapest pricing (10-20% less)
• Lowest latency to US
• Best integrations

But it's also where control plane APIs, IAM, Route 53, and CloudFront dependencies live.

#ResilienceEngineering

**Tweet 3/12**
Hidden dependency #1: Control Plane vs Data Plane

Your app runs in us-west-2 (data plane).
But control plane APIs run in us-east-1.

When us-east-1 goes down:
❌ Can't scale
❌ Can't deploy
❌ Can't see metrics
✅ App still runs (until something needs to change)

**Tweet 4/12**
Hidden dependency #2: IAM

IAM is "global" but actually runs in us-east-1.

Existing tokens work (cached).
New authentication fails.
Token refresh fails after ~1 hour.

Your services in us-west-2 can't authenticate to each other.

**Tweet 5/12**
Hidden dependency #3: Single-region database

Application servers in 3 regions ✅
Database in us-east-1 ❌

When us-east-1 goes down, servers in us-west-2 and eu-west-1 can't reach the database.

You're down everywhere despite "multi-region" compute.

**Tweet 6/12**
Active-Active vs Active-Passive:

Active-Active:
• 2x cost ($20K/month)
• No failover delay
• Complex consistency
• $2-5K/month data transfer

Active-Passive:
• 1.3x cost ($13K/month)
• 5-60 min failover
• Simple consistency
• Standby might not work

**Tweet 7/12**
Data replication: The hard part

Synchronous:
✅ Zero data loss
✅ Strong consistency
❌ 70-250ms latency per write
❌ Writes fail if region down

Asynchronous:
✅ Low latency
✅ High availability
❌ 1-5 second data loss risk
❌ Eventual consistency

**Tweet 8/12**
Cost analysis nobody talks about:

If downtime costs $100K/hour:
Multi-region costs $10K/month extra
Break-even: Prevent 6 minutes of downtime per month

If downtime costs $10K/hour:
Break-even: Prevent 1 hour per month

Do the math for your business.

**Tweet 9/12**
Real disasters:

AWS us-east-1 (Dec 2021): 5 hours, $100M+ losses
OVH datacenter fire (Mar 2021): Building burned down, 3.6M sites offline
Azure DNS (Apr 2021): 3 hours, global DNS failure
GCP networking (Jun 2019): 4 hours, YouTube/Gmail down

Nobody is immune.

**Tweet 10/12**
Netflix's strategy:

• Active-active across 3 regions
• Stateless services
• Cassandra for multi-region data
• EVCache for distributed caching
• Constant chaos engineering

During us-east-1 outage, edge services continued working.

**Tweet 11/12**
Stripe's strategy:

• Active-passive with fast failover
• Synchronous replication for payments (can't lose transactions)
• Asynchronous for analytics
• Automated failover with manual approval

Different data needs different strategies.

**Tweet 12/12**
What to do Monday:

1. Calculate your downtime cost
2. Find hidden us-east-1 dependencies
3. Test backup recovery
4. Build graceful degradation
5. Multi-region only if math works

Full guide with disaster stories, replication strategies, and cost breakdowns:

[ARTICLE URL]

---

**Thread length**: 12 tweets
**Format**: Numbered thread with clear progression
**Hashtags**: Minimal (2 in main post, 1 in thread)
