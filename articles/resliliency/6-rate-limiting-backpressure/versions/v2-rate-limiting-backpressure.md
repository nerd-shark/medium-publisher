# Rate Limiting and Backpressure: Protecting Systems from Themselves

Part 6 of my series on Resilience Engineering. Last time, we explored [multi-region architecture and surviving infrastructure apocalypse](link). This time: what happens when your own success kills you — and how to build systems that protect themselves from overwhelming traffic. Follow along for more deep dives into building systems that don't fall apart.

## Killed by Success

Black Friday 2022. A major e-commerce platform's API starts receiving 10x normal traffic at 6 AM. Nothing is broken. No bugs, no crashes, no failed deployments. Just... too much.

Response times climb from 200ms to 2 seconds. Then 10 seconds. Then 45 seconds. Users start refreshing pages, which doubles the load. Mobile apps retry failed requests automatically — tripling it. The load balancer keeps accepting connections because the servers are technically "healthy" (they're responding, just slowly). The database connection pool fills up. Queries start queuing. The queue grows unbounded until the service runs out of memory and crashes.

Four hours. $12 million in lost revenue. And the root cause wasn't a bug — it was the absence of a simple word: "no."

The system never learned to say "no." It accepted every request, tried to serve every user, and drowned trying. The fix wasn't more servers. It was rate limiting and backpressure — teaching the system to protect itself from itself.

## Why Systems Need to Say "No"

Every system has finite capacity. CPU cycles, memory, database connections, network bandwidth, thread pools — all finite. Without explicit limits, a traffic spike doesn't just slow things down. It creates a cascade.

Here's how the cascade works:

1. Traffic increases beyond capacity
2. Response times increase (requests take longer, consuming resources longer)
3. More concurrent requests pile up (because each takes longer to complete)
4. Resource utilization hits 100% (CPU, memory, connections)
5. Everything slows down further (contention, context switching, GC pressure)
6. Users retry failed/slow requests (doubling or tripling load)
7. Monitoring systems fire alerts, triggering automated scaling (which takes minutes)
8. By the time new capacity arrives, the system has crashed

This is the retry storm — the most common cause of cascading failures in distributed systems. One slow service causes retries, retries cause more load, more load causes more slowness, more slowness causes more retries. It's a positive feedback loop that ends in total system failure.

Rate limiting breaks this loop by rejecting excess traffic before it enters the system. Backpressure propagates "slow down" signals through the entire service chain. Together, they're the immune system of your architecture.

[The irony: the systems that crash hardest are often the ones that try hardest to serve every request. The systems that survive are the ones that learned to say "no" gracefully]

## Rate Limiting Algorithms: Pick Your Weapon

There are five major rate limiting algorithms. Each has different characteristics for burst handling, memory usage, and accuracy. The right choice depends on your traffic patterns.

### Token Bucket

The most common algorithm. A bucket holds N tokens and refills at rate R tokens per second. Each request costs one token. If the bucket is empty, the request is rejected or queued.

**How it works**:
- Bucket capacity: 100 tokens (allows bursts up to 100)
- Refill rate: 10 tokens/second (sustained rate of 10 req/s)
- Request arrives: if tokens > 0, decrement and allow; if tokens = 0, reject
- Bucket refills continuously at the configured rate

**Strengths**: Allows controlled bursts (up to bucket size), simple to implement, low memory (just two numbers: token count and last refill timestamp). Used by AWS API Gateway, Stripe, GitHub API.

**Weaknesses**: Doesn't smooth traffic — allows full burst followed by rejection. If bucket size is 100, a client can send 100 requests in 1 second, then nothing for 10 seconds.

```python
class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.monotonic()
    
    def allow_request(self) -> bool:
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
    
    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
```

[This is the algorithm you should start with. It handles 90% of use cases well. Only switch to something else if you have specific requirements it doesn't meet]

### Leaky Bucket

Requests enter a queue (the bucket). They're processed at a fixed rate (the leak). If the queue is full, new requests are rejected.

**How it works**:
- Queue capacity: 50 requests
- Processing rate: 10 requests/second (fixed, constant)
- Request arrives: if queue not full, enqueue; if full, reject
- Requests dequeued and processed at constant rate

**Strengths**: Smooths traffic to a perfectly constant rate. No bursts reach your backend. Good for systems that need steady, predictable throughput.

**Weaknesses**: Adds latency (requests wait in queue). Doesn't handle legitimate bursts well — a burst of 50 requests all wait in queue even if the system could handle them immediately. Poor for interactive APIs where latency matters.

[Use leaky bucket for background processing, message queues, and systems where constant throughput matters more than latency. Don't use it for user-facing APIs — the added latency will frustrate users]

### Fixed Window Counter

Count requests in fixed time windows (e.g., per minute). Reset the counter at each window boundary.

**How it works**:
- Window size: 1 minute
- Limit: 100 requests per window
- Request arrives: increment counter; if counter > limit, reject
- At window boundary (e.g., 12:01:00), reset counter to 0

**Strengths**: Dead simple to implement. Low memory (one counter per client). Easy to understand and debug.

**Weaknesses**: The boundary burst problem. A client sends 100 requests at 11:59:59 and 100 more at 12:00:01. That's 200 requests in 2 seconds, despite a "100 per minute" limit. The window reset creates a vulnerability at every boundary.

[Good enough for many use cases despite the boundary problem. If your limit is 1000/minute and someone sends 2000 in 2 seconds at the boundary, is that actually a problem for your system? Often it's not. Don't over-engineer]

### Sliding Window Log

Track the timestamp of every request. Count requests in the last N seconds by scanning the log.

**How it works**:
- Window size: 60 seconds
- Limit: 100 requests per window
- Request arrives: add timestamp to log, remove timestamps older than 60 seconds, count remaining; if count > limit, reject

**Strengths**: Most accurate. No boundary burst problem. Precise rate limiting.

**Weaknesses**: Memory-intensive — stores every request timestamp. At 1000 req/s, that's 60,000 timestamps per client per minute. Scanning the log on every request adds latency.

[Use only when precision matters more than efficiency. Financial APIs, security-sensitive endpoints. For most APIs, the sliding window counter (next) is a better choice]

### Sliding Window Counter

A hybrid of fixed window and sliding window. Uses a weighted average of the current and previous window counts.

**How it works**:
- Window size: 1 minute
- Current window count: 40 requests (started 45 seconds ago)
- Previous window count: 80 requests
- Weighted count: 80 × (15/60) + 40 = 80 × 0.25 + 40 = 60
- If weighted count > limit, reject

**Strengths**: Good accuracy without the memory cost of sliding window log. Handles boundary bursts much better than fixed window. Low memory (two counters per client).

**Weaknesses**: Approximate — not perfectly accurate. But the approximation is good enough for virtually all production use cases.

[This is the sweet spot for most production systems. Used by Redis-based rate limiters, Cloudflare, and most serious API platforms. If you're not sure which algorithm to use, use this one]

## Backpressure: When Rate Limiting Isn't Enough

Rate limiting says "no" at the front door. But what about traffic that's already inside your system? What about internal service-to-service calls? What about message queues that grow unbounded?

Backpressure is the mechanism that propagates "slow down" signals through your entire system, not just at the edge.

### The Unbounded Queue Problem

Here's a pattern I see constantly: Service A sends messages to a queue. Service B consumes from the queue. The queue is unbounded (or has a very large limit). Service B gets slow. Messages pile up. The queue grows to millions of messages. Memory usage spikes. Eventually something crashes.

The fix is simple but counterintuitive: make the queue small. A bounded queue with a capacity of 1,000 messages forces the producer to slow down when the consumer can't keep up. The producer either blocks (synchronous backpressure) or gets a rejection (asynchronous backpressure).

[Unbounded queues are a lie. Every queue has a limit — it's either the limit you set or the amount of available memory. The difference is whether you handle the limit gracefully or crash]

### Backpressure Propagation

In a microservices architecture, backpressure needs to propagate through the entire call chain.

Service A → Service B → Service C → Database

If the database is slow, Service C's response times increase. Service B's thread pool fills up waiting for C. Service A's requests to B start timing out.

Without backpressure: A keeps sending requests to B. B's queue grows. B runs out of memory. B crashes. A retries. A's queue grows. A crashes. Cascade complete.

With backpressure: C returns HTTP 503 with Retry-After header. B's circuit breaker opens for C. B returns 503 to A. A's circuit breaker opens for B. A returns 503 to the client with a Retry-After header. The client waits and retries later. System stays alive.

[The key insight: backpressure turns a crash into a temporary degradation. Instead of "everything is dead," you get "some requests are delayed." That's a much better failure mode]

### Load Shedding: The Nuclear Option

When backpressure isn't enough — when you're so overwhelmed that even slowing down won't help — you need load shedding. Drop low-priority work to protect high-priority work.

Not all requests are equal:
- **Priority 1**: Checkout, payment processing ($1M/hour revenue)
- **Priority 2**: Product pages, search ($100K/hour)
- **Priority 3**: Recommendations, personalization ($10K/hour)
- **Priority 4**: Analytics, A/B tests, non-essential features ($0 direct revenue)

During a traffic spike, shed Priority 4 first. Then Priority 3. Protect Priority 1 at all costs.

Amazon does this during Prime Day. When traffic exceeds capacity, they disable recommendations, personalization, and non-essential features to protect the checkout flow. Users might see generic product pages instead of personalized ones, but they can still buy things. Revenue is protected.

[The hard part isn't implementing load shedding — it's deciding what to shed. This requires business input, not just engineering judgment. Have the conversation with product and business stakeholders before the crisis, not during it]

## DDoS Protection: Rate Limiting's Big Brother

Rate limiting protects against legitimate traffic spikes. DDoS protection handles malicious traffic designed to overwhelm your system.

The difference: rate limiting says "you're sending too many requests." DDoS protection says "you're not a real user."

### Layer 3/4 DDoS (Network Level)
- Volumetric attacks: flood bandwidth (UDP floods, ICMP floods)
- Protocol attacks: exploit protocol weaknesses (SYN floods)
- Mitigation: CDN-level filtering (Cloudflare, AWS Shield), ISP-level scrubbing
- You can't handle this at the application level — the traffic overwhelms your network before it reaches your servers

### Layer 7 DDoS (Application Level)
- HTTP floods: legitimate-looking requests at massive scale
- Slowloris: keep connections open with slow, incomplete requests
- Application-specific attacks: expensive queries, large uploads
- Mitigation: WAF rules, behavioral analysis, CAPTCHA challenges, rate limiting per IP/fingerprint

### Practical DDoS Defense
- **CDN**: Absorb volumetric attacks at the edge (Cloudflare handles 100+ Tbps)
- **WAF**: Block known attack patterns (SQL injection, XSS, bot signatures)
- **Rate limiting per IP**: 100 req/s per IP is generous for humans, restrictive for bots
- **Geographic filtering**: If your users are in the US, block traffic from countries you don't serve
- **Challenge pages**: CAPTCHA or JavaScript challenges for suspicious traffic

[Most companies don't need custom DDoS protection. Cloudflare's free tier handles most attacks. AWS Shield Standard is included with every AWS account. The expensive custom solutions are for companies that are specifically targeted — financial services, gaming, political organizations]

## Implementation: Where and How to Rate Limit

### The Four Layers

**Layer 1: Edge (CDN/WAF)** — Per-IP rate limiting, DDoS protection, bot filtering. This is your first line of defense. Cloudflare, AWS CloudFront + WAF, Akamai.

**Layer 2: API Gateway** — Per-client rate limiting (API keys, OAuth tokens). Business-level limits: free tier gets 100 req/min, paid tier gets 10,000 req/min. AWS API Gateway, Kong, Nginx.

**Layer 3: Service Mesh** — Per-service rate limiting. Service A can call Service B at 1,000 req/s. Prevents internal cascade failures. Istio, Linkerd, Envoy.

**Layer 4: Application** — Per-resource rate limiting. Database connection pools, thread pools, queue sizes. This is your last line of defense.

[You need rate limiting at multiple layers. Edge rate limiting alone doesn't protect against internal cascades. Application rate limiting alone doesn't protect against DDoS. Defense in depth]

### Distributed Rate Limiting

Single server: easy. Count requests in memory. Done.

Multiple servers: harder. You need shared state. Options:

**Redis**: Most common. Atomic increment operations. Lua scripts for complex algorithms. Latency: 1-2ms per check. Problem: Redis itself becomes a dependency. If Redis goes down, do you allow all traffic (fail open) or reject all traffic (fail closed)?

**Local + Sync**: Each server tracks locally, periodically syncs with peers. Less accurate but no external dependency. Good for approximate rate limiting where ±10% accuracy is acceptable.

**Sticky Sessions**: Route the same client to the same server. Rate limit locally. Simple but limits load balancing flexibility.

[For most systems, Redis with fail-open is the right choice. If Redis goes down, you temporarily lose rate limiting but your system stays up. The alternative — fail-closed — means Redis downtime causes a total outage. That's worse than temporarily allowing excess traffic]

### What to Return When Rate Limited

This matters more than you think. Bad rate limiting responses cause retry storms.

```
HTTP/1.1 429 Too Many Requests
Retry-After: 30
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1679616000

{
  "error": "rate_limit_exceeded",
  "message": "Too many requests. Please retry after 30 seconds.",
  "retry_after": 30
}
```

The `Retry-After` header is critical. Without it, clients retry immediately, making the problem worse. With it, well-behaved clients wait. The `X-RateLimit-*` headers let clients self-regulate before hitting the limit.

[Never silently drop connections. Never return 500 for rate limiting. Always return 429 with Retry-After. This is the difference between a system that recovers gracefully and one that spirals into a retry storm]

## Real-World Rate Limiting

| Service | Limit | Algorithm | Notes |
|---------|-------|-----------|-------|
| Stripe | 100 req/s per key | Token bucket | Separate limits for read/write |
| GitHub | 5,000 req/hr (auth) | Sliding window | 60/hr unauthenticated |
| Twitter/X | Varies by endpoint | Tiered | 15-min windows, per-endpoint |
| AWS API Gateway | Configurable | Token bucket | Per-stage, per-method |
| Cloudflare | Configurable | Sliding window | Edge-level, per-zone |
| Shopify | 40 req/s (Plus) | Leaky bucket | Cost-based (some ops cost more) |

[Shopify's approach is interesting — they use a cost-based system where complex operations (bulk queries) cost more "tokens" than simple ones (single reads). This prevents a client from consuming disproportionate resources with expensive queries while staying under the request count limit]

## The Tradeoffs Nobody Talks About

**Too aggressive**: Legitimate users get blocked. Revenue lost. Customer support tickets spike. "Why can't I check out?" is a bad customer experience.

**Too lenient**: System overwhelmed during spikes. The rate limits exist but don't actually protect anything. You've added complexity without benefit.

**The monitoring gap**: You set rate limits but don't monitor them. Are 0.1% of requests being rate-limited? That's probably fine. Are 5% being rate-limited? Your limits are too tight or your capacity is too low.

**The fairness problem**: Per-IP rate limiting punishes users behind corporate NATs (thousands of users sharing one IP). Per-user rate limiting requires authentication, which means unauthenticated endpoints are unprotected.

**The cost of saying "no"**: Every rejected request is a user who might not come back. Rate limiting is a business decision, not just a technical one. The product team should be involved in setting limits.

## What to Do Monday Morning

Start with the highest-impact, lowest-effort changes:

**Week 1**: Add rate limiting to your API gateway. Token bucket, 100 req/s per client. Return proper 429 responses with Retry-After headers. Monitor the hit rate.

**Week 2**: Implement bounded queues for all internal message queues. If a queue has no size limit, add one. Start with 10x your normal queue depth and adjust down.

**Week 3**: Add priority queuing for your critical path. Identify your top 3 revenue-generating endpoints. Ensure they get resources first during overload.

**Week 4**: Load test with rate limiting enabled. Use k6, Locust, or Artillery to simulate 10x traffic. Verify that rate limiting kicks in, responses are correct, and the system stays healthy.

The goal isn't to block users. It's to keep the system alive so you can serve as many users as possible. A system that serves 80% of users at normal speed is better than a system that serves 0% of users because it crashed trying to serve 100%.

---

Target: ~1,800 words detailed outline with rough prose
