# Medium Article Writing Process

**Purpose**: Repeatable process for creating high-quality Medium articles with version control and iterative refinement.

**Last Updated**: 2025-01-28  
**Based On**: Green Coding Intro Article Development

---

## Overview

This process ensures articles are written in a consistent voice, properly versioned, and iteratively refined based on feedback. It emphasizes conversational but intellectually authoritative tone, practical examples, and technical accuracy.

---

## Phase 1: Pre-Writing Setup

### 1.1 Create Article Directory Structure

```
for-approval/medium/{topic}/
├── {article-name}/
│   ├── versions/
│   │   ├── v1-{article-name}.md
│   │   ├── v2-{article-name}.md
│   │   └── v3-{article-name}.md
│   ├── advertising/          (created after v1 complete)
│   │   ├── linkedin-post.md
│   │   ├── x-post.md
│   │   ├── instagram-post.md
│   │   ├── facebook-post.md
│   │   ├── threads-post.md
│   │   ├── reddit-post.md
│   │   ├── teams-post.md
│   │   └── hashtag-strategy.md
│   ├── {article-name}-proposal.md
│   └── TODO.md
```

**Example**:
```
for-approval/medium/green-coding/
├── intro/
│   ├── versions/
│   │   ├── v1-intro-article.md
│   │   ├── v2-intro-article.md
│   │   ├── v3-intro-article.md
│   │   ├── v4-intro-article.md
│   │   └── v5-intro-article.md
│   ├── advertising/          (created after v1, updated with each version)
│   │   ├── linkedin-post.md
│   │   ├── x-post.md
│   │   ├── instagram-post.md
│   │   ├── facebook-post.md
│   │   ├── threads-post.md
│   │   ├── reddit-post.md
│   │   ├── teams-post.md
│   │   └── hashtag-strategy.md
│   ├── intro-article-proposal.md
│   └── TODO.md
```

**Note**: The `advertising/` directory is created AFTER v1 is complete (Phase 3.3), not during initial setup.

### 1.2 Review Writing Samples

**Action**: Read existing writing samples to understand tone and style.

**Location**: `for-approval/writing-samples/`

**Key Characteristics to Identify**:
- Conversational vs formal tone
- Technical depth and jargon usage
- Use of examples (concrete vs abstract)
- Paragraph structure and flow
- How problems are introduced and solved
- Use of humor, asides, and personality

**From Green Coding Example**:
- Direct, no fluff ("Here's the thing...")
- Conversational but authoritative ("Before you start rewriting everything in Rust...")
- Real-world examples with specific numbers
- Honest about limitations ("Not perfect, but good enough...")
- Uses asides and personality ("I lied. Sort of.")

### 1.3 Research Market Opportunity (Optional)

**Action**: Review market analysis if creating content for course/series.

**Location**: `for-approval/Market-Opportunity-Analysis-Udemy-Medium.md`

**Extract**:
- Target audience demographics
- Content gaps in existing market
- Revenue potential
- Competitive advantages
- Related article series topics

---

## Phase 2: Proposal Creation

### 2.1 Create Initial Proposal

**File**: `{article-name}-proposal.md`

**Contents**:
- Article title
- Target reading time (5-7 minutes typical)
- Target audience
- Article objective
- Major talking points (8-10 sections)
- Supporting elements (visuals, code examples)
- SEO keywords
- Success metrics
- Follow-up article teasers

**From Green Coding Example**:
```markdown
# Green Coding: Introductory Medium Article Proposal

**Article Title**: "Why Your Code's Carbon Footprint Matters (And How to Measure It)"
**Target Reading Time**: 5-7 minutes
**Target Audience**: Software engineers, technical leads, CTOs

## Article Structure & Major Talking Points
1. Hook: The Surprising Carbon Cost of Software
2. What is Green Coding?
3. Why Should Developers Care?
...
```

### 2.2 Review and Refine Proposal

**Action**: Get feedback on proposal structure and talking points.

**Questions to Ask**:
- Does the structure flow logically?
- Are all major points covered?
- Is anything missing or redundant?
- Does it match the target reading time?
- Will it resonate with the target audience?

**Note**: Proposal may be skipped if jumping straight to article writing.

---

## Phase 3: Iterative Writing Process (Natural Human Development)

**Philosophy**: Articles should evolve naturally like human writing, not appear fully formed. Early versions are rough, exploratory, and full of thinking-in-progress. This creates authentic development history and makes the writing process more manageable.

### 3.1 Version 1 - Brainstorming Outline with Exploratory Thinking

**File**: `versions/v1-{article-name}.md`

**Purpose**: Capture initial thinking and structure without committing to anything

**Contents**:
- Article title (may change completely)
- Brief introduction (rough, conversational)
- Section headings with exploratory notes
- Bullet points that sound like thinking out loud
- Questions and uncertainties embedded
- Alternative approaches considered
- Rough notes on examples needed

**Writing Style**:
- Conversational, not formal ("The Stupid Thing We All Do")
- Questions embedded ("Maybe call this section something catchier?")
- Uncertainties acknowledged ("or whatever we call it")
- Thinking visible ("Need more than just Black Friday")
- Exploratory tone ("That's insane when you think about it")

**Example v1 Structure**:
```markdown
# When Everything Fails: The Art of Failing Gracefully

Part 4 of my series on Resilience Engineering...

## Opening Hook - The 3AM Disaster

- Phone explodes with alerts at 3:47 AM
- Not just one service - EVERYTHING is red
- Circuit breakers are... wait, they're failing CLOSED? That's backwards
- Real story: Black Friday 2023, big e-commerce site
- Need the actual numbers here - wasn't it like $47M and 4 hours?
- The kicker: their resilience patterns made it WORSE
- Maybe start with the Slack message: "The circuit breakers are failing closed."

## Why Resilience Patterns Fail (The Paradox)

- We build all these patterns thinking they'll save us
- Circuit breakers stop cascades... except when they don't
- The thing nobody tells you: these patterns can fail too
- Real question: how do you make your safety nets safe?

## Principle 1: Don't Let Your Circuit Breaker Depend on Redis

**The Stupid Thing We All Do**:
- Circuit breaker stores state in Redis
- Service also uses Redis
- Redis goes down
- Circuit breaker can't track state, defaults to "closed" (allow everything)
- This is literally what happened Black Friday
- It's like having your fire extinguisher inside the burning building

**What Actually Works**:
- Keep circuit breaker state in memory, local to each instance
- No external dependencies for critical decisions
- If you can't tell what's happening, default to SAFE not SORRY

**Maybe call this section something catchier?**
- "Your Circuit Breaker Shouldn't Need Redis"
- "Failure Independence or: How I Learned to Stop Worrying"

## Making It Real (Implementation)

- Need code examples - Python probably
- Can't deploy all this at once
- Start with circuit breakers (week 1)
- This is a journey not a destination

Target: ~500 words outline (this is the skeleton, flesh out in v2)
```

**Characteristics**:
- Minimal prose, mostly rough thinking
- Questions and alternatives visible
- Conversational asides and commentary
- Uncertainty acknowledged
- Focus on capturing ideas, not polish
- Reading time: 2-3 minutes if fully written

**Checklist**:
- [ ] Title captures main idea (may evolve)
- [ ] Major sections identified
- [ ] Thinking is visible and exploratory
- [ ] Questions and uncertainties noted
- [ ] Alternative approaches considered
- [ ] Rough scope defined

### 3.2 Version 2 - Detailed Outline with Rough Draft Prose

**File**: `versions/v2-{article-name}.md`

**Purpose**: Flesh out structure with more detail, mix of rough prose and detailed bullets

**Contents**:
- Expanded introduction (rough draft prose, 1-2 paragraphs)
- Some sections in rough prose, others still bullets
- Specific examples identified with rough descriptions
- Code snippet outlines (not actual code yet)
- Table structures (headers, some data)
- TODOs that sound like thinking out loud

**Writing Style**:
- Mix of rough prose and detailed bullets
- Prose is conversational, not polished
- TODOs sound like unfinished thoughts
- Examples are specific but not fully written
- Transitions are rough or missing
- Some sections more developed than others

