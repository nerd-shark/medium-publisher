---
document-title: Unpublished Articles Update Requirements
document-subtitle: Series Navigation and SEO Updates for Planned Articles
document-type: Update Specification
document-date: 2025-02-13
document-revision: 1.0
document-author: Kiro AI Assistant
review-cycle: One-time
---

# Unpublished Articles Update Requirements

## Overview

This document specifies the mandatory updates required for all unpublished Medium articles based on the new Article Writing Process guidelines. These updates ensure consistency, improve SEO, and enhance reader navigation across all three series.

**Reference Document**: `for-approval/medium/ARTICLE-WRITING-PROCESS.md`
**Affected Articles**: All articles with "Planned" status in `MEDIUM-ARTICLE-RELEASE-SCHEDULE.md`

---

## Mandatory Updates for All Unpublished Articles

### 1. Series Opening Blurb (MANDATORY)

**Location**: Immediately after the article title and subtitle, before the main content

**Template**:
```markdown
Part {N} of my series on {Series Name}. Last time, we explored {previous topic} — {brief description}. This time: {current topic}. Follow along for more {series theme}.
```

**Purpose**:
- Provides context for new readers
- Creates continuity across series
- Encourages exploration of previous articles
- Improves SEO through internal linking

**Special Case - First Article in Series**:
For the first article, use a modified opening:
```markdown
Part 1 of my new series on {Series Name}. In this series, we'll explore {series overview}. This time: {current topic}. Follow along for {series theme}.
```

### 2. Series Navigation Section (MANDATORY)

**Location**: At the end of the article, after main content, before author bio

**Template**:
```markdown
---

## Series Navigation

**Previous Article**: [Title of Previous Article](link)

**Next Article**: [Title of Next Article](link) *(Coming soon!)*

**Coming Up**: Topic 1, topic 2, topic 3, topic 4
```

**Guidelines**:
- Use horizontal rule (---) to separate from main content
- Link to previous article (if exists, otherwise omit this line)
- Link to next article (if published) or note "Coming soon!"
- List 3-5 upcoming topics (2-3 words each, lowercase)
- Keep topic names concise and descriptive
- Update previous articles when new ones are published

**Special Case - First Article**:
```markdown
---

## Series Navigation

**Next Article**: [Title of Next Article](link) *(Coming soon!)*

**Coming Up**: Topic 1, Topic 2, Topic 3, Topic 4, Topic 5
```

**Special Case - Last Article**:
```markdown
---

## Series Navigation

**Previous Article**: [Title of Previous Article](link)

**Series Complete**: This concludes the {Series Name} series. Check out the full series index [here](link).
```

### 3. SEO Optimization Checklist

Before publishing, verify each article meets these SEO requirements:

#### Title Optimization
- [ ] Title is 60-70 characters
- [ ] Primary keyword near the beginning
- [ ] Clear and intriguing (not clickbait)
- [ ] Numbers used when relevant

#### Keyword Strategy
- [ ] Primary keyword identified
- [ ] Primary keyword in first paragraph
- [ ] Primary keyword in at least 2 subheadings
- [ ] 3-5 secondary keywords identified
- [ ] Keywords used naturally (1-2% density)

#### Subheading Optimization
- [ ] H2/H3 headings include keywords
- [ ] Question format used where appropriate
- [ ] Descriptive and scannable

#### Internal/External Linking
- [ ] 3-5 internal links to related articles
- [ ] 3-5 external links to authority sources
- [ ] Keyword-rich anchor text
- [ ] Series navigation links included

#### Tag Strategy
- [ ] All 5 Medium tags used
- [ ] Primary tag first
- [ ] Mix of broad and specific tags
- [ ] Tags have 10K+ followers when possible

#### Image Optimization
- [ ] Cover image selected/created
- [ ] Alt text on all images
- [ ] Descriptive file names

#### Content Structure
- [ ] Word count 1,500-2,500 words
- [ ] Paragraphs 2-4 sentences
- [ ] Bullet points for lists
- [ ] Code blocks formatted properly

---

## Article-Specific Update Requirements

### Communication Series

#### Part 2: Navigating Executive Disagreement (Feb 14, 2025)

**Status**: Draft exists (v1)
**Updates Needed**:

1. **Series Opening Blurb**:
```markdown
Part 2 of my series on Technical Communication. Last time, we explored speaking executive — the foundational principles of C-suite communication. This time: navigating stakeholder dynamics when executives disagree in front of you. Follow along for more deep dives into technical leadership communication.
```

