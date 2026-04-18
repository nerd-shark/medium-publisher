# X/Twitter Post

**Article**: Rate Limiting and Backpressure: Protecting Systems from Themselves
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Main Post (280 characters)

Black Friday 2018: Walmart.com goes down. 3.6M shoppers affected. ~$9M lost.

The root cause wasn't a bug. The system never learned to say "no."

Rate limiting and backpressure — your system's immune system 🧵

[ARTICLE URL]

#RateLimiting #SystemDesign

---

**Character count**: 265
**Hashtags**: 2

---

## Thread

**Tweet 1** (Main post above)

**Tweet 2/10**
The retry storm death spiral:

Traffic spikes → response times climb → users refresh (2x load) → mobile apps retry (3x load) → connection pools fill → everything crashes

A healthy system at 10:00 AM can be dead by 10:03 AM.

Rate limiting breaks this loop.

**Tweet 3/10**
5 rate limiting algorithms:

🪣 Token Bucket — burst-friendly, minimal memory (Stripe, AWS, GitHub)
🚰 Leaky Bucket — constant rate, no bursts (Shopify)
📊 Fixed Window — simple, boundary vulnerability
📈 Sliding Window — best balance (Cloudflare)
📋 Sliding Log — most accurate, highest memory

**Tweet 4/10**
Token bucket handles 90% of use cases.

Bucket holds N tokens, refills at rate R/sec. Each request costs 1 token. Empty bucket = rejected request.

Allows bursts (real traffic is bursty) while enforcing sustained limits.

Memory: 2 numbers per client. That's it.

**Tweet 5/10**
Backpressure: the internal immune system.

Rate limiting says "no" at the front door. Backpressure manages traffic already inside.

The unbounded queue trap: every queue has a limit. It's either yours or available memory.

Make queues small. Force producers to slow down.

**Tweet 6/10**
Load shedding: choosing what to sacrifice.

Amazon during Prime Day:
❌ Recommendations disabled
❌ Personalization disabled
✅ Checkout protected
✅ Payments protected

Users see generic pages but can still buy. Revenue protected.

Decide what to shed BEFORE the crisis.

**Tweet 7/10**
Defense in depth — rate limit at every layer:

1. Edge (CDN/WAF): per-IP, DDoS, bot filtering
2. API Gateway: per-client, business-level limits
3. Service Mesh: per-service, prevent internal cascades
4. Application: connection pools, thread pools, queue sizes

**Tweet 8/10**
The response format matters:

Always return 429 with Retry-After header.

Without Retry-After → clients retry immediately → retry storm
With Retry-After → clients wait → system recovers

Never return 500 for rate limiting. Never silently drop connections.

**Tweet 9/10**
The tradeoffs nobody talks about:

Too aggressive → legitimate users blocked, revenue drops
Too lenient → limits don't protect anything
No monitoring → you don't know which it is

Per-IP punishes corporate NATs. Per-user requires auth. Every approach has blind spots.

**Tweet 10/10**
What to do Monday:

Week 1: Rate limit API gateway (token bucket, 100 req/s)
Week 2: Bound all internal queues
Week 3: Priority queuing for critical paths
Week 4: Load test at 10x with rate limiting on

Full guide: [ARTICLE URL]

Part 6 of Resilience Engineering series.

---

**Thread length**: 10 tweets
**Format**: Numbered thread with clear progression
**Hashtags**: Minimal (2 in main post)