**Example v2 Expansion**:
```markdown
# When Everything Fails: The Art of Failing Gracefully

Part 4 of my series on Resilience Engineering...

## The Nightmare Scenario

3:47 AM. Your phone explodes with alerts. Not one or two - dozens. Every service is red. Circuit breakers are open everywhere. Fallbacks are timing out. The database connection pool is exhausted. Redis is down. The message queue is backed up with millions of messages.

Then you see the message that makes your blood run cold: "The circuit breakers are failing closed. Everything is cascading."

This isn't hypothetical. This happened to a major e-commerce platform during Black Friday 2023. Complete platform outage. 4 hours. Cost: $47 million in lost revenue, plus immeasurable damage to customer trust.

[Was it database first or Redis? Need to trace the actual cascade - probably database overload triggered everything else]

Here's the thing nobody tells you: resilience patterns can fail too. And when they fail, they often make things worse.

## The Resilience Paradox

We build all these patterns to prevent failures. Circuit breakers to stop cascades. Fallbacks to keep things running when dependencies fail. Retries to handle transient errors. Bulkheads to isolate failure domains.

But what happens when these patterns themselves become the problem?

Circuit breakers can fail closed - they should be blocking bad traffic but instead they're allowing everything through. [When state store goes down, defaults to "allow" - saw this at 3AM once, error rate went from 2% to 40% in seconds]

Fallbacks can overwhelm secondary systems. Primary fails, all traffic shifts to the fallback, but the fallback wasn't sized for full load. [Redis was doing double duty - circuit breaker state AND cache fallback. When it went down, lost both at once. Classic mistake]

So the real question isn't "how do we prevent failures?" - that's impossible. The real question is: How do you build resilience into your resilience mechanisms?

## Design Principle 1: Failure Independence

**The Problem**: Most resilience patterns share infrastructure with the systems they're protecting.

Consider a typical circuit breaker implementation. It stores state in Redis (shared dependency). Uses same thread pool as application code (shared resource). Depends on same network as protected service (shared failure domain).

[Draw this: circuit breaker → Redis ← traffic spike. Circular dependency - the thing protecting you needs the thing that's failing]

**The Design Solution**: Failure independence through architectural separation.

Your resilience mechanisms must operate independently from the systems they protect. This means three things:

First, separate failure domains. If your service fails due to database overload, your circuit breaker shouldn't depend on that same database.

Second, local-first decisions. Critical resilience decisions must be made locally without requiring external coordination. [Just count errors locally - if >5% in last 10 seconds, open circuit. Why wait for Redis to tell you what you already know?]

Third, multiple independent signals. Don't rely on a single signal for degradation. [Combine with OR logic? If ANY signal bad, degrade? Or weighted score?]

### Architectural Pattern: Isolated Failure Detection

Instead of coupling circuit breaker state to external dependencies, design for local state with eventual consistency.

Each service instance maintains circuit breaker state in-process memory. No external dependency for reads. Fast access (nanoseconds, not milliseconds). Survives network partitions.

[Just a HashMap in memory - error count, timestamp, state. No Redis, no network, no disk. Pure local]

Instances share state changes via lightweight gossip protocol, not on the critical path. [Gossip like Consul - every 5 seconds, tell neighbors "I'm seeing 10% errors". They adjust their thresholds. Eventually consistent]

Circuit decisions are based on local observations. [Sliding window of last 100 requests. Count errors. That's it. No Raft, no Paxos, no distributed consensus]

## Design Principle 2: Degradation Hierarchy

**The Problem**: Binary failure modes (working vs broken) don't reflect reality.

[Black Friday example - they had cached data but couldn't use it. Lost $47M because they couldn't process orders with 5-minute-old inventory. That's insane]

**The Design Solution**: Multi-level degradation hierarchy with explicit feature dependencies.

Not all features are equally critical. [Rank by revenue: Checkout ($1M/hour) > Product Pages ($100K/hour) > Recommendations ($10K/hour) > A/B Tests ($0)]

[Need format like: requires=[inventory:realtime], optional=[personalization], fallback=[inventory:cached]]

### Architectural Pattern: Capability-Based Degradation

Design your system as a hierarchy of capabilities, where each level depends only on capabilities below it.

Level 0 is static content with no dependencies. [CloudFront with 24-hour TTL, serve stale on error. Even if origin down, users get yesterday's data]

Level 1 is read-only data with database reads only. [Try database, if fails check Redis cache, if cache miss serve last known good value with "data may be stale" banner]

Level 2 is core transactions on the critical path only. [Skip: upsells, cross-sells, recommendations. Just: item + address + payment = done]

[Code example here - thinking something like a feature registry that maps features to their dependencies and fallback strategies... would make this way more concrete]

## Design Principle 3: Fallback Composition

[Still need to write this - show the actual loop through fallbacks, checking circuit breakers, tracking remaining latency budget]

## Design Principle 4: Resource Isolation

[Thread pools isolated but connections shared - that's the Black Friday mistake. Need to isolate: threads, connections, memory, CPU, disk I/O, network bandwidth]

## Design Principle 5: Adaptive Rate Limiting

[If error rate >5%, cut limit by 50%. If latency >1s, cut by 30%. Priority queue: checkout (priority 1), browse (priority 5), recommendations (priority 10)]

## Design Principle 6: Observability of Degradation

[Dashboard: "Checkout: DEGRADED - using 10min old inventory, 5000 users affected, $12K/hour revenue at risk". Metrics: degradation_level, affected_users, revenue_impact]

## Implementation Patterns

[Start with circuit breakers (week 1), add degradation levels (week 2), add fallback chains (week 3). Test with chaos monkey. Python examples for each]

## Real-World Case Studies

[AWS S3 2017 (typo in command), Netflix Chaos Monkey (kill instances in prod), Google SRE error budgets (spend your 0.1% downtime wisely)]

## The Tradeoffs

[Math: if downtime costs $10M/hour and this takes 6 months ($500K), break even after 3 minutes of prevented downtime. Worth it. If downtime costs $100/hour? Not worth it]

Target: ~1,800 words when complete
```

**Characteristics**:
- Mix of rough prose and detailed bullets
- Prose is conversational, not polished
- TODOs sound like unfinished human thoughts
- Examples are specific but not fully fleshed out
- Some sections more developed than others
- Transitions are rough or missing
- Reading time: 4-5 minutes if fully written

**Checklist**:
- [ ] Some sections have rough prose
- [ ] Other sections still in bullets
- [ ] Examples are specific (not generic)
- [ ] TODOs sound like thinking out loud
- [ ] Code snippets are outlined
- [ ] Tables have structure
- [ ] Natural mix of polish levels

### 3.3 Version 3 - First Full Prose Version

**File**: `versions/v3-{article-name}.md`

**Purpose**: Convert outline to readable article with full sentences and paragraphs

**Contents**:
- Complete introduction with hook
- Full paragraphs for each section
- Concrete examples with real numbers
- Actual code snippets (working code)
- Completed tables with data
- Transitions between sections
- Conclusion with takeaways

**Example v3 Full Prose**:
```markdown
# Why Your Code's Carbon Footprint Matters (And How to Measure It)

Your code has a carbon footprint. Every API call, database query, and algorithm you write consumes electricity — and that electricity often comes from fossil fuels. Here's the thing: most developers have no idea how much energy their code uses, or how to measure it.

According to the Green Software Foundation, software is responsible for approximately 2-3% of global carbon emissions. That's roughly equivalent to the aviation industry. And unlike planes, which we can see and hear, software's environmental impact is invisible.

This guide will show you exactly how to measure your code's environmental impact and what to do about it.

## What is Green Coding?

Green coding is the practice of writing software that minimizes energy consumption and environmental impact. It's not about sacrificing performance or user experience — it's about being intentional with resource usage.

The core principle is simple: efficient code is green code. When you optimize for performance, you're usually optimizing for energy efficiency too. A faster algorithm uses less CPU time, which means less electricity, which means lower carbon emissions.

But green coding goes beyond just writing fast code. It's about:

- **Choosing efficient algorithms and data structures**: An O(n log n) sort uses 35x less energy than an O(n²) sort on 10,000 items
- **Optimizing resource usage**: Shutting down idle resources, using appropriate instance sizes
- **Measuring impact**: You can't improve what you don't measure
- **Making informed tradeoffs**: Sometimes a slightly slower algorithm is worth it for other reasons

## The Hidden Costs

Let's talk about where your code is wasting energy right now.

### Inefficient Algorithms

Consider a simple lookup operation. If you're using a List to check if an item exists, you're doing an O(n) operation. Switch to a HashMap, and it's O(1). On a list of 10,000 items, that's the difference between 10,000 comparisons and 1 lookup.

```python
# Inefficient: O(n) lookup
user_ids = [1, 2, 3, ..., 10000]
if user_id in user_ids:  # Checks every item
    process_user(user_id)

# Efficient: O(1) lookup
user_ids = {1, 2, 3, ..., 10000}  # Set (HashMap)
if user_id in user_ids:  # Single hash lookup
    process_user(user_id)
```

If this code runs 1 million times per day, you've just eliminated 10 billion unnecessary comparisons. That's real energy savings.

### Idle Resources

[Continue with full prose for remaining sections...]

## Measurement Tools

### Cloud Carbon Footprint

Cloud Carbon Footprint is an open-source tool that estimates the carbon emissions of your cloud infrastructure. It integrates with AWS, Azure, and GCP to analyze your usage and calculate emissions.

```bash
# Install
npm install -g @cloud-carbon-footprint/cli

# Run analysis
ccf estimate --startDate 2024-01-01 --endDate 2024-01-31
```

The tool provides:
- Emissions by service (EC2, Lambda, S3, etc.)
- Cost vs emissions tradeoffs
- Recommendations for optimization

[Continue with other tools...]

## Quick Wins

Here are five things you can do today to reduce your code's carbon footprint:

1. **Use efficient data structures**: Replace List lookups with HashMap/Set. On 10,000 items, this is 10,000x faster and uses proportionally less energy.

2. **Shut down idle resources**: That staging environment running 24/7? Shut it down at night. That's 12 hours of wasted electricity every day.

[Continue with remaining quick wins...]

## Resources

- [Green Software Foundation](https://greensoftware.foundation/) - Standards and best practices
- [Cloud Carbon Footprint](https://www.cloudcarbonfootprint.org/) - Open source emissions calculator
- [CodeCarbon](https://codecarbon.io/) - Python library for tracking ML emissions
- [Electricity Maps](https://app.electricitymaps.com/) - Real-time carbon intensity by region

---

**Coming Up**: In the next article, we'll dive deep into algorithm optimization patterns and show you exactly which code patterns waste the most energy.
```

