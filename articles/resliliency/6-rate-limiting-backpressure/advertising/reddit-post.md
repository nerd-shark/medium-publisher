# Reddit Post

**Article**: Rate Limiting and Backpressure: Protecting Systems from Themselves
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Suggested Subreddits

- r/programming
- r/softwarearchitecture
- r/devops
- r/sre
- r/ExperiencedDevs
- r/aws
- r/webdev
- r/Backend
- r/microservices
- r/cloudcomputing

---

## Post Title

Rate Limiting and Backpressure: What Walmart's Black Friday crash teaches about systems that never learned to say "no"

---

## Post Body

Black Friday 2018. Walmart.com buckles under a traffic surge. 3.6 million shoppers affected, roughly $9 million in estimated lost sales. Lowe's, J.Crew, Best Buy, and Office Depot all went down that same weekend.

The root cause across all of them wasn't a bug. It was the absence of rate limiting and backpressure. The systems accepted every request, tried to serve every user, and drowned trying.

I wrote a deep dive into rate limiting algorithms, backpressure patterns, and load shedding — the mechanisms that teach systems to protect themselves from overwhelming traffic.

**Key points:**

**The retry storm death spiral:** Traffic spikes → response times climb → users refresh (2x load) → mobile apps auto-retry (3x load) → connection pools fill → everything crashes. A healthy system at 10:00 AM can be dead by 10:03 AM. Rate limiting breaks this loop. Backpressure propagates "slow down" through the chain.

**5 rate limiting algorithms compared:**

1. **Token Bucket** — Handles bursts, minimal memory (2 numbers per client). Used by Stripe, AWS API Gateway, GitHub. Handles 90% of use cases. Start here.
2. **Leaky Bucket** — Constant rate, no bursts reach backend. Shopify uses this with cost-based weighting where a bulk query costs more "tokens" than a single lookup.
3. **Fixed Window Counter** — Dead simple, one counter per client. Has boundary burst vulnerability but often good enough in practice.
4. **Sliding Window Counter** — Best balance of accuracy and efficiency. Used by Cloudflare and most Redis-based rate limiters. Weighted average of current and previous window.
5. **Sliding Window Log** — Most accurate, highest memory. 60K timestamps per client per minute at 1K req/s. Only for financial/compliance APIs.

**The unbounded queue trap:** Every queue has a limit. It's either the limit you set or the amount of available memory. The difference is whether you handle it gracefully with a clear error message, or catastrophically with an OOM crash at 3 AM. Make queues small. Force producers to slow down.

**Load shedding — choosing what to sacrifice:** Amazon disables recommendations and personalization during Prime Day to protect checkout. Users see generic pages but can still buy things. Revenue is protected. The hard part isn't implementing it — it's deciding what to shed. That's a business conversation, not an engineering one.

**Defense in depth — rate limit at every layer:**
- Edge (CDN/WAF): per-IP, DDoS, bot filtering
- API Gateway: per-client with API keys/OAuth, business-level limits
- Service Mesh: per-service, prevents internal cascade failures
- Application: connection pools, thread pools, bounded queues

**Distributed rate limiting:** Single server is trivial. Multiple servers need shared state (usually Redis). But Redis becomes a dependency — if it goes down, do you fail open (allow all traffic) or fail closed (reject all)? For most systems, fail open is correct. Losing rate limiting temporarily is better than a total outage.

**The response format matters more than you think:** Always return 429 with Retry-After header. Without it, clients retry immediately, creating the exact retry storm you're trying to prevent. Never return 500 for rate limiting. Never silently drop connections.

**Real-world comparison table:**

| Service | Limit | Algorithm | Notes |
|---------|-------|-----------|-------|
| Stripe | 100 req/s per key | Token bucket | Separate read/write limits |
| GitHub | 5,000 req/hr (auth) | Sliding window | 60/hr unauthenticated |
| Shopify | 40 req/s (Plus) | Leaky bucket | Cost-based (complex ops cost more) |
| Cloudflare | Configurable | Sliding window | Edge-level, per-zone |
| AWS API GW | Configurable | Token bucket | Per-stage, per-method |

**The tradeoffs nobody talks about:** Too aggressive and legitimate users get blocked — I've seen companies lose more revenue from overly aggressive rate limiting than from the traffic spike they were preventing. Too lenient and the limits don't protect anything. Per-IP punishes corporate NATs. Per-user requires auth. Every approach has blind spots.

The article includes code examples (Python token bucket implementation), algorithm comparisons, DDoS protection strategies, and a 4-week implementation plan.

I've been building distributed systems for 15+ years and have seen the retry storm death spiral more times than I'd like to admit. Happy to discuss implementation details, algorithm tradeoffs, or specific production challenges in the comments.

[ARTICLE URL]

---

**Format**:
- No hashtags (Reddit doesn't use them)
- Conversational, authentic tone
- Detailed technical summary with specific numbers
- Invites discussion
- Establishes credibility without being salesy
- Direct link to article

**Posting Strategy**:
- Post during peak hours (9-11 AM or 6-8 PM EST)
- Engage with comments within first hour
- Be ready to discuss algorithm tradeoffs in detail
- Don't be defensive if someone prefers a different approach
- Share war stories in comment threads
