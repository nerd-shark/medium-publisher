# LinkedIn Post v2

**Article**: The Bulkhead Pattern: Isolating Failure Domains Within Services
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

It was a Tuesday afternoon around 2:30 PM when I was consulting for a platform handling about 50,000 requests per minute. Everything looked solid—green across the board. Then, out of nowhere, a third-party recommendation API started dragging, responding in 30 seconds instead of the usual 200ms.

Not a full failure, just painfully slow.

With 200 shared threads, that recommendation endpoint began hogging them all. They just sat there, waiting. In under two minutes, every single thread was tied up.

Checkout crashed—not because of any issue with checkout itself, but because no threads were available. Search followed, then profiles, and even health checks. The load balancer thought the whole server was dead.

One sluggish API, 200 otherwise healthy endpoints, and boom—total platform outage.

This is Part 7 of my Resilience Engineering series, and it's a lesson I wish more teams learned earlier.

The solution? Borrowed from naval engineering. Ships use bulkheads—watertight compartments. If one gets breached, the others stay intact, keeping the ship afloat.

Apply that to software: ditch the single shared thread pool of 200. Instead:

- Allocate 80 threads to checkout (it's your lifeline)
- 60 to search
- 30 to recommendations
- 30 split among the rest

If recommendations' pool maxes out? Checkout keeps its 80 threads running smoothly. The platform stays up. Recommendations might error out, but everything else hums along.

What deserves isolation? Definitely third-party APIs (you can't control their reliability), your revenue-critical paths like checkout and payments, and any component with wildly different failure modes.

Pair bulkheads with circuit breakers for the best results. Bulkheads limit the damage zone; circuit breakers cut the exposure time. Together, they ensure requests fail fast with a solid fallback, using only a capped number of threads for a short window.

Sizing is key: pool_size = peak_rps × timeout_seconds × 1.5

For 50 requests per second with a 2-second timeout, that's 150 threads—way too many. Drop to 500ms timeout, and it's down to 38. That's why tight timeouts are non-negotiable in bulkheaded setups.

It's not the sexy part of engineering. More like fixing pipes than building rockets. But it's this kind of groundwork that prevents a slow recommendation API from sinking your entire platform.

Dive deeper with the full guide, including Python code and Kubernetes patterns:

[ARTICLE URL]

#ResilienceEngineering #SystemDesign #DevOps #SoftwareArchitecture

---

**Character count**: ~1,900
**Hashtags**: 4</content>
<parameter name="filePath">c:\Users\3717246\Repos\Medium\articles\resliliency\7-bulkhead-pattern\advertising\linkedin-post-v2.md