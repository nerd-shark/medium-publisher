# Rate Limiting and Backpressure: Protecting Systems from Themselves

Part 6 of my series on Resilience Engineering. Last time we covered multi-region architecture and surviving AWS going down. This time: what happens when your own success kills you.

## Opening Hook - Killed by Success

- Black Friday 2022 - major retailer's API gets 10x normal traffic
- Everything was "working" - no bugs, no crashes, just... too much
- Response times went from 200ms to 45 seconds
- Users started refreshing, making it worse (retry storm)
- The system wasn't broken - it was drowning
- Total revenue loss: $12M in 4 hours
- The fix wasn't more servers - it was saying "no" to some requests
- Hook: "Your system is being killed by success. 10x traffic and everything's on fire. Not because anything is broken — because everything is working exactly as designed."

## Why Rate Limiting Matters

- Systems have finite capacity - CPU, memory, connections, database connections
- Without limits, one bad actor or traffic spike can take down everything
- It's not just about DDoS - it's about protecting yourself from yourself
- Microservices make this worse - one slow service backs up everything upstream
- The retry storm problem: failures cause retries, retries cause more failures
- Rate limiting is the immune system of your architecture
- Without it, you're one viral tweet away from an outage

## Rate Limiting Algorithms

### Token Bucket
- Bucket holds N tokens, refills at rate R
- Each request costs 1 token
- If bucket empty, request rejected (or queued)
- Allows bursts up to bucket size
- Simple, effective, most common
- Used by: AWS API Gateway, Stripe, GitHub API
- Good for: APIs with bursty traffic patterns
- Problem: doesn't smooth traffic, just caps it

### Leaky Bucket
- Requests enter a queue (the bucket)
- Processed at a fixed rate (the leak)
- If queue full, new requests rejected
- Smooths traffic to a constant rate
- Good for: systems that need steady throughput
- Problem: adds latency (queuing), doesn't handle bursts well
- Used by: network traffic shaping, some message queues

### Fixed Window Counter
- Count requests in fixed time windows (e.g., per minute)
- Reset counter at window boundary
- Simple to implement
- Problem: boundary burst - 100 requests at 11:59:59 + 100 at 12:00:01 = 200 in 2 seconds
- Used by: simple API rate limiters
- Good enough for many use cases despite the boundary problem

### Sliding Window Log
- Track timestamp of each request
- Count requests in last N seconds
- Most accurate but most memory-intensive
- Stores every request timestamp
- Good for: precise rate limiting where accuracy matters
- Problem: memory usage scales with request volume

### Sliding Window Counter
- Hybrid of fixed window and sliding window
- Weighted average of current and previous window
- Good balance of accuracy and memory
- Used by: Redis-based rate limiters, Cloudflare
- The sweet spot for most production systems

## Backpressure: When Rate Limiting Isn't Enough

- Rate limiting says "no" at the front door
- Backpressure says "slow down" through the entire system
- Like a highway on-ramp meter - control flow at every point
- Without backpressure, internal services can still overwhelm each other
- The queue problem: unlimited queues just delay the crash
- Bounded queues + rejection = backpressure
- Reactive Streams (Java), Go channels, Rust async - built-in backpressure

### Backpressure Propagation
- Service A calls Service B calls Service C
- C is slow → B's queue fills → B tells A to slow down
- Each layer propagates pressure upstream
- Without this: A keeps sending, B's queue grows unbounded, OOM crash
- With this: A slows down, users see "please wait", system stays alive

### Load Shedding
- When you're overwhelmed, drop low-priority work
- Not all requests are equal: checkout > browse > recommendations
- Priority queues: serve high-priority first, shed low-priority
- The hard part: deciding what's "low priority" in real-time
- Amazon does this: during peak, they disable recommendations to protect checkout

## DDoS Protection

- Rate limiting per IP, per user, per API key
- But DDoS comes from thousands of IPs
- Need: global rate limiting + pattern detection
- WAF (Web Application Firewall) for known attack patterns
- CDN-level rate limiting (Cloudflare, AWS Shield)
- The difference between rate limiting and DDoS protection:
  - Rate limiting: "you're sending too many requests"
  - DDoS protection: "you're not a real user"

## Priority Queues and Fair Queuing

- Not all traffic is equal
- Checkout requests > product page views > recommendation requests
- Priority queues ensure critical paths get resources first
- Fair queuing prevents one tenant from starving others (multi-tenant)
- Weighted fair queuing: tenant A gets 60%, tenant B gets 30%, tenant C gets 10%
- The starvation problem: low-priority requests never get served
- Solution: aging - low-priority requests gradually increase in priority

## Implementation Patterns

### Where to Rate Limit
- API Gateway (front door) - per-client limits
- Service mesh (internal) - per-service limits
- Database connection pool - per-query limits
- Message queue consumer - per-consumer limits
- Each layer needs its own limits

### Distributed Rate Limiting
- Single server: easy, just count in memory
- Multiple servers: need shared state (Redis, etc.)
- The consistency problem: Redis might be slightly behind
- Solution: approximate rate limiting (allow small overages)
- Or: sticky sessions (same client always hits same server)

### What to Return When Rate Limited
- HTTP 429 Too Many Requests
- Retry-After header (tell client when to try again)
- Rate limit headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
- Don't just drop connections silently - that causes retry storms

## Real-World Examples

- Stripe: 100 requests/second per API key, token bucket
- GitHub: 5000 requests/hour authenticated, 60 unauthenticated
- Twitter/X: Tiered rate limits by endpoint and plan
- AWS API Gateway: Configurable per-stage, per-method
- Netflix: Zuul gateway with adaptive rate limiting

## The Tradeoffs

- Too aggressive: legitimate users get blocked, revenue lost
- Too lenient: system overwhelmed during spikes
- The Goldilocks problem: finding the right limits
- Start conservative, loosen based on data
- Monitor 429 rates - if >1% of traffic, limits might be too tight
- A/B test rate limits (carefully)

## What to Do Monday Morning

- Add rate limiting to your API gateway (if you haven't already)
- Implement backpressure in your message queues (bounded queues)
- Add priority queuing for critical paths
- Return proper 429 responses with Retry-After headers
- Monitor your rate limit hit rates
- Test with load testing tools (k6, Locust, Artillery)

Target: ~500 words outline (brainstorm skeleton)