2. **Series Navigation** (add at end):
```markdown
---

## Series Navigation

**Previous Article**: [Speaking Executive: A Technical Guide to C-Suite Communication](link-to-part-1)

**Next Article**: [The Technical Presentation Playbook: Tailoring to Every Audience](link) *(Coming soon!)*

**Coming Up**: Architecture reviews, design reviews, technical writing, technical debt
```

3. **SEO Keywords**:
- Primary: "stakeholder management"
- Secondary: "executive disagreement", "technical leadership", "stakeholder dynamics", "political skills"
- Long-tail: "navigating executive disagreement", "handling stakeholder conflict"

4. **Tags**:
1. Technical Leadership
2. Stakeholder Management
3. Executive Communication
4. Engineering Leadership
5. Software Architecture

#### Part 3: The Technical Presentation Playbook (Feb 21, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 3 of my series on Technical Communication. Last time, we explored navigating stakeholder dynamics — how to handle executive disagreement with grace. This time: tailoring your technical presentations to any audience, from C-suite to engineers. Follow along for more technical leadership communication strategies.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [Navigating Executive Disagreement: Stakeholder Dynamics](link-to-part-2)

**Next Article**: [The Architecture Review Survival Guide](link) *(Coming soon!)*

**Coming Up**: Design reviews, technical writing, technical debt, cross-functional communication
```

#### Part 4: Architecture Review Survival Guide (Feb 28, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 4 of my series on Technical Communication. Last time, we explored the technical presentation playbook — adapting your message to any audience. This time: surviving (and thriving in) architecture reviews without getting torn apart. Follow along for more technical leadership strategies.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [The Technical Presentation Playbook: Tailoring to Every Audience](link-to-part-3)

**Next Article**: [The Design Review Playbook: Facilitating Technical Discussions](link) *(Coming soon!)*

**Coming Up**: Technical writing, technical debt, cross-functional communication
```

#### Part 5: Design Review Playbook (Mar 7, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 5 of my series on Technical Communication. Last time, we explored architecture review survival — defending your designs without getting defensive. This time: facilitating design reviews that actually improve the design (not just the politics). Follow along for more technical leadership insights.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [The Architecture Review Survival Guide](link-to-part-4)

**Next Article**: [Writing Technical Documents That Non-Technical People Actually Read](link) *(Coming soon!)*

**Coming Up**: Technical debt, cross-functional communication
```

#### Part 6: Writing Technical Documents (Mar 14, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 6 of my series on Technical Communication. Last time, we explored design review facilitation — running reviews that improve designs, not egos. This time: writing technical documents that non-technical people actually read (and understand). Follow along for more communication strategies.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [The Design Review Playbook: Facilitating Technical Discussions](link-to-part-5)

**Next Article**: [Communicating Technical Debt to Non-Technical Stakeholders](link) *(Coming soon!)*

**Coming Up**: Cross-functional communication
```

#### Part 7: Communicating Technical Debt (Mar 21, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 7 of my series on Technical Communication. Last time, we explored writing technical documents that non-technical people actually read. This time: explaining technical debt to stakeholders who only care about features and deadlines. Follow along for the final installment in this series.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [Writing Technical Documents That Non-Technical People Actually Read](link-to-part-6)

**Next Article**: [Cross-Functional Communication: Engineering, Product, and Design](link) *(Coming soon!)*

**Coming Up**: Series finale
```

#### Part 8: Cross-Functional Communication (Mar 28, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 8 of my series on Technical Communication. Last time, we explored communicating technical debt to non-technical stakeholders. This time: the final piece — mastering cross-functional communication between engineering, product, and design. Follow along for the conclusion of this series.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [Communicating Technical Debt to Non-Technical Stakeholders](link-to-part-7)

**Series Complete**: This concludes the Technical Communication series. Check out all 8 articles:
1. Speaking Executive: A Technical Guide to C-Suite Communication
2. Navigating Executive Disagreement: Stakeholder Dynamics
3. The Technical Presentation Playbook: Tailoring to Every Audience
4. The Architecture Review Survival Guide
5. The Design Review Playbook: Facilitating Technical Discussions
6. Writing Technical Documents That Non-Technical People Actually Read
7. Communicating Technical Debt to Non-Technical Stakeholders
8. Cross-Functional Communication: Engineering, Product, and Design
```

---

