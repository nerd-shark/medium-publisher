# Reddit Post

**Article**: Writing Technical Documents That Non-Technical People Actually Read
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Suggested Subreddits
- r/ExperiencedDevs
- r/programming
- r/softwarearchitecture
- r/cscareerquestions
- r/engineering
- r/technicalwriting

## Post Title
Your 47-page RFC is technically perfect and practically useless — here's how to write docs that actually get read and funded

## Post Body

I've been writing technical proposals, RFCs, and architecture documents for 15+ years. The single biggest lesson: the best technical document isn't the most thorough one. It's the one that gets read.

**The problem**: Technical documents have three audiences with completely different reading patterns.

- **Executives**: Title, first paragraph, conclusion. 30 seconds. Looking for: problem, solution, cost, risk.
- **Product managers**: Impact, timeline, dependencies. Skip implementation entirely.
- **Engineers**: Everything. Want more detail. Read the appendices.

Most of us write for engineers (because we are engineers) and then wonder why executives don't read our 47-page RFCs.

**The fix: layered documents**

Think newspaper article: headline, lead paragraph, full story, background.

- **Layer 1**: Executive summary (1 page, 300 words max). Problem → Solution → Impact → Ask. Self-contained — reader can stop here.
- **Layer 2**: Technical overview (3-5 pages). Architecture, key decisions, tradeoffs. Self-contained — reader can stop here.
- **Layer 3**: Implementation details (appendix, unlimited). Code, data models, APIs. For engineers who will build it.

Each layer tells the complete story at its level of detail. Executives stop at Layer 1. PMs stop at Layer 2. Engineers read Layer 3.

**The one-page executive summary**

This is the most important page. 300 words max. No jargon.

Bad: "We propose migrating from a monolithic architecture to microservices using Kubernetes orchestration with Istio service mesh, implementing event-driven communication via Apache Kafka."

Good: "Our platform can't handle Black Friday traffic — we lost $3.2M last year. We propose splitting the system into independent components that fail independently. Cost: $400K over 6 months. ROI: positive within one Black Friday."

Same project. One gets filed. The other gets funded.

**The inverted pyramid**

Put the answer first. Evidence second. Context third.

Bad: "We evaluated PostgreSQL, MySQL, MongoDB, DynamoDB, and CockroachDB across 14 criteria..." [3 paragraphs later] "...we recommend PostgreSQL."

Good: "We recommend PostgreSQL. It meets all requirements, the team has expertise, and it's 40% cheaper. Full analysis in Appendix B."

**ADRs (Architecture Decision Records)**

Most underused documentation tool. One decision per record. One page max. Context → Decision → Consequences (good AND bad). Your future self will thank you.

**The pre-alignment trick**

Don't surprise stakeholders with a 47-page RFC. Share a one-page problem statement first. Share your approach informally. Get feedback before formalizing. By the time you submit the formal RFC, it's a formality — not a surprise.

"I'd love your input before I formalize this" is the most powerful sentence in technical communication.

**Monday morning test**

Take your last RFC. Add a 300-word executive summary. Move implementation to an appendix. Ask a non-technical colleague to read page 1. If they can't explain your proposal, rewrite it.

Full article with RFC templates, ADR examples, and visual communication guidelines: [ARTICLE URL]

Part 6 of my Technical Communication series. Happy to discuss document structure, stakeholder communication, or RFC processes in the comments.

---

**Format**: No hashtags, conversational, discussion-focused
**Posting Strategy**: Peak hours, engage with comments in first hour