**Characteristics**:
- Full sentences and paragraphs
- Conversational but authoritative tone
- Concrete examples with real numbers
- Working code snippets
- Complete tables with data
- Smooth transitions
- Reading time: 6-8 minutes

**Checklist**:
- [ ] All placeholders replaced with content
- [ ] Examples are concrete and specific
- [ ] Code snippets are tested and working
- [ ] Tables have complete data
- [ ] Tone is consistent throughout
- [ ] Transitions flow naturally

### 3.4 Version 4 - First Publishable Version

**File**: `versions/v4-{article-name}.md`

**Purpose**: Polish v3 into publication-ready article

**Changes from v3**:
- Refine introduction hook
- Add catchy subtitle to YAML front matter (see below)
- Add more concrete examples
- Improve transitions between sections
- Add nuance and balance
- Verify all numbers and statistics
- Add more resources
- Polish conclusion
- Add SEO elements (keywords, tags)

**Catchy Subtitle (MANDATORY for v4)**:
The subtitle in the YAML front matter must be punchy, hook-driven, and concise — not just a restatement of the title or a dry description. It should make the reader feel something or create curiosity. Think of it as the line that sells the click after the title gets attention.

**Good Subtitles**:
- "C is 75x more energy-efficient than Python. Your Rust evangelist won't shut up about it. Here's what the benchmarks actually mean for your codebase."
- "The gap between 'cool demo' and 'production agent' is massive. Here's how to close it with working code."
- "10x traffic. Everything's on fire. Nothing is broken — your system just never learned to say 'no.'"

**Bad Subtitles**:
- "A practical guide to building agentic AI systems" (boring, restates title)
- "Learn about rate limiting and backpressure patterns" (dry, no hook)
- "This article covers programming language efficiency" (reads like a textbook)

**Focus Areas**:
- **Clarity**: Is every sentence clear?
- **Flow**: Do sections connect smoothly?
- **Evidence**: Are claims backed by data?
- **Balance**: Are tradeoffs acknowledged?
- **Actionability**: Can readers apply this?

**Example v4 Refinements**:
```markdown
# Why Your Code's Carbon Footprint Matters (And How to Measure It)

[Same intro, but refined hook]

Your code has a carbon footprint. Every API call, database query, and algorithm you write consumes electricity — and that electricity often comes from fossil fuels. Here's the thing: most developers have no idea how much energy their code uses, or how to measure it.

According to the Green Software Foundation, software is responsible for approximately 2-3% of global carbon emissions. That's roughly equivalent to the aviation industry. And unlike planes, which we can see and hear, software's environmental impact is invisible.

But here's the good news: measuring and reducing your code's carbon footprint isn't complicated. You don't need to rewrite everything in Rust or abandon cloud computing. You just need to be intentional about a few key decisions.

This guide will show you exactly how to measure your code's environmental impact and what to do about it.

[Rest of article with refinements...]

## Green Coding Doesn't Happen in a Vacuum

Before you start rewriting everything for energy efficiency, let's be realistic: green coding is one factor among many.

You're also dealing with:
- **Data residency requirements**: Can't always choose the greenest region
- **Disaster recovery**: Redundancy costs energy
- **Compliance**: Some regulations require specific infrastructure
- **Performance SLAs**: Sometimes you need that extra compute
- **Cost constraints**: Green isn't always cheap

The goal isn't to sacrifice everything for energy efficiency. It's to make energy efficiency a factor in your decisions, alongside performance, cost, and reliability.

When you're choosing between two algorithms with similar performance, pick the more efficient one. When you're provisioning infrastructure, consider carbon intensity alongside cost. When you're designing systems, think about idle resources.

Small, intentional decisions add up.

[Conclusion with refined takeaways...]
```

**Characteristics**:
- Polished prose
- Balanced perspective
- Acknowledges tradeoffs
- More nuanced arguments
- Better examples
- Stronger conclusion
- Reading time: 7-9 minutes

**Checklist**:
- [ ] Hook is compelling
- [ ] Catchy subtitle in YAML front matter (punchy, hook-driven — not a dry description)
- [ ] All claims are supported
- [ ] Tradeoffs are acknowledged
- [ ] Examples are the best available
- [ ] Conclusion is actionable
- [ ] SEO elements added
- [ ] Ready for publication

### 3.5 Version 5+ - Post-Publication Refinements

**File**: `versions/v5-{article-name}.md`, `v6-{article-name}.md`, etc.

**Purpose**: Incorporate feedback, add depth, fix issues

**Triggers for New Versions**:
- Reader feedback requesting clarification
- New examples or data available
- Redundant content identified
- Better way to explain concept
- Related article published (add cross-links)
- Industry changes (update statistics)

**Process**:
1. Read feedback/comments
2. Identify specific improvements
3. Create new version with changes
4. Update Medium article
5. Document changes in TODO.md

**Example v5 Changes**:
- Added "Green Coding Doesn't Happen in a Vacuum" section
- Addressed tradeoffs with other NFRs
- Added more nuance about practical constraints
- Updated statistics with latest data
- Added cross-links to related articles

**Characteristics**:
- Responds to real feedback
- Adds depth without bloat
- Maintains original structure
- Improves clarity
- Updates outdated information

---

## Phase 4: Advertising Infrastructure (After v3 or v4)

### 4.1 When to Create Advertising

**Trigger**: After v3 (first full prose) or v4 (first publishable) is complete

**Why Wait**:
- Need actual content to reference
- Need concrete examples and numbers
- Need to know article's actual focus
- Need to understand tone and voice

**Don't Create Too Early**:
- v1 (outline) - too early, content will change
- v2 (bullets) - still too early, examples not concrete
- v3 (full prose) - good time, content is real
- v4 (publishable) - also good, content is polished

### 4.2 Create Advertising Directory

**Action**: Create `advertising/` directory with 7 files

**Process**:
1. Read latest version (v3 or v4) completely
2. Extract key points, examples, and numbers
3. Create platform-specific posts using templates
4. Verify character counts and hashtag limits
5. Add to TODO.md: "Advertising infrastructure created for v{N}"

**Files to Create**:
- `advertising/linkedin-post.md` - Professional, detailed
- `advertising/x-post.md` - Concise + thread version
- `advertising/instagram-post.md` - Visual, link in bio
- `advertising/facebook-post.md` - Detailed, direct link
- `advertising/threads-post.md` - Conversational
- `advertising/reddit-post.md` - Authentic, discussion-focused
- `advertising/teams-post.md` - Internal, images/formatting OK
- `advertising/hashtag-strategy.md` - Platform-specific hashtag research

### 4.3 Update Advertising with Each Version

**Trigger**: After creating v4, v5, v6, etc.

**Process**:
1. Review changes in new version
2. Identify new examples or key points
3. Update advertising files if needed
4. Document in TODO.md

**When to Update**:
- New compelling example with numbers
- Better hook or opening line
- Article focus shifted
- New sections added

**When NOT to Update**:
- Minor wording changes
- Typo fixes
- Small clarifications
- Same key points

---

## Phase 5: Version Control Best Practices

### 5.1 Never Modify Existing Versions

**Rule**: Once a version is created, NEVER modify it. Always create a new version.

**Why**:
- Preserves development history
- Shows natural evolution of ideas
- Allows comparison between versions
- Maintains audit trail

**Process**:
1. Copy previous version as starting point
2. Make changes in new version file
3. Update version number in filename
4. Document changes in TODO.md

### 5.2 Version Naming Convention

**Format**: `v{N}-{article-name}.md`

**Examples**:
- `v1-intro-article.md` - Title and outline
- `v2-intro-article.md` - Bullet points and detail
- `v3-intro-article.md` - First full prose
- `v4-intro-article.md` - First publishable
- `v5-intro-article.md` - Post-publication refinement

### 5.3 Document Version Changes

**File**: `TODO.md`

**Version History Section**:
```markdown
## Version History
- **v1** (2025-01-28): Title and rough outline created
- **v2** (2025-01-28): Added bullet points and detailed placeholders
- **v3** (2025-01-28): First full prose version with complete paragraphs
- **v4** (2025-01-28): First publishable version, polished and balanced
- **v5** (2025-01-29): Added tradeoffs section based on feedback
```

**Change Documentation**:
- Date of version creation
- Brief description of changes
- Reason for changes (if applicable)
- Word count and reading time (if changed significantly)

### 5.4 Version Comparison Techniques

**For Small Changes** (v1 → v2, v2 → v3):
- Simple change list in TODO.md
- Note major additions or removals

**For Major Changes** (v3 → v4, v4 → v5):
- Create side-by-side HTML comparison (see Phase 4.5)
- Visual diff for editing published articles
- Actionable change list

### 5.5 TODO List Management

**File**: `TODO.md`

**Contents**:
- Version history (see 5.3)
- Content additions needed (by priority)
- Editorial review checklist
- Pre-publication checklist
- Follow-up article references
- Research notes
- Advertising update log