### Green Coding Series

#### Part 5: Sustainable Microservices Architecture (Feb 17, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 5 of my series on Sustainable Software Engineering. Last time, we explored building carbon-aware applications — when and where you run code matters as much as how you write it. This time: sustainable microservices architecture patterns that reduce both energy costs and your cloud bill. Follow along for more green coding practices.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [Building Carbon-Aware Applications](link-to-part-4)

**Next Article**: [Green DevOps Practices](link) *(Coming soon!)*

**Coming Up**: AI/ML sustainability, language efficiency, workload placement
```

3. **SEO Keywords**:
- Primary: "sustainable microservices"
- Secondary: "green architecture", "energy-efficient services", "carbon-aware design", "sustainable software"
- Long-tail: "building sustainable microservices architecture", "reducing microservices energy consumption"

4. **Tags**:
1. Green Coding
2. Microservices
3. Sustainable Software
4. Software Architecture
5. Cloud Computing

#### Part 6: Green DevOps Practices (Feb 24, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 6 of my series on Sustainable Software Engineering. Last time, we explored sustainable microservices architecture — patterns that reduce energy waste at scale. This time: green DevOps practices that cut carbon emissions across your entire deployment pipeline. Follow along for more sustainable development strategies.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [Sustainable Microservices Architecture](link-to-part-5)

**Next Article**: [Sustainable AI/ML and MLOps](link) *(Coming soon!)*

**Coming Up**: Language efficiency, workload placement
```

#### Part 7: Sustainable AI/ML and MLOps (Mar 3, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 7 of my series on Sustainable Software Engineering. Last time, we explored green DevOps practices — reducing carbon across your deployment pipeline. This time: sustainable AI/ML and MLOps strategies, because training models doesn't have to cost the earth (literally). Follow along for more green coding insights.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [Green DevOps Practices](link-to-part-6)

**Next Article**: [Programming Language Efficiency Deep Dive](link) *(Coming soon!)*

**Coming Up**: Workload placement
```

#### Part 8: Programming Language Efficiency Deep Dive (Mar 10, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 8 of my series on Sustainable Software Engineering. Last time, we explored sustainable AI/ML and MLOps — training models without burning the planet. This time: a deep dive into programming language efficiency and when language choice actually matters for energy consumption. Follow along for the penultimate article in this series.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [Sustainable AI/ML and MLOps](link-to-part-7)

**Next Article**: [Carbon-Aware Workload Placement Strategies](link) *(Coming soon!)*

**Coming Up**: Series finale
```

#### Part 9: Carbon-Aware Workload Placement (Mar 17, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 9 of my series on Sustainable Software Engineering. Last time, we explored programming language efficiency — when your language choice actually impacts energy consumption. This time: carbon-aware workload placement strategies that automatically shift compute to cleaner grids. Follow along for the conclusion of this series.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [Programming Language Efficiency Deep Dive](link-to-part-8)

**Series Complete**: This concludes the Sustainable Software Engineering series. Check out all 9 articles:
1. Why Your Code's Carbon Footprint Matters (And How to Measure It)
2. Energy-Efficient Algorithm Patterns
3. Database Optimization Strategies That Cut Energy Costs
4. Building Carbon-Aware Applications
5. Sustainable Microservices Architecture
6. Green DevOps Practices
7. Sustainable AI/ML and MLOps
8. Programming Language Efficiency Deep Dive
9. Carbon-Aware Workload Placement Strategies
```

---

### Resilience Engineering Series

#### Part 2: Chaos Engineering in Production (Feb 12, 2025)

**Status**: Draft exists
**Updates Needed**:

1. **Series Opening Blurb**:
```markdown
Part 2 of my series on Resilience Engineering. Last time, we explored cell-based architecture and circuit breakers — the foundation of resilient systems. This time: chaos engineering in production, or how to break things on purpose so they don't break by accident. Follow along for more resilience patterns.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [Cell-Based Architecture & Circuit Breakers](link-to-part-1)

**Next Article**: [The $10M Blind Spot: Why Your Monitoring is Lying to You](link) *(Coming soon!)*

