# Facebook Post

**Article**: Rate Limiting and Backpressure: Protecting Systems from Themselves
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

🚨 Black Friday 2018. Walmart.com buckles under a massive traffic surge.

3.6 million shoppers affected. ~$9 million in lost sales. And Walmart wasn't alone — Lowe's, J.Crew, Best Buy, and Office Depot all went down that same weekend.

The root cause wasn't a bug. It wasn't a bad deployment. The system never learned to say "no."

---

**THE RETRY STORM DEATH SPIRAL**

Every system has finite capacity. Without explicit limits, a traffic spike creates a positive feedback loop:

Traffic increases → response times climb → users refresh pages (doubling load) → mobile apps auto-retry (tripling load) → connection pools fill → everything crashes in sequence.

A system that was healthy at 10:00 AM can be completely dead by 10:03 AM. This happens every Black Friday, every viral marketing campaign, every time a product gets featured on Hacker News.

---

**5 RATE LIMITING ALGORITHMS**

🪣 **Token Bucket** — Handles bursts naturally, minimal memory. Used by Stripe, AWS API Gateway, GitHub. If you're not sure which to pick, start here.

🚰 **Leaky Bucket** — Smooths traffic to a constant rate. No bursts reach your backend. Shopify uses this with cost-based weighting where complex operations consume more capacity.

📊 **Fixed Window Counter** — Dead simple: one counter per client. Has a boundary burst vulnerability, but often good enough in practice.

📈 **Sliding Window Counter** — Best balance of accuracy and efficiency. Used by Cloudflare and most Redis-based rate limiters.

📋 **Sliding Window Log** — Most accurate, highest memory cost. Use only for financial APIs or compliance-driven rate limiting.

---

**BACKPRESSURE: THE INTERNAL IMMUNE SYSTEM**

Rate limiting says "no" at the front door. But what about traffic already inside your system?

The unbounded queue trap: Service A sends messages to a queue. Service B consumes from the queue. B gets slow. Messages pile up to millions. Memory spikes. Something crashes.

The fix: make queues small. A bounded queue forces the producer to slow down when the consumer can't keep up. Every queue has a limit — it's either the limit you set or the amount of available memory.

---

**LOAD SHEDDING: CHOOSING WHAT TO SACRIFICE**

Not all requests are equal. Amazon does this during Prime Day — they disable recommendations, personalization, and non-essential features to protect the checkout flow. Users see generic product pages but can still buy things. Revenue is protected.

The hard part isn't implementing load shedding — it's deciding what to shed. That's a business conversation, not just an engineering one. Have it before the crisis, not during it.

---

**WHAT TO DO MONDAY**

Week 1: Add rate limiting to your API gateway. Token bucket, 100 req/s per client. Return 429 with Retry-After headers.
Week 2: Bound all internal message queues. No queue should be unlimited.
Week 3: Add priority queuing for your top 3 revenue-generating endpoints.
Week 4: Load test with rate limiting enabled. Simulate 10x traffic.

Your system's job isn't to accept every request. It's to serve as many as it can, well, and gracefully decline the rest.

Full guide with algorithms, code examples, and real-world rate limiting comparisons from Stripe, GitHub, Shopify, and Cloudflare:

[ARTICLE URL]

Part 6 of my Resilience Engineering series. Catch up on the full series for the complete picture.

#ResilienceEngineering #RateLimiting #Backpressure #APIDesign #LoadShedding #DistributedSystems #SRE #SystemDesign

---

**Character count**: ~2,700 (within Facebook's limits)
**Hashtags**: 8 (appropriate for Facebook)
**Link Placement**: Direct link with clear CTA
**Visual**: Use the Overwhelmed Gateway or Defense in Depth image