**Example Structure**:
```markdown
# {Article Name} - TODO

## Version History
[See 5.3 above]

## Content Additions Needed

### High Priority
- [ ] Add section on X
  - Placement: After section Y
  - Tone: Pragmatic, not preachy
  
### Medium Priority
- [ ] Add specific numbers for Z
- [ ] Include real-world case study

### Low Priority
- [ ] Consider adding diagram for concept A

## Advertising Updates
- **v1** (2025-01-28): Initial advertising created
- **v3** (2025-01-28): Updated with new examples
- **v4** (2025-01-28): No changes needed (same key points)

## Pre-Publication Checklist
- [ ] All examples are concrete
- [ ] All numbers verified
- [ ] All links working
- [ ] SEO checklist complete
- [ ] Cover image selected
```

---

## Phase 4: Iterative Refinement

### 4.1 Version 2+ - Add Major Content

**Trigger**: Feedback requesting new sections or major additions

**Process**:
1. Create new version file: `v{N}-{article-name}.md`
2. Copy previous version as starting point
3. Add new section(s) in appropriate location
4. Ensure smooth transitions
5. Update word count and reading time
6. Update TODO list
7. **Review and update advertising materials** (see 4.6)

**From Green Coding Example**:
- **v2**: Added programming language efficiency section
  - Placed after "Hidden Carbon Costs"
  - Added efficiency spectrum (C/Rust → Python/Ruby)
  - Emphasized when language choice matters
  - ~2,000 words, 7-8 minute read

### 4.2 Version 3+ - Expand Existing Content

**Trigger**: Feedback requesting deeper coverage of existing topics

**Process**:
1. Create new version file
2. Identify section to expand
3. Add subsections or examples
4. Maintain flow and readability
5. Update resources if needed
6. **Review and update advertising materials** (see 4.6)

**From Green Coding Example**:
- **v3**: Expanded "Where Your Code Runs" section
  - Added carbon intensity by region (Norway vs India)
  - Added carbon-aware computing subsection
  - Added time-of-day variations
  - Updated quick wins and resources
  - ~2,200 words, 8-9 minute read

### 4.3 Version 4+ - Refine and Deduplicate

**Trigger**: Feedback about redundancy or clarity issues

**Process**:
1. Create new version file
2. Identify redundant content
3. Replace with different examples serving same purpose
4. Ensure each example is unique
5. Verify smooth transitions
6. **Review and update advertising materials** (see 4.6)

**From Green Coding Example**:
- **v4**: Removed redundant algorithm example
  - Replaced O(n²) vs O(n log n) in "Inefficient Algorithms"
  - Used HashMap vs List example instead
  - Kept original example in "Technical Case" section
  - Same word count, improved clarity

### 4.4 Version 5+ - Add Nuance and Balance

**Trigger**: Feedback requesting acknowledgment of tradeoffs or real-world constraints

**Process**:
1. Create new version file
2. Add section addressing practical constraints
3. Acknowledge competing requirements
4. Provide balanced perspective
5. Maintain optimistic but realistic tone
6. **Review and update advertising materials** (see 4.6)

**From Green Coding Example**:
- **v5**: Added "Green Coding Doesn't Happen in a Vacuum"
  - Addressed tradeoffs with other NFRs
  - Covered data residency, DR, compliance conflicts
  - Positioned energy efficiency as one factor among many
  - Emphasized SDLC integration
  - ~2,600 words, 10-11 minute read

### 4.5 Version Comparison - Side-by-Side HTML Technique

**Trigger**: Need to edit published Medium article from one version to another

**Problem**: Command-line diffs are hard to read. Simple change lists lack visual context. You need a clear, visual way to see what changed between versions to edit your Medium article efficiently.

**Solution**: Create an HTML side-by-side comparison that opens in a browser.

**Process**:
1. Create HTML file: `versions/v{old}-to-v{new}-side-by-side.html`
2. Use two-column layout (old version left, new version right)
3. Color-code changes:
   - Red background: Content removed in new version
   - Green background: Content added in new version
   - Yellow background: Content changed in new version
4. Include summary section at bottom with actionable steps
5. Make responsive for mobile/tablet viewing

