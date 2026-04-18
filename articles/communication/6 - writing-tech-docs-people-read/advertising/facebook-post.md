# Facebook Post

**Article**: Writing Technical Documents That Non-Technical People Actually Read
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

📄 You spent 3 weeks writing a 47-page RFC. Two people read it.

Architecture diagrams with proper UML notation. Sequence diagrams. Risk analysis with probability matrices. Cost projections broken down by quarter. It was thorough, technically precise, and comprehensive.

One person skimmed the conclusion. The other asked "can you just summarize this in Slack?"

The project got approved anyway — based on a 5-minute hallway conversation with the VP of Engineering.

Your RFC was technically perfect and practically useless.

---

**THE THREE-AUDIENCE PROBLEM**

Technical documents have three audiences with completely different reading patterns:

📊 **Executives** read the title, first paragraph, and conclusion. They have 30 seconds and 47 other documents competing for attention.

📋 **Product Managers** read impact, timeline, and dependencies. They skip implementation entirely.

💻 **Engineers** read everything and want more detail.

Most documents fail because they're written for one audience (engineers) and read by three.

---

**THE ONE-PAGE EXECUTIVE SUMMARY**

300 words maximum. Problem → Solution → Impact → Ask.

**Bad**: "We propose migrating from a monolithic architecture to microservices using Kubernetes orchestration with Istio service mesh."

**Good**: "Our platform can't handle Black Friday traffic — we lost $3.2M last year. We propose splitting the system into independent components. Cost: $400K over 6 months. ROI: positive within one Black Friday."

Same project. The first gets filed. The second gets funded.

---

**THE LAYERED DOCUMENT**

Think newspaper: headline, lead paragraph, full story, background.

Layer 1: Executive summary (1 page) — business value and ask
Layer 2: Technical overview (3-5 pages) — architecture and tradeoffs
Layer 3: Implementation details (appendix) — code, data models, APIs

Each layer is self-contained. Executives stop at Layer 1. PMs stop at Layer 2. Engineers read Layer 3.

---

**WHAT TO DO MONDAY**

1. Add a one-page executive summary to your last RFC
2. Move implementation details to an appendix
3. Ask a non-technical colleague to read the first page — if they can't explain your proposal, rewrite it

Full guide with RFC structure, ADR templates, and visual communication tips:

[ARTICLE URL]

Part 6 of my Technical Communication series.

#TechnicalCommunication #EngineeringLeadership #Documentation #RFC #TechnicalWriting #SoftwareArchitecture #TechLeadership #CareerDevelopment

---

**Character count**: ~2,200
**Hashtags**: 8