**Coming Up**: Graceful failures, infrastructure apocalypse, rate limiting, bulkhead pattern
```

3. **SEO Keywords**:
- Primary: "chaos engineering"
- Secondary: "production testing", "resilience testing", "failure injection", "chaos monkey"
- Long-tail: "chaos engineering in production", "breaking things on purpose"

4. **Tags**:
1. Chaos Engineering
2. Resilience Engineering
3. Site Reliability
4. DevOps
5. System Design

#### Part 3: The $10M Blind Spot (Feb 19, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 3 of my series on Resilience Engineering. Last time, we explored chaos engineering — breaking things on purpose to find weaknesses. This time: the $10M blind spot in your monitoring that's lying to you right now. Follow along for more resilience insights.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [Chaos Engineering in Production: Breaking Things on Purpose](link-to-part-2)

**Next Article**: [When Everything Fails: The Art of Failing Gracefully](link) *(Coming soon!)*

**Coming Up**: Infrastructure apocalypse, rate limiting, bulkhead pattern, incident response
```

#### Part 4: When Everything Fails (Feb 26, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 4 of my series on Resilience Engineering. Last time, we explored the $10M blind spot — why your monitoring is lying to you. This time: when everything fails, the art of failing gracefully and keeping the lights on. Follow along for more resilience strategies.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [The $10M Blind Spot: Why Your Monitoring is Lying to You](link-to-part-3)

**Next Article**: [The Day AWS Went Down: Surviving Infrastructure Apocalypse](link) *(Coming soon!)*

**Coming Up**: Rate limiting, bulkhead pattern, incident response, database resilience
```

#### Part 5: The Day AWS Went Down (Mar 5, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 5 of my series on Resilience Engineering. Last time, we explored failing gracefully — keeping the lights on when everything breaks. This time: surviving infrastructure apocalypse when AWS (or any cloud provider) goes down. Follow along for more resilience patterns.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [When Everything Fails: The Art of Failing Gracefully](link-to-part-4)

**Next Article**: [Rate Limiting and Backpressure: Protecting Systems from Themselves](link) *(Coming soon!)*

**Coming Up**: Bulkhead pattern, incident response, database resilience, cost analysis
```

#### Part 6: Rate Limiting and Backpressure (Mar 12, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 6 of my series on Resilience Engineering. Last time, we explored surviving infrastructure apocalypse — when AWS goes down. This time: rate limiting and backpressure strategies that protect your systems from themselves. Follow along for more resilience techniques.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [The Day AWS Went Down: Surviving Infrastructure Apocalypse](link-to-part-5)

**Next Article**: [The Bulkhead Pattern: Isolating Failure Domains](link) *(Coming soon!)*

**Coming Up**: Incident response, database resilience, cost analysis, Kubernetes patterns
```

#### Part 7: The Bulkhead Pattern (Mar 19, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 7 of my series on Resilience Engineering. Last time, we explored rate limiting and backpressure — protecting systems from themselves. This time: the bulkhead pattern for isolating failure domains so one problem doesn't sink the whole ship. Follow along for more resilience patterns.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [Rate Limiting and Backpressure: Protecting Systems from Themselves](link-to-part-6)

**Next Article**: [Incident Response: From Detection to Resolution in 10 Minutes](link) *(Coming soon!)*

**Coming Up**: Database resilience, cost analysis, Kubernetes patterns
```

#### Part 8: Incident Response (Mar 26, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 8 of my series on Resilience Engineering. Last time, we explored the bulkhead pattern — isolating failure domains to contain damage. This time: incident response strategies that get you from detection to resolution in 10 minutes (not 10 hours). Follow along for more resilience practices.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [The Bulkhead Pattern: Isolating Failure Domains](link-to-part-7)

**Next Article**: [Database Resilience: When Your Data Layer Fails](link) *(Coming soon!)*

**Coming Up**: Cost analysis, Kubernetes patterns
```

#### Part 9: Database Resilience (Apr 2, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 9 of my series on Resilience Engineering. Last time, we explored incident response — getting from detection to resolution fast. This time: database resilience strategies for when your data layer fails (and it will). Follow along for more resilience insights.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [Incident Response: From Detection to Resolution in 10 Minutes](link-to-part-8)

**Next Article**: [The Cost of Resilience: ROI Analysis for Reliability Engineering](link) *(Coming soon!)*

**Coming Up**: Kubernetes patterns
```

#### Part 10: The Cost of Resilience (Apr 9, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 10 of my series on Resilience Engineering. Last time, we explored database resilience — surviving data layer failures. This time: the cost of resilience and ROI analysis for reliability engineering (because CFOs care about numbers, not uptime). Follow along for the penultimate article in this series.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [Database Resilience: When Your Data Layer Fails](link-to-part-9)