**HTML Template Structure**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Article Comparison: v{old} to v{new}</title>
    <style>
        .comparison { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .removed { background: #ffe0e0; }
        .added { background: #d4f4dd; }
        .changed { background: #fff3cd; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Article: v{old} → v{new} Comparison</h1>
        <div class="stats">
            <strong>v{old}:</strong> {lines} lines | 
            <strong>v{new}:</strong> {lines} lines | 
            <strong>Reduction:</strong> {percent}% shorter
        </div>
    </div>
    
    <div class="comparison">
        <div class="version v{old}">
            <h2>v{old} (Original)</h2>
            <!-- Section-by-section comparison -->
        </div>
        <div class="version v{new}">
            <h2>v{new} (Revised)</h2>
            <!-- Section-by-section comparison -->
        </div>
    </div>
    
    <div class="summary">
        <h1>Key Changes Summary</h1>
        <h3>What to Do in Medium Editor:</h3>
        <ol>
            <li>Specific actionable steps</li>
        </ol>
    </div>
</body>
</html>
```

**From Database Optimization Example**:
- **v2 to v5 comparison**: 2,478 lines → 650 lines (74% reduction)
- Created `v2-to-v5-side-by-side.html`
- Showed removed "How It Works" sections in red
- Showed combined Pattern 9 in green
- Provided clear action list for Medium editing
- File opened in browser for easy visual scanning

**Benefits**:
- Visual, easy-to-scan comparison
- Works on any device (responsive design)
- Color coding makes changes obvious
- Actionable summary at bottom
- Much better than command-line diff output
- Can be shared with editors/reviewers

**When to Use**:
- Editing published Medium article from old to new version
- Major restructuring between versions (not just typo fixes)
- Need to explain changes to editor or reviewer
- Want visual reference while editing in Medium's editor
- Comparing versions with 20%+ content changes

**When NOT to Use**:
- Minor typo fixes (just edit directly)
- Small wording changes (use simple change list)
- Adding single paragraph (obvious without comparison)
- First draft to publication (no prior version to compare)

### 4.6 Update Advertising Materials After Each Major Revision (MANDATORY)

**Trigger**: After creating any new version (v2, v3, v4, etc.)

**Why**: Advertising materials must reflect current article content, examples, and key points

**Process**:

**Step 1: Review Changes**
- Read the new version completely
- Identify new sections, examples, or key points
- Note any removed or changed content
- Check if article focus or tone shifted

**Step 2: Evaluate Impact on Advertising**
- Do new examples make better hooks?
- Are there better numbers/statistics to highlight?
- Did the article's main value proposition change?
- Are current hashtags still relevant?

**Step 3: Update Files (If Needed)**

**Update linkedin-post.md if**:
- New compelling example with concrete numbers
- Better hook or opening line
- Article focus shifted significantly
- New key points worth highlighting

**Update x-post.md if**:
- Better concise hook (under 280 chars)
- Thread needs new tweets for new sections
- Main value proposition changed

**Update instagram-post.md if**:
- New visual examples or concepts
- Better engagement question
- Key points changed

**Update facebook-post.md if**:
- New detailed examples worth explaining
- Article expanded significantly
- Better engagement angle

**Update threads-post.md if**:
- New conversational angle
- Better discussion prompt
- Key points changed

**Update reddit-post.md if**:
- New technical depth worth highlighting
- Better discussion questions
- New subreddits become relevant

**Update hashtag-strategy.md if**:
- Article topic expanded to new areas
- New trending hashtags emerged
- Better niche tags discovered

**Step 4: Document Updates**

Add to TODO.md:
```markdown
## Version History
- **v1** (2025-01-28): Initial draft, advertising created
- **v2** (2025-01-28): Added programming language section
  - Updated advertising: New hook using language efficiency example
- **v3** (2025-01-28): Added carbon intensity by region
  - Updated advertising: Added regional examples to posts
- **v4** (2025-01-28): Replaced redundant algorithm example
  - Advertising: No changes needed (same key points)
- **v5** (2025-01-28): Added tradeoffs and NFR section
  - Updated advertising: Added nuance about tradeoffs to LinkedIn/Facebook posts
```

**Decision Matrix**:

| Change Type | Update Advertising? | Which Files? |
|-------------|---------------------|--------------|
| New major section | Yes | All platform posts |
| Expanded existing section | Maybe | LinkedIn, Facebook (detailed posts) |
| Better example/number | Yes | All posts (better hook) |
| Removed redundancy | No | Keep existing (unless hook affected) |
| Added nuance/balance | Maybe | LinkedIn, Facebook (professional context) |
| Typo fixes | No | No changes needed |
| Minor wording | No | No changes needed |

**Checklist After Each Version**:
- [ ] Read new version completely
- [ ] Identify changes that affect advertising
- [ ] Update relevant advertising files
- [ ] Verify character counts still within limits
- [ ] Document changes in TODO.md
- [ ] Mark "Advertising reviewed for v{N}" in TODO.md

**Pro Tip**: Even if you don't update the files, always REVIEW them after each version to ensure they still accurately represent the article.

---

## Phase 5: Version Control Best Practices

### 5.1 Never Modify Existing Versions

**Rule**: Once a version is created, it is immutable.

**Rationale**:
- Preserves revision history
- Allows comparison between versions
- Enables rollback if needed
- Documents evolution of content

### 5.2 Version Naming Convention

**Format**: `v{N}-{descriptive-name}.md`

**Examples**:
- `v1-intro-article.md`
- `v2-intro-article.md`
- `v3-intro-article.md`

**Not**:
- `intro-article-draft.md` (no version number)
- `intro-article-final.md` (ambiguous)
- `intro-article-2025-01-28.md` (date-based, not sequential)

### 5.3 Version Increment Triggers

**Create New Version When**:
- Adding new major section
- Expanding existing section significantly
- Replacing examples or content
- Addressing feedback requiring structural changes
- Adding nuance or balance to arguments

**Don't Create New Version For**:
- Typo fixes (fix in latest version)
- Minor wording changes (fix in latest version)
- Formatting adjustments (fix in latest version)
- Link updates (fix in latest version)

### 5.4 Track Changes in TODO

**Update TODO.md After Each Version**:
```markdown
## Version History
- **v1** (2025-01-28): Initial draft, core content complete
- **v2** (2025-01-28): Added programming language section
- **v3** (2025-01-28): Added carbon intensity by region, carbon-aware computing
- **v4** (2025-01-28): Replaced redundant algorithm example
- **v5** (2025-01-28): Added tradeoffs and NFR section
```

---

## Phase 6: Content Guidelines

### 6.1 Markdown Formatting for Medium

#### Checkbox Formatting

**Problem**: Markdown checkboxes `[ ]` and `[x]` don't translate properly to Medium's editor.

**Solution**: Use Unicode checkbox characters instead of markdown checkbox syntax.

**Character Reference**:
- Empty checkbox: `☐` (U+2610)
- Checked checkbox: `☑` (U+2611) or `✓` (U+2713)

**Example**:
```markdown
❌ WRONG (Markdown syntax - doesn't work on Medium):
- [ ] Item one
- [x] Item two

✅ CORRECT (Unicode characters - works on Medium):
- ☐ Item one
- ☑ Item two
```

**When to Use**:
- Checklists in articles
- Action items for readers
- Step-by-step processes
- Pre-flight checklists
- Implementation guides

**Implementation**:
Before publishing to Medium, search for `[ ]` and `[x]` in your article and replace with `☐` and `☑` respectively.

---

### 6.2 Tone and Voice

**Conversational but Authoritative**:
- Use "you" and "your" to address reader
- Use contractions (don't, isn't, you're)
- Use casual phrases ("Here's the thing...", "Anyway, back to...")
- Acknowledge complexity honestly ("Not perfect, but...")
- Use humor sparingly and naturally

**Avoid**:
- Overly formal language
- Marketing speak or hype
- Condescending tone
- Excessive exclamation points
- Buzzwords without explanation

### 6.2 Structure and Flow

**Opening**:
- Hook with surprising fact or relatable scenario
- Establish relevance quickly
- Set expectations for article

**Opening for Series Articles (MANDATORY)**:
When writing an article that is part of a series, ALWAYS start with a context-setting blurb that:
- Identifies the series name
- References the previous article's topic
- Introduces the current article's focus
- Invites readers to follow the series

**Series Opening Template**:
```markdown
Part {N} of my series on {Series Name}. Last time, we explored {previous topic} — {brief description}. This time: {current topic}. Follow along for more {series theme}.
```

**Example**:
```markdown
Part 3 of my series on Sustainable Software Engineering. Last time, we explored energy-efficient algorithm patterns — the specific code structures that reduce computational waste. This time: database optimization strategies that cut both energy costs and your cloud bill. Follow along for more deep dives into green coding practices.
```

**Benefits**:
- Provides context for new readers
- Creates continuity across series
- Encourages readers to explore previous articles
- Builds anticipation for future content
- Improves SEO through internal linking

**Body**:
- Use clear subheadings (H2, H3)
- Keep paragraphs short (2-4 sentences)
- Use concrete examples with real numbers
- Include code snippets where relevant
- Use bullet points for lists
- Add transitions between sections

**Closing**:
- Summarize key takeaways
- Provide actionable next steps
- Tease follow-up articles
- Include call to action (comment prompt)

**Closing for Series Articles (MANDATORY)**:
End every series article with a "Series Navigation" section to help readers navigate the series.

**Series Navigation Template**:
```markdown
---

## Series Navigation

**Previous Article**: [Title of Previous Article](link)

**Next Article**: [Title of Next Article](link) *(or "Coming soon!" if not yet published)*

**Coming Up**: Topic 1, Topic 2, Topic 3, Topic 4
```

**Example**:
```markdown
---

## Series Navigation

**Previous Article**: [Energy-Efficient Algorithm Patterns](https://medium.com/...)

**Next Article**: [Building Carbon-Aware Applications](https://medium.com/...) *(Coming soon!)*

**Coming Up**: Microservices architecture, DevOps practices, AI/ML sustainability, language efficiency
```

**Guidelines**:
- Place after main content, before author bio
- Use horizontal rule (---) to separate from main content
- Link to previous article (if exists)
- Link to next article (if published) or note "Coming soon!"
- List 3-5 upcoming topics after the next article
- Keep topic names concise but descriptive
- Update previous articles when new ones are published

**Benefits**:
- Improves series discoverability
- Encourages binge-reading behavior
- Builds anticipation for upcoming content
- Creates internal linking structure for SEO
- Helps readers plan their learning journey

### 6.3 Examples and Evidence

**Use Concrete Examples**:
- Real numbers: "35x difference" not "significant difference"
- Specific scenarios: "API endpoint handling 10K req/sec" not "high-traffic service"
- Named technologies: "HashMap vs List" not "efficient data structures"
- Actual regions: "Norway vs India" not "clean vs dirty grids"

**Provide Evidence**:
- Link to studies and research
- Reference industry standards
- Cite cloud provider data
- Include tool names and URLs

### 6.4 Technical Depth

**Balance Accessibility and Authority**:
- Explain technical concepts simply
- Use analogies where helpful
- Provide enough detail to be credible
- Don't oversimplify to the point of inaccuracy
- Assume reader has basic technical knowledge

**From Green Coding Example**:
- Explained O(n) vs O(1) without formal CS notation
- Used HashMap vs List (familiar to most developers)
- Provided carbon intensity numbers with context
- Explained JIT compilation without deep dive

---

## Phase 7: Pre-Publication Checklist

### 7.1 Content Review

- [ ] All major points from proposal covered
- [ ] Examples are concrete and specific
- [ ] Numbers and statistics are accurate
- [ ] Links and resources are valid
- [ ] Code examples are correct
- [ ] No redundant content
- [ ] Smooth transitions between sections
- [ ] Consistent tone throughout

### 7.2 Technical Accuracy

- [ ] Statistics verified with sources
- [ ] Tool names and URLs correct
- [ ] Technical concepts explained accurately
- [ ] No outdated information
- [ ] Regional data is current
- [ ] Standards and specifications cited correctly

### 7.3 Readability

- [ ] Target reading time achieved (5-7 min typical)
- [ ] Paragraphs are short and scannable
- [ ] Subheadings are clear and descriptive
- [ ] No walls of text
- [ ] Bullet points used appropriately
- [ ] Code blocks formatted correctly

### 7.4 SEO and Discoverability

**CRITICAL**: SEO optimization is mandatory for all articles to maximize reach and discoverability.

#### Title Optimization (MANDATORY)

**Rules**:
- **Length**: 60-70 characters (optimal for search results)
- **Keywords**: Include primary keyword near the beginning
- **Clarity**: Make it clear what the article is about
- **Intrigue**: Create curiosity without clickbait
- **Numbers**: Use numbers when relevant (e.g., "5 Ways to...", "2024 Guide")

**Title Formulas That Work**:
- "How to {Achieve Outcome} with {Method}"
- "{Number} Ways to {Solve Problem}"
- "Why {Topic} Matters (And How to {Action})"
- "The Complete Guide to {Topic}"
- "{Topic}: What You Need to Know in {Year}"

**Examples**:
- ✅ "Why Your Code's Carbon Footprint Matters (And How to Measure It)"
- ✅ "5 Database Optimization Patterns That Cut Energy Costs"
- ✅ "Building Carbon-Aware Applications: A Developer's Guide"
- ❌ "Some thoughts on coding" (too vague, no keywords)
- ❌ "You won't believe this one weird trick..." (clickbait)

#### Subtitle/Description Optimization

**Rules**:
- **Length**: 140-160 characters
- **Hook-driven**: The subtitle should make readers feel something or spark curiosity — not just describe the article
- **Punchy over descriptive**: Lead with a surprising stat, a bold claim, or a tension that demands resolution
- **Expand on title**: Provide additional context, but with personality
- **Include secondary keywords**: Naturally incorporate related terms
- **Call to action**: Hint at what readers will learn

**Good Example** (hook-driven):
```markdown
Title: Programming Language Efficiency Deep Dive
Subtitle: C is 75x more energy-efficient than Python. Your Rust evangelist won't shut up about it. Here's what the benchmarks actually mean for your codebase.
```

**Bad Example** (dry, descriptive):
```markdown
Title: Why Your Code's Carbon Footprint Matters (And How to Measure It)
Subtitle: A practical guide to measuring and reducing the environmental impact of your software, with tools and techniques you can use today.
```

#### Keyword Strategy (MANDATORY)

**Primary Keyword**:
- Choose ONE main keyword phrase (2-4 words)
- Use in: Title, first paragraph, at least 2 subheadings, conclusion
- Density: 1-2% of total word count (natural, not forced)

**Secondary Keywords**:
- Choose 3-5 related keyword phrases
- Use throughout article naturally
- Include in subheadings where relevant

**Long-Tail Keywords**:
- Target specific, longer phrases (4-6 words)
- Lower competition, higher conversion
- Use in subheadings and body text

**Keyword Research Tools**:
- Google Trends (trending topics)
- AnswerThePublic (question-based keywords)
- Medium search suggestions (what readers search for)
- Google Search Console (if you have access)
- Competitor article analysis

**Example Keyword Strategy**:
```markdown
Primary: "green coding"
Secondary: "sustainable software", "carbon footprint", "energy efficiency", "environmental impact"
Long-tail: "how to measure code carbon footprint", "reduce software energy consumption"
```

#### Subheading Optimization (MANDATORY)

**Rules**:
- **Include keywords**: Use primary/secondary keywords in H2/H3 headings
- **Question format**: Use questions readers might search for
- **Descriptive**: Make it clear what the section covers
- **Scannable**: Readers should understand article structure from headings alone

**Examples**:
- ✅ "What is Green Coding?" (question + primary keyword)
- ✅ "How to Measure Your Code's Carbon Footprint" (question + long-tail keyword)
- ✅ "5 Quick Wins for Energy-Efficient Code" (number + secondary keyword)
- ❌ "Introduction" (too generic, no keywords)
- ❌ "Some thoughts" (vague, no keywords)

#### First Paragraph Optimization (MANDATORY)

**Rules**:
- **Hook immediately**: First sentence must grab attention
- **Include primary keyword**: Use within first 100 words
- **Set expectations**: Tell readers what they'll learn
- **Keep it short**: 3-4 sentences maximum

**Example**:
```markdown
Your code has a carbon footprint. Every API call, database query, and algorithm you write consumes electricity — and that electricity often comes from fossil fuels. Here's the thing: most developers have no idea how much energy their code uses, or how to measure it. This guide will show you exactly how to measure your code's environmental impact and what to do about it.
```
*(Primary keyword "carbon footprint" in first sentence, sets clear expectations)*

#### Internal Linking Strategy (MANDATORY)

**Rules**:
- **Link to related articles**: 3-5 internal links per article
- **Anchor text**: Use descriptive, keyword-rich anchor text
- **Contextual**: Links should be relevant to surrounding content
- **Series navigation**: Always link to previous/next articles in series
- **Update old articles**: Add links to new articles in older content

**Example**:
```markdown
We covered [energy-efficient algorithm patterns](link) in the previous article, 
but database optimization is where you'll see the biggest impact.
```

#### External Linking Strategy

**Rules**:
- **Authority sources**: Link to reputable sources (research, documentation, standards)
- **3-5 external links**: Provides credibility and context
- **Open in new tab**: Use target="_blank" (Medium does this automatically)
- **Anchor text**: Use descriptive text, not "click here"

**Example**:
```markdown
According to the [Green Software Foundation](https://greensoftware.foundation/), 
software is responsible for approximately 2-3% of global carbon emissions.
```

#### Image Optimization

**Rules**:
- **Alt text**: Always include descriptive alt text with keywords
- **File names**: Use descriptive, keyword-rich file names
- **Cover image**: Eye-catching, relevant to topic
- **In-article images**: Break up text, illustrate concepts
- **Diagrams**: Use for complex concepts (improves engagement)

**Example**:
```markdown
Alt text: "Comparison chart showing energy consumption of different algorithms"
File name: "algorithm-energy-comparison-chart.png"
```

#### Tag Strategy (MANDATORY)

**Rules**:
- **Use all 5 tags**: Medium allows 5 tags, use them all
- **Primary tag first**: Most relevant tag goes first
- **Mix broad and specific**: Combine popular and niche tags
- **Check tag popularity**: Use tags with existing followers
- **Consistent tagging**: Use same tags across series

**Tag Selection Priority**:
1. **Primary topic tag**: Main subject (e.g., "Software Development")
2. **Specific niche tag**: Narrow focus (e.g., "Green Tech")
3. **Audience tag**: Who it's for (e.g., "Software Engineering")
4. **Related topic tag**: Adjacent topic (e.g., "Sustainability")
5. **Trending tag**: Current interest (e.g., "Climate Change")

**Example Tag Set**:
```markdown
1. Software Development (broad, popular)
2. Green Tech (specific niche)
3. Software Engineering (audience)
4. Sustainability (related topic)
5. DevOps (related technical area)
```

**Tag Research**:
- Search Medium for your topic
- Check tags on popular articles in your niche
- Look at tag follower counts
- Use tags with 10K+ followers when possible

#### URL Optimization

**Rules**:
- **Custom URL slug**: Edit Medium's auto-generated URL
- **Include primary keyword**: Use main keyword in URL
- **Keep it short**: 3-5 words maximum
- **Use hyphens**: Separate words with hyphens
- **Remove stop words**: Remove "a", "the", "and", etc.

**Example**:
```markdown
Auto-generated: medium.com/@user/why-your-codes-carbon-footprint-matters-and-how-to-measure-it-a1b2c3d4e5f6
Optimized: medium.com/@user/measure-code-carbon-footprint
```

#### Meta Description (If Applicable)

**Rules**:
- **Length**: 150-160 characters
- **Include primary keyword**: Use naturally
- **Call to action**: Encourage clicks
- **Unique**: Don't duplicate title

**Example**:
```markdown
Learn how to measure and reduce your code's carbon footprint with practical tools and techniques. Start building more sustainable software today.
```

#### Content Structure for SEO

**Rules**:
- **Word count**: 1,500-2,500 words (optimal for SEO)
- **Paragraph length**: 2-4 sentences (improves readability score)
- **Bullet points**: Use for lists (improves scannability)
- **Bold/italic**: Emphasize key points (helps readers scan)
- **Code blocks**: Format code properly (improves user experience)

#### Engagement Signals (Ranking Factors)

**Medium's Algorithm Considers**:
- **Read time**: Longer read times = higher ranking
- **Read ratio**: % of article read (aim for 50%+)
- **Claps**: More claps = higher visibility
- **Responses**: Comments indicate engagement
- **Shares**: External shares boost ranking
- **Highlights**: Reader highlights show value

**Optimization Strategies**:
- **Hook early**: Grab attention in first 30 seconds
- **Use subheadings**: Make content scannable
- **Add visuals**: Break up text, increase engagement
- **End with CTA**: Encourage comments/claps
- **Ask questions**: Prompt reader interaction

#### Publication Strategy

**Rules**:
- **Submit to publications**: Higher reach than personal blog
- **Choose relevant publications**: Match your topic
- **Follow publication guidelines**: Each has specific requirements
- **Build relationships**: Engage with publication editors

**Top Tech Publications on Medium**:
- Better Programming
- The Startup
- Level Up Coding
- JavaScript in Plain English
- Towards Data Science (for data-heavy topics)

#### Timing and Frequency

**Optimal Publishing Times**:
- **Best days**: Tuesday, Wednesday, Thursday
- **Best times**: 8-10 AM or 6-8 PM (reader's timezone)
- **Avoid**: Monday mornings, Friday afternoons, weekends
- **Consistency**: Publish on same day/time each week

**Series Publishing Strategy**:
- **Weekly cadence**: One article per week
- **Build momentum**: Publish consistently for 4-6 weeks
- **Cross-promote**: Link new articles in old ones
- **Email list**: Notify subscribers of new articles

#### SEO Checklist (MANDATORY)

Before publishing, verify:

- [ ] Title includes primary keyword (60-70 characters)
- [ ] Subtitle includes secondary keywords (140-160 characters)
- [ ] Primary keyword in first paragraph
- [ ] Primary keyword in at least 2 subheadings
- [ ] 3-5 internal links with keyword-rich anchor text
- [ ] 3-5 external links to authority sources
- [ ] All 5 tags used (primary tag first)
- [ ] Custom URL slug with primary keyword
- [ ] Alt text on all images
- [ ] Subheadings are descriptive and keyword-rich
- [ ] Word count 1,500-2,500 words
- [ ] Series navigation section (if part of series)
- [ ] Call to action at end
- [ ] Proofread for grammar/spelling (affects credibility)

#### SEO Monitoring (Post-Publication)

**Track These Metrics**:
- **Views**: Total article views
- **Reads**: Complete reads (read ratio)
- **Read time**: Average time spent reading
- **Claps**: Total claps received
- **Responses**: Comments and replies
- **Fans**: New followers from article
- **Referrers**: Where traffic comes from
- **Search terms**: What people searched to find article (if available)

**Optimization Actions**:
- If low views: Improve title, tags, or promotion
- If low read ratio: Improve hook, structure, or formatting
- If low engagement: Add more CTAs, questions, or interactive elements
- If high bounce: Check if content matches title/expectations

#### Advanced SEO Techniques

**Semantic SEO**:
- Use related terms and synonyms naturally
- Cover topic comprehensively (answer related questions)
- Use LSI (Latent Semantic Indexing) keywords

**Featured Snippets**:
- Answer questions directly and concisely
- Use numbered lists for "how to" content
- Use bullet points for "what is" content
- Format for easy extraction by search engines

**Schema Markup** (Limited on Medium):
- Medium handles most schema automatically
- Focus on content structure and formatting
- Use proper heading hierarchy (H1 → H2 → H3)

**Social Signals**:
- Share on LinkedIn, Twitter, Reddit
- Encourage team members to share
- Engage with comments quickly
- Cross-post to Dev.to, Hashnode (with canonical link)

---

**SEO Resources**:
- [Google Search Central](https://developers.google.com/search)
- [Moz Beginner's Guide to SEO](https://moz.com/beginners-guide-to-seo)
- [Medium's Distribution System](https://help.medium.com/hc/en-us/articles/360006362473)
- [Ahrefs Blog](https://ahrefs.com/blog/) (keyword research)

---

### 7.5 Supporting Materials

- [ ] Cover image created or selected
- [ ] Code examples tested
- [ ] Visuals/diagrams created (if needed)
- [ ] Social media snippets prepared
- [ ] Author bio updated

---

## Phase 8: Publication and Promotion

### 8.1 Final Version Selection

**Action**: Copy approved version to parent directory as final article.

**Example**:
```bash
# Copy v5 as final version
cp versions/v5-intro-article.md intro-article-FINAL.md
```

### 8.2 Medium Publication

**Steps**:
1. Create new story in Medium
2. Paste markdown content
3. Format code blocks and quotes
4. Add cover image
5. Add tags (5-7 tags)
6. Set publication (if applicable)
7. Preview on mobile and desktop
8. Publish or schedule

**Recommended Tags** (Green Coding Example):
- Software Development
- Sustainability
- Green Tech
- Software Engineering
- Climate Change
- DevOps
- Cloud Computing

### 8.3 Promotion (Use Pre-Created Advertising Infrastructure)

**CRITICAL**: Use the social media posts created in Phase 1.5 (`advertising/` directory)

**Process**:
1. Review and customize each platform's post with article-specific content
2. Replace placeholders with actual article URL
3. Add article-specific examples and numbers
4. Verify hashtags are relevant and current
5. Post according to schedule in MEDIUM-ARTICLE-RELEASE-SCHEDULE.md

**Posting Order** (Day of Publication):

**Morning (9:00-10:00 AM EST)**:
1. Publish article on Medium
2. Get article URL
3. Update all advertising files with actual URL
4. Post to LinkedIn (use `advertising/linkedin-post.md`)
5. Post to X/Twitter (use `advertising/x-post.md` - main post)
6. Monitor initial engagement (first 2 hours critical)

**Afternoon (12:00-1:00 PM EST)**:
7. Post to Instagram (use `advertising/instagram-post.md`)
8. Post to Facebook (use `advertising/facebook-post.md`)
9. Post to Threads (use `advertising/threads-post.md`)
10. Share in relevant LinkedIn groups

**Evening (5:00-6:00 PM EST)**:
11. Post to Reddit (use `advertising/reddit-post.md`)
12. Post X/Twitter thread if desired (use thread version)
13. Final engagement check
14. Respond to all comments

**Channels** (Reference Files):
- LinkedIn → `advertising/linkedin-post.md`
- X/Twitter → `advertising/x-post.md`
- Instagram → `advertising/instagram-post.md`
- Facebook → `advertising/facebook-post.md`
- Threads → `advertising/threads-post.md`
- Reddit → `advertising/reddit-post.md`
- Hashtags → `advertising/hashtag-strategy.md`

**Timing Best Practices**:
- Publish Tuesday-Thursday for best engagement
- Morning (8-10 AM) in target timezone
- Avoid Mondays and Fridays
- Avoid holidays

**Cross-Platform Strategy**:
- LinkedIn: Professional, detailed, no hashtags
- X: Concise, thread optional, 5 hashtags
- Instagram: Visual, link in bio, 30 hashtags
- Facebook: Detailed, direct link, 20-30 hashtags
- Threads: Conversational, 15-20 hashtags
- Reddit: Authentic, no hashtags, discussion-focused

---

## Phase 9: Post-Publication

### 9.1 Engagement

**Monitor and Respond**:
- Reply to comments within 24 hours
- Engage with thoughtful questions
- Acknowledge corrections or additions
- Thank readers for sharing

### 9.2 Metrics Tracking

**Track**:
- Views (first 7 days, first 30 days)
- Read ratio (views vs reads)
- Claps/reactions
- Comments
- Shares
- Referral sources
- Time on page

**From Green Coding Example**:
- Target: 15K-40K views (first 30 days)
- Target: 500+ claps
- Target: 100+ comments
- Target: 5-10% read-through rate

### 9.3 Iterate Based on Feedback

**Action**: Note common questions or confusion in comments.

**Use For**:
- Follow-up articles
- Clarifications in future versions
- FAQ section
- Course content development

---

## Phase 10: Series Management

### 10.1 Plan Article Series

**From Green Coding Example**:
1. Why Your Code's Carbon Footprint Matters (intro) ✓
2. Energy-Efficient Algorithm Patterns
3. Building Carbon-Aware Applications
4. Sustainable Microservices Architecture
5. Green DevOps Practices
6. Programming Language Efficiency Deep Dive
7. Carbon-Aware Workload Placement Strategies
8. ISO/IEC 21031 (SCI Standard) Deep Dive

### 10.2 Cross-Link Articles

**Action**: Update older articles with links to newer ones.

**Example**:
```markdown
**Update (Feb 2025)**: Check out the follow-up article on 
[Energy-Efficient Algorithm Patterns](#) for deeper technical details.
```

### 10.3 Create Series Landing Page

**Action**: Create index article linking to all articles in series.

**Location**: `for-approval/medium/{topic}/series-index.md`

---

## Appendix A: Backfilling Advertising Infrastructure for Existing Articles

### A.1 Overview

**Purpose**: Add advertising infrastructure to articles published before this process was established
**Priority**: High - ensures consistent promotion across all articles
**Timeline**: Complete within 2 weeks of process adoption

### A.2 Backfill Checklist

For each existing article without `advertising/` directory:

- [ ] Create `advertising/` directory in article folder
- [ ] Create `linkedin-post.md` (use published post or create new)
- [ ] Create `x-post.md` (use published post or create new)
- [ ] Create `instagram-post.md` (create from scratch)
- [ ] Create `facebook-post.md` (create from scratch)
- [ ] Create `threads-post.md` (create from scratch)
- [ ] Create `reddit-post.md` (create from scratch)
- [ ] Create `hashtag-strategy.md` (research current best hashtags)
- [ ] Update TODO.md to mark advertising infrastructure complete

### A.3 Backfill Process

**Step 1: Identify Articles Needing Backfill**

```bash
# List all article directories
ls -R for-approval/medium/

# Check which ones are missing advertising/ directory
```

**Articles to Backfill** (as of 2026-02-18):
- Green Coding 1: intro (✓ already has advertising/)
- Green Coding 2: ee-algo-patterns
- Green Coding 3: eff-database
- Green Coding 4: carbon-aware-apps
- Green Coding 5: sustainable-microservices
- Communication 1: speaking-executive
- Communication 2: stakeholder-dynamics
- Resilience 1: cell-based-architecture
- Resilience 2: chaos-engineering

**Step 2: Create Directory Structure**

For each article:
```bash
mkdir -p "for-approval/medium/{series}/{article}/advertising"
```

**Step 3: Create Social Media Posts**

**Option A: Use Existing Published Posts**
- If you already posted to LinkedIn/X, copy that content
- Preserve what worked well
- Add missing platforms (Instagram, Facebook, Threads, Reddit)

**Option B: Create From Scratch**
- Use templates from Phase 1.5
- Extract key points from article
- Create platform-specific versions
- Research current best hashtags

**Step 4: Populate Files**

For each platform, create file with:
1. Article-specific hook and content
2. Actual Medium article URL
3. Platform-appropriate hashtags
4. Character count verification

**Step 5: Verify Completeness**

- [ ] All 7 files created (6 platform posts + hashtag strategy)
- [ ] All files follow template structure
- [ ] All URLs are correct and working
- [ ] All hashtags are current and relevant
- [ ] Character counts within platform limits

### A.4 Backfill Priority Order

**Priority 1: Most Recent Articles** (published in last 30 days)
- Green Coding 5: sustainable-microservices
- Communication 2: stakeholder-dynamics
- Resilience 2: chaos-engineering

**Priority 2: High-Performing Articles** (most views/engagement)
- Check Medium analytics
- Backfill top 3 performers first

**Priority 3: Series Starters** (first article in each series)
- Green Coding 1: intro (✓ already done)
- Communication 1: speaking-executive
- Resilience 1: cell-based-architecture

**Priority 4: Remaining Articles**
- Complete in chronological order

### A.5 Backfill Timeline

**Week 1**:
- Day 1-2: Priority 1 articles (3 articles)
- Day 3-4: Priority 2 articles (3 articles)
- Day 5: Priority 3 articles (2 remaining)

**Week 2**:
- Day 1-5: Remaining articles (1-2 per day)

### A.6 Re-Promotion Strategy

After backfilling advertising infrastructure:

**Option A: Immediate Re-Promotion**
- Post to platforms not used originally
- Example: If only posted to LinkedIn originally, now post to Instagram, Threads, Reddit

**Option B: Scheduled Re-Promotion**
- Add to content calendar for re-sharing
- "In case you missed it" posts
- Share 30-60 days after original publication

**Option C: Series Compilation**
- Create "Series Index" post linking all articles
- Use backfilled posts as reference for compilation post

### A.7 Backfill Verification

After completing backfill:

```bash
# Verify all articles have advertising/ directory
find for-approval/medium -type d -name "advertising"

# Should return one directory per article
```

**Final Checklist**:
- [ ] All existing articles have `advertising/` directory
- [ ] All directories contain 7 files (6 posts + hashtag strategy)
- [ ] All files follow current template structure
- [ ] All URLs are correct and working
- [ ] Process documented in each article's TODO.md

---

## Appendix B: Advertising Infrastructure Templates

### Writing Tools
- **Markdown Editor**: VS Code, Typora, or Medium's editor
- **Grammar Check**: Grammarly (optional)
- **Readability**: Hemingway Editor (optional)
- **Word Count**: Built into most editors

### Research Tools
- **Academic Papers**: Google Scholar, arXiv
- **Industry Data**: Cloud provider documentation
- **Standards**: ISO, Green Software Foundation
- **Statistics**: Statista, industry reports

### Version Control
- **Git**: For tracking all versions
- **Folder Structure**: As defined in Phase 1
- **Naming Convention**: As defined in Phase 5

---

## Common Pitfalls to Avoid

### Content Pitfalls
- ❌ Being too preachy or judgmental
- ❌ Using vague examples ("some companies", "many developers")
- ❌ Oversimplifying complex topics
- ❌ Making claims without evidence
- ❌ Redundant content across sections
- ❌ Walls of text without breaks

### Process Pitfalls
- ❌ Modifying existing versions instead of creating new ones
- ❌ Skipping the TODO list
- ❌ Not tracking version changes
- ❌ Writing without reviewing tone samples
- ❌ Publishing without technical review
- ❌ Forgetting to update "Coming Up" section

### Tone Pitfalls
- ❌ Too formal or academic
- ❌ Too casual or unprofessional
- ❌ Inconsistent voice throughout article
- ❌ Condescending to readers
- ❌ Overly enthusiastic or salesy

---

## Success Criteria

### Content Quality
- ✅ Conversational but authoritative tone
- ✅ Concrete examples with real numbers
- ✅ Technical accuracy verified
- ✅ Smooth flow and transitions
- ✅ Actionable takeaways
- ✅ Proper citations and links

### Process Quality
- ✅ All versions preserved
- ✅ TODO list maintained
- ✅ Changes documented
- ✅ Feedback incorporated
- ✅ Pre-publication checklist completed

### Engagement Quality
- ✅ Target reading time achieved
- ✅ High read-through rate
- ✅ Positive comments
- ✅ Shares and claps
- ✅ Follow-up article interest

---

## Appendix: Green Coding Article Timeline

**Example of Full Process**:

1. **Initial Setup** (5 min)
   - Created directory structure
   - Reviewed writing samples

2. **Proposal** (30 min)
   - Created initial proposal
   - Defined talking points
   - Got feedback (skipped in this case)

3. **v1 - Initial Draft** (60 min)
   - Wrote complete first draft
   - 1,600 words, core content
   - Created TODO list

4. **v2 - Language Section** (45 min)
   - Added programming language efficiency
   - 2,000 words
   - Updated TODO

5. **v3 - Carbon Intensity** (45 min)
   - Added region-based carbon intensity
   - Added carbon-aware computing
   - 2,200 words

6. **v4 - Deduplication** (20 min)
   - Replaced redundant example
   - Improved clarity

7. **v5 - Tradeoffs** (60 min)
   - Added NFR balancing section
   - Added SDLC integration
   - 2,600 words

**Total Time**: ~4.5 hours for complete article with 5 iterations

---

**Status**: Active Process  
**Owner**: Content Team  
**Next Review**: After 5 articles using this process


---

## Quick Reference: Advertising Infrastructure

### Required Files Per Article

```
{article-name}/
└── advertising/                (created after v1 complete)
    ├── linkedin-post.md      (max ~2,000 chars body, no hashtags, reserve ~1,000 for URL)
    ├── x-post.md             (280 chars + thread, 5 hashtags)
    ├── instagram-post.md     (2,200 chars, 30 hashtags)
    ├── facebook-post.md      (1,000-2,000 chars, 20-30 hashtags)
    ├── threads-post.md       (500 chars, 15-20 hashtags)
    ├── reddit-post.md        (no hashtags, subreddit list)
    ├── teams-post.md         (internal, images/formatting OK, no hashtags)
    └── hashtag-strategy.md   (platform-specific tags)
```

### When to Create/Update

- **Initial Creation**: Phase 3.3 (after v1 complete)
- **Review/Update**: Phase 4.6 (after each major revision - v2, v3, v4, etc.)
- **Existing Articles**: Backfill within 2 weeks (see Appendix A)

### Update Decision Matrix

| Change Type | Update Advertising? | Which Files? |
|-------------|---------------------|--------------|
| New major section | Yes | All platform posts |
| Expanded existing section | Maybe | LinkedIn, Facebook (detailed posts) |
| Better example/number | Yes | All posts (better hook) |
| Removed redundancy | No | Keep existing (unless hook affected) |
| Added nuance/balance | Maybe | LinkedIn, Facebook (professional context) |
| Typo fixes | No | No changes needed |
| Minor wording | No | No changes needed |

### Posting Schedule (Day of Publication)

| Time | Platform | File Reference |
|------|----------|----------------|
| 9:00 AM | Medium | Publish article |
| 9:15 AM | LinkedIn | `advertising/linkedin-post.md` |
| 9:30 AM | X/Twitter | `advertising/x-post.md` (main) |
| 10:00 AM | Teams | `advertising/teams-post.md` |
| 12:00 PM | Instagram | `advertising/instagram-post.md` |
| 12:15 PM | Facebook | `advertising/facebook-post.md` |
| 12:30 PM | Threads | `advertising/threads-post.md` |
| 5:00 PM | Reddit | `advertising/reddit-post.md` |
| 5:30 PM | X/Twitter | `advertising/x-post.md` (thread) |

### Platform Limits

| Platform | Character Limit | Hashtag Limit | Notes |
|----------|----------------|---------------|-------|
| LinkedIn | 3,000 | 0 | Professional tone, no hashtags, reserve ~1,000 chars for article URL |
| X/Twitter | 280 | 5-10 | Concise, thread optional |
| Instagram | 2,200 | 30 | Visual, link in bio |
| Facebook | No limit | 20-30 | Detailed, direct link |
| Threads | 500 | 15-20 | Conversational |
| Reddit | No limit | 0 | No hashtags, authentic |
| Teams | No limit | 0 | Internal (Jabil Dev Network — Architecture Community), 30-60s read, featured image, catchy subject line |

### LinkedIn Formatting Guidelines (MANDATORY)

**CRITICAL**: LinkedIn has very limited formatting options. Follow these rules strictly.

**Bullet Points**:
- ❌ DON'T use markdown bullets (-, *, •) - they don't render properly
- ✅ DO use emoji bullets for visual hierarchy

**Recommended Emoji Bullets**:
- 🔹 Small blue diamond (general points)
- 🔸 Small orange diamond (alternative points)
- ✅ Check mark (completed items, benefits)
- ❌ Cross mark (problems, what not to do)
- 💡 Light bulb (insights, tips)
- 🎯 Target (goals, objectives)
- 📊 Chart (metrics, data points)
- ⚡ Lightning (performance, speed)
- 🔴 Red circle (errors, critical issues)
- 🟢 Green circle (success, healthy status)
- 🟡 Yellow circle (warnings)
- ➤ Arrow (action items)

**Formatting Rules**:
1. **No markdown**: Bold, italic, code blocks don't work
2. **Use CAPS for emphasis**: "CRITICAL", "IMPORTANT", "KEY POINT"
3. **Use emoji bullets**: Replace all `- ` with emoji bullets
4. **Line breaks**: Use double line breaks for paragraph separation
5. **Visual separators**: Use `━━━━━━━━━━` or `---` for section breaks
6. **Numbers**: Use actual numbers (1️⃣ 2️⃣ 3️⃣) or plain text (1. 2. 3.)

**Example - BAD (Markdown)**:
```
Key points:
- First point
- Second point
- Third point

**Important**: This is critical
```

**Example - GOOD (LinkedIn Format)**:
```
Key points:

🔹 First point
🔹 Second point
🔹 Third point

IMPORTANT: This is critical
```

**Section Structure**:
```
Hook paragraph (2-3 sentences)

[Double line break]

SECTION TITLE IN CAPS

🔹 Point one with details
🔹 Point two with details
🔹 Point three with details

[Double line break]

━━━━━━━━━━━━━━━━

[Double line break]

NEXT SECTION TITLE

Content continues...
```

**Hashtag Placement**:
- Place all 30 hashtags at the END of the post
- Separate from main content with line break
- LinkedIn rewards using all 30 hashtags

### Backfill Priority

1. **Most Recent** (last 30 days)
2. **High-Performing** (most views)
3. **Series Starters** (first in series)
4. **Remaining** (chronological)

---

**Document Version**: 2.2
**Last Updated**: 2026-02-20
**Major Changes**: 
- v2.0: Added mandatory advertising infrastructure
- v2.1: Moved advertising creation to Phase 3.3 (after v1), added Phase 4.6 (review/update after each version)
- v2.2: Added LinkedIn formatting guidelines with emoji bullet points (mandatory)
