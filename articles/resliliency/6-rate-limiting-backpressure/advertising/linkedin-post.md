# LinkedIn Post

**Article**: Rate Limiting and Backpressure: Protecting Systems from Themselves
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

Black Friday 2018. Walmart.com buckles under a massive traffic surge.

3.6 million shoppers affected. ~$9 million in lost sales. And Walmart wasn't alone — Lowe's, J.Crew, Best Buy, and Office Depot all went down that same weekend.

The root cause wasn't a bug. It was the absence of a simple word: "no."

Part 6 of my Resilience Engineering series.

━━━━━━━━━━━━━━━━

THE RETRY STORM DEATH SPIRAL

Traffic increases → response times climb → users refresh → load doubles → mobile apps retry → load triples → connection pools fill → everything crashes.

A healthy system at 10:00 AM can be completely dead by 10:03 AM.

Rate limiting breaks this loop. Backpressure propagates "slow down" through the chain.

━━━━━━━━━━━━━━━━

5 RATE LIMITING ALGORITHMS

🪣 Token Bucket — Handles bursts, minimal memory. Used by AWS, Stripe, GitHub. Start here.
🚰 Leaky Bucket — Constant rate, no bursts. Used by Shopify with cost-based weighting.
📊 Fixed Window — Dead simple, boundary burst vulnerability. Often good enough.
📈 Sliding Window — Best balance of accuracy and efficiency. Used by Cloudflare, Redis.
📋 Sliding Window Log — Most accurate, highest memory. For financial/compliance APIs only.

━━━━━━━━━━━━━━━━

BACKPRESSURE: THE INTERNAL IMMUNE SYSTEM

Rate limiting says "no" at the front door. Backpressure manages traffic already inside.

The unbounded queue trap: every queue has a limit. It's either the limit you set or the amount of available memory. The difference is whether you handle it gracefully or catastrophically at 3 AM.

━━━━━━━━━━━━━━━━

LOAD SHEDDING: CHOOSING WHAT TO SACRIFICE

Not all requests are equal.

Amazon disables recommendations and personalization during Prime Day to protect checkout. Users see generic pages but can still buy things. Revenue is protected.

The hard part isn't implementing load shedding — it's deciding what to shed. That's a business conversation, not an engineering one.

━━━━━━━━━━━━━━━━

WHAT TO DO MONDAY

Week 1: Rate limit your API gateway. Token bucket, 100 req/s per client. Return 429 with Retry-After.
Week 2: Bound all internal queues. No queue should be unlimited.
Week 3: Priority queuing for critical paths. Identify top 3 revenue endpoints.
Week 4: Load test with rate limiting enabled. Simulate 10x traffic.

Your system's job isn't to accept every request. It's to serve as many as it can, well, and gracefully decline the rest.

Full guide with algorithms, code examples, and real-world comparisons:

[ARTICLE URL]

What's your rate limiting strategy? Drop a comment.

#ResilienceEngineering #RateLimiting #Backpressure #APIDesign #LoadShedding #DistributedSystems #SRE #DevOps #SystemDesign #CloudArchitecture #SiteReliability #Microservices #PlatformEngineering #SoftwareArchitecture #BackendEngineering #TechLeadership #CloudNative #APIGateway #TokenBucket #HighAvailability

---

**Character count**: ~2,100 (within LinkedIn's 3,000 limit)
**Hashtags**: 20
**Format**: Emoji bullets, visual separators
