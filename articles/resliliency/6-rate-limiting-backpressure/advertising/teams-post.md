# Teams Post — Rate Limiting and Backpressure

**Channel**: Jabil Developer Network — Architecture Community
**Subject Line**: Black Friday 2018. Walmart goes down. 3.6 million shoppers affected. The root cause was the absence of one word: "no."
**Featured Image**: `images/featured_image.png`
**Article URL**: https://medium.com/gitconnected/rate-limiting-and-backpressure-protecting-systems-from-themselves-72a3f9162ea8

---

![Featured Image](../images/featured_image.png)

## The Retry Storm Death Spiral

Traffic increases. Response times climb. Users refresh. Load doubles. Mobile apps retry automatically. Load triples. Connection pools fill. Everything crashes. A healthy system at 10:00 AM can be dead by 10:03.

Rate limiting breaks this loop. Backpressure propagates "slow down" through the chain. Load shedding decides what to sacrifice when you can't serve everything.

## The Part Most Teams Skip

Amazon disables recommendations and personalization during Prime Day to protect checkout. Users see generic pages but can still buy things. Revenue is protected.

The hard part isn't implementing load shedding — it's deciding what to shed. That's a business conversation, not an engineering one. And most teams haven't had it before the incident happens.

The article covers 5 rate limiting algorithms (token bucket, leaky bucket, fixed/sliding window), backpressure patterns, load shedding strategies, and a 4-week implementation roadmap starting with "rate limit your API gateway on Monday."

**Part 6 of the Resilience Engineering series** — [Read the full article](https://medium.com/gitconnected/rate-limiting-and-backpressure-protecting-systems-from-themselves-72a3f9162ea8)
