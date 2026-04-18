# X/Twitter Post

**Article**: Memory Systems for AI Agents: Beyond Context Windows
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Main Post

Customer calls about a billing issue. Agent resolves it.

Two weeks later, same customer, related issue. Agent has zero memory. Asks the same questions from scratch.

Customer: "I already explained this."

Your agent is a goldfish. Here's how to fix that.

[ARTICLE URL]

#AgenticAI #VectorDatabases

---

## Thread

**2/7**
Three types of agent memory, roughly mapping to how human memory works:

Working memory = context window. 128K-200K tokens. Fast, temporary. Gone when conversation ends.

Short-term = session persistence. Redis + TTL. Survives within a session.

Long-term = vector databases. Persists forever. Searchable by meaning.

**3/7**
Vector databases are what make long-term memory work.

Store: "duplicate charge on card ending 4521, resolved by refund"
Search: "billing problem with card 4521"
→ Found. Different words, same meaning.

Semantic similarity, not keyword matching. That's the difference.

**4/7**
Where most teams get retrieval wrong:

Dumping 50 memories into the context window when only 3 are relevant. More context isn't always better — it wastes tokens and can actually confuse the model.

You need relevance scoring + recency weighting + importance filtering.

**5/7**
The forgetting problem is real.

200 individual records per customer after a year. Retrieval gets slow and noisy.

Fix: periodically compress into summaries.

"Jane: 3-year customer, billing issues (60%), prefers email, 3 duplicate charges from gateway timeouts"

One summary > 200 records.

**6/7**
Not every agent needs memory. The complexity isn't justified for:

- One-shot translation
- Simple data extraction
- Stateless API calls

The test: would a human expert be better at this if they remembered previous interactions? If yes, add memory. If no, keep it simple.

**7/7**
Start small:

Week 1: Redis session store (short-term memory, ~20 lines)
Week 2: ChromaDB for interaction summaries (long-term)
Week 3: Metadata filtering (scope by user, topic)
Week 4: Measure impact — does memory actually improve outcomes?

Full guide with Python code: [ARTICLE URL]

---

**Thread length**: 7 tweets
