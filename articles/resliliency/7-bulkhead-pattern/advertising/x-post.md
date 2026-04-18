# X/Twitter Post

**Article**: The Bulkhead Pattern: Isolating Failure Domains Within Services
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Main Post

A recommendation API got slow. Not down — just slow. 30 seconds instead of 200ms.

Within 2 minutes, checkout was returning 503. Search was down. Everything was down.

Because all 200 threads shared one pool. One slow dependency drained them all.

[ARTICLE URL]

#ResilienceEngineering #SystemDesign

---

## Thread

**2/6**
The fix comes from ships. Literally.

Ships have watertight compartments — bulkheads. Breach one, the others stay dry.

Software version: give each dependency its own thread pool.
Checkout: 80 threads
Search: 60
Recommendations: 30

Recommendations fills up? Checkout still has 80.

**3/6**
What to isolate:

Every third-party API (you don't control their SLAs or their bad days)
Your revenue path (checkout, payments — protect at all costs)
Anything with different failure modes

Practical starting point: one bulkhead per external dep, one for critical path, one shared for everything else.

**4/6**
Bulkheads + circuit breakers are better together.

Bulkhead: limits how many threads a dependency can consume
Circuit breaker: detects failure and stops sending requests

Without circuit breaker, bulkhead threads sit blocked until timeout.
With circuit breaker, requests fail fast and threads free up immediately.

**5/6**
Sizing formula that actually works:

pool_size = peak_rps × timeout_seconds × 1.5

50 req/s with 2s timeout = 150 threads (way too many)
50 req/s with 500ms timeout = 38 threads (reasonable)

This is why aggressive timeouts matter so much. The timeout determines the bulkhead size.

**6/6**
Not glamorous work. It's plumbing.

But it's the plumbing that keeps your platform from going down because some third-party recommendation API had a bad afternoon.

Full guide with Python code and K8s patterns: [ARTICLE URL]

---

**Thread length**: 6 tweets
