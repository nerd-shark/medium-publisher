# Facebook Post

**Article**: The Bulkhead Pattern: Isolating Failure Domains Within Services
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

Tuesday afternoon, about 2:30. Platform I was consulting for handles 50,000 requests per minute across maybe 200 endpoints. Everything looks fine. Dashboards are green.

Then a third-party recommendation API starts responding slowly. Not failing — just slow. 30 seconds instead of 200 milliseconds.

The application server has a shared thread pool. 200 threads, serving everything. The recommendation endpoint starts consuming threads that just sit there waiting. Within about two minutes, all 200 threads are blocked.

And then checkout goes down. Not because anything is wrong with checkout. Not because the payment gateway is slow. Checkout goes down because there are literally no threads left to serve it. Search goes down. User profiles go down. The health check goes down, which makes the load balancer think the server is dead.

One slow third-party API. 200 healthy endpoints. Total platform outage. The recommendation service didn't even fail — it just got slow. And that was enough.

**The fix comes from ships.**

Ships have watertight compartments — bulkheads. If the hull is breached in one compartment, water floods that compartment but the bulkheads prevent it from spreading. The ship stays afloat because the damage is contained.

Same principle for software. Instead of one shared pool of 200 threads:

- Checkout gets 80 threads (it's your revenue — protect it)
- Search gets 60 threads
- Recommendations gets 30 threads
- Everything else shares the remaining 30

When recommendations goes slow and its 30 threads fill up, checkout still has 80 threads available. Platform stays healthy. Recommendations returns errors, everything else keeps working.

**What to isolate:**

Every third-party API call — you don't control their SLAs or their bad days. Your critical revenue path — checkout, payments, whatever makes money. Anything with different failure characteristics from the rest.

**Bulkheads + circuit breakers work best together.** Bulkhead limits how many threads a dependency can consume (contains the blast radius). Circuit breaker detects the failure and stops sending requests (minimizes the duration). Without circuit breaker, bulkhead threads sit blocked until timeout. With circuit breaker, requests fail fast and threads free up immediately.

**Sizing matters:** pool_size = peak_rps × timeout_seconds × 1.5

50 req/s with a 2-second timeout = 150 threads (way too many). With a 500ms timeout = 38 threads (much more reasonable). This is why aggressive timeouts matter so much — the timeout directly determines how big your bulkhead needs to be.

Not glamorous work. It's plumbing. But it's the plumbing that keeps your platform from going down because some recommendation API had a bad afternoon.

Full guide with Python code and Kubernetes-native patterns:

[ARTICLE URL]

Part 7 of my Resilience Engineering series.

#ResilienceEngineering #BulkheadPattern #FaultIsolation #DistributedSystems #SRE #SystemDesign #CloudArchitecture #DevOps

---

**Character count**: ~2,500
**Hashtags**: 8
