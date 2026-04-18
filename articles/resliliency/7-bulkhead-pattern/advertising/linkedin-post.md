# LinkedIn Post

**Article**: The Bulkhead Pattern: Isolating Failure Domains Within Services
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

Tuesday afternoon, about 2:30. Platform I was consulting for handles 50,000 requests per minute. Everything's green. Then a third-party recommendation API starts responding in 30 seconds instead of 200ms.

Not failing. Just slow.

200 shared threads. Recommendation endpoint starts consuming them. They just sit there, waiting. Within two minutes, all 200 threads are blocked.

Checkout goes down. Not because anything's wrong with checkout. Because there are no threads left to serve it. Search goes down. Profiles go down. Health checks go down, which makes the load balancer think the server is dead.

One slow API. 200 healthy endpoints. Total outage.

Part 7 of my Resilience Engineering series.

The fix comes from ships. Literally. Ships have watertight compartments — bulkheads. Breach one, the others stay dry. Ship stays afloat.

Same idea for software. Instead of one shared pool of 200 threads:

Checkout gets 80 (it's your revenue)
Search gets 60
Recommendations gets 30
Everything else shares 30

Recommendations pool fills up? Checkout still has 80 threads. Platform stays healthy. Recommendations returns errors, everything else keeps working.

What to isolate:
- Every third-party API call (you don't control their SLAs)
- Your critical revenue path (checkout, payments)
- Anything with different failure characteristics

Bulkheads + circuit breakers work best together. Bulkhead contains the blast radius. Circuit breaker minimizes the duration. Together: limited threads for limited time before requests fail fast with a fallback.

Sizing matters: pool_size = peak_rps × timeout_seconds × 1.5

50 req/s with a 2-second timeout = 150 threads. That's a lot. With a 500ms timeout = 38 threads. Much more reasonable. This is why aggressive timeouts matter so much in bulkheaded systems.

Not glamorous work. It's plumbing. But it's the plumbing that keeps your platform from going down because a recommendation API got slow.

Full guide with Python implementation and Kubernetes-native patterns:

[ARTICLE URL]

#ResilienceEngineering #BulkheadPattern #FaultIsolation #DistributedSystems #SRE #SystemDesign #Kubernetes #CloudArchitecture #SoftwareArchitecture #DevOps

---

**Character count**: ~2,000
**Hashtags**: 10
