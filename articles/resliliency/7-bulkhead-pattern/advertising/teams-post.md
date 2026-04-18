# Teams Post — The Bulkhead Pattern

**Channel**: Jabil Developer Network — Architecture Community
**Subject Line**: One slow API call just ate your entire thread pool. 200 healthy endpoints are returning 503 because of a single bad dependency.
**Featured Image**: `images/featured_image.png`
**Article URL**: https://medium.com/@the-architect-ds/the-bulkhead-pattern-isolating-failure-domains-within-services-f0d6f5a5341e

---

![Featured Image](../images/featured_image.png)

## The Thread Pool That Ate Everything

Tuesday afternoon. Platform handles 50,000 requests per minute. A third-party recommendation API starts responding in 30 seconds instead of 200ms. Not failing — just slow. 200 shared threads. Within two minutes, all blocked waiting for recommendations. Checkout goes down. Search goes down. Health checks go down. Total outage from one slow dependency.

## The Fix: Resource Isolation

The bulkhead pattern gives each critical dependency its own isolated resource pool. Checkout gets 80 threads. Search gets 60. Recommendations gets 30. When recommendations fills up, checkout still has 80 threads available.

The article covers:

- **What to isolate** — external dependencies, critical revenue paths, different failure characteristics
- **Beyond thread pools** — connection pools, memory, CPU isolation
- **Bulkheads + circuit breakers** — bulkhead contains the blast radius, circuit breaker minimizes the duration
- **Sizing formula** — `pool_size = peak_rps × timeout_seconds × 1.5`
- **Kubernetes-native bulkheads** — pod resource limits, namespace quotas, PDBs, service mesh rate limiting

Includes Python implementation and a 4-week rollout plan.

**Part 7 of the Resilience Engineering series** — [Read the full article](https://medium.com/@the-architect-ds/the-bulkhead-pattern-isolating-failure-domains-within-services-f0d6f5a5341e)