**Next Article**: [Kubernetes Resilience Patterns: Cloud-Native Reliability](link) *(Coming soon!)*

**Coming Up**: Series finale
```

#### Part 11: Kubernetes Resilience Patterns (Apr 16, 2025)

**Status**: To be written
**Required Elements**:

1. **Series Opening Blurb**:
```markdown
Part 11 of my series on Resilience Engineering. Last time, we explored the cost of resilience — making the business case for reliability. This time: Kubernetes resilience patterns for cloud-native reliability at scale. Follow along for the conclusion of this series.
```

2. **Series Navigation**:
```markdown
---

## Series Navigation

**Previous Article**: [The Cost of Resilience: ROI Analysis for Reliability Engineering](link-to-part-10)

**Series Complete**: This concludes the Resilience Engineering series. Check out all 11 articles:
1. Cell-Based Architecture & Circuit Breakers
2. Chaos Engineering in Production: Breaking Things on Purpose
3. The $10M Blind Spot: Why Your Monitoring is Lying to You
4. When Everything Fails: The Art of Failing Gracefully
5. The Day AWS Went Down: Surviving Infrastructure Apocalypse
6. Rate Limiting and Backpressure: Protecting Systems from Themselves
7. The Bulkhead Pattern: Isolating Failure Domains
8. Incident Response: From Detection to Resolution in 10 Minutes
9. Database Resilience: When Your Data Layer Fails
10. The Cost of Resilience: ROI Analysis for Reliability Engineering
11. Kubernetes Resilience Patterns: Cloud-Native Reliability
```

---

## Implementation Workflow

### For Existing Drafts (v1 already exists)

1. **Create v2 version file**
2. **Copy v1 content to v2**
3. **Add/update series opening blurb** (after title, before main content)
4. **Add series navigation section** (at end, before author bio)
5. **Verify SEO checklist** (title, keywords, tags, links)
6. **Update TODO.md** with version history

### For Articles Not Yet Written

1. **Create article directory structure**
2. **Create proposal (optional)**
3. **Write v1 with all required elements**:
   - Series opening blurb
   - Main content
   - Series navigation section
   - Author bio
4. **Verify SEO checklist**
5. **Create TODO.md**

---

## Quality Assurance Checklist

Before marking any article as "Ready to Publish":

- [ ] Series opening blurb present and accurate
- [ ] Series navigation section present with correct links
- [ ] Previous article link works (if not first article)
- [ ] "Coming Up" topics listed (3-5 items)
- [ ] SEO title optimized (60-70 characters)
- [ ] Primary keyword in first paragraph
- [ ] Primary keyword in 2+ subheadings
- [ ] 3-5 internal links included
- [ ] 3-5 external links included
- [ ] All 5 Medium tags selected
- [ ] Cover image selected/created
- [ ] Alt text on all images
- [ ] Word count 1,500-2,500 words
- [ ] Proofread for grammar/spelling
- [ ] Author bio updated

---

## Timeline and Priorities

### Immediate Priority (Week of Feb 10-14)

1. **Communication Part 2** (Feb 14) - Update existing v1 to v2
2. **Resilience Part 2** (Feb 12) - Update existing draft

### High Priority (Week of Feb 17-21)

1. **Green Coding Part 5** (Feb 17) - Write with new requirements
2. **Resilience Part 3** (Feb 19) - Write with new requirements
3. **Communication Part 3** (Feb 21) - Write with new requirements

### Medium Priority (Week of Feb 24-28)

1. **Green Coding Part 6** (Feb 24)
2. **Resilience Part 4** (Feb 26)
3. **Communication Part 4** (Feb 28)

### Ongoing

Continue writing articles 2-3 weeks ahead of publication date, ensuring all new requirements are met from the start.

---

## Notes

- **Backward Compatibility**: Published articles (Parts 1-4 of Green Coding, Part 1 of Communication, Part 1 of Resilience) should be updated with series navigation sections when time permits
- **Link Updates**: As new articles are published, update "Coming soon!" links in previous articles to actual URLs
- **SEO Monitoring**: Track which articles perform best with new SEO optimizations
- **Reader Feedback**: Monitor comments for questions about series structure or navigation

---

**Status**: Active | **Created**: 2025-02-13 | **Owner**: Content Team
**Purpose**: Ensure consistency and SEO optimization across all unpublished Medium articles
**Next Review**: After first 5 articles published with new requirements

