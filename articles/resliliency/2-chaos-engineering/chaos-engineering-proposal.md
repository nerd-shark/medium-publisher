---
document-title: Resilience Engineering Series
document-subtitle: Chaos Engineering in Production - Proposal
document-type: Article Proposal
document-date: 2025-02-08
document-revision: 1.0
document-author: Daniel Stauffer
author-email: daniel_stauffer@jabil.com
author-org: Enterprise Architecture
review-cycle: Per Article
---

# Resilience Part 2: Chaos Engineering in Production - Proposal

**Article Title**: "Chaos Engineering in Production: Breaking Things on Purpose (So They Don't Break by Accident)"

**Target Reading Time**: 7-9 minutes

**Target Audience**: SREs, platform engineers, engineering managers, DevOps teams

**Series Context**: Part 2 of Resilience Engineering series
- Part 1: Cell-Based Architecture & Circuit Breakers (published)
- **Part 2: Chaos Engineering in Production** ← THIS ARTICLE
- Part 3: The $10M Blind Spot (observability)
- Part 4: When Everything Fails (graceful degradation)
- Part 5: The Day AWS Went Down (multi-region)

## Article Objective

Teach readers how to build and run a chaos engineering program that validates resilience patterns and uncovers hidden failure modes before they cause production incidents.

## Major Talking Points

### 1. Hook: The Netflix Origin Story
- Chaos Monkey and the birth of chaos engineering
- The migration from data center to AWS
- "We don't know if our systems are resilient until we test them in production"
- The surprising result: Systems got MORE reliable

### 2. Why Staging Tests Don't Prove Production Resilience
- Staging environments are too clean
- Production has emergent behaviors staging can't replicate
- Real traffic patterns, real data volumes, real failure modes
- The "works in staging, breaks in prod" problem

### 3. Chaos Engineering Principles
- Build a hypothesis (what SHOULD happen when X fails?)
- Define blast radius (start small, expand gradually)
- Run experiments in production (with safety controls)
- Measure and learn (did the system behave as expected?)

### 4. Failure Injection Techniques
- Network failures (latency, packet loss, partitions)
- Service failures (kill processes, exhaust resources)
- Infrastructure failures (terminate instances, fill disks)
- Dependency failures (simulate third-party outages)
- Real examples with code snippets

### 5. Blast Radius Control
- Canary experiments (1% of traffic first)
- Time-boxing (automatic rollback after N minutes)
- Kill switches (abort button for experiments)
- Monitoring during experiments
- When to stop an experiment immediately

### 6. Tools and Platforms
- AWS Fault Injection Simulator (FIS)
- Gremlin (commercial chaos platform)
- Chaos Toolkit (open source)
- LitmusChaos (Kubernetes-native)
- Custom chaos tools
- Tool comparison matrix

### 7. Game Days and Fire Drills
- Scheduled chaos events
- Cross-team participation
- Simulating major outages
- Post-game retrospectives
- Building muscle memory for incidents

### 8. Building Organizational Buy-In
- Overcoming "don't break production" fear
- Starting with non-critical systems
- Demonstrating value through prevented incidents
- Executive communication strategies
- Celebrating chaos engineering wins

### 9. Measuring Resilience Improvements
- MTTR (Mean Time To Recovery)
- Blast radius reduction
- Incident frequency trends
- Customer impact metrics
- Before/after chaos engineering data

### 10. Real-World Chaos Experiments
- Killing database primaries
- Simulating AWS region failures
- Exhausting connection pools
- Injecting latency into critical paths
- Actual results and lessons learned

### 11. Validating Circuit Breakers from Part 1
- Testing circuit breaker state transitions
- Verifying fallback chains work
- Discovering hidden dependencies
- Improving resilience patterns based on chaos results

### 12. Tradeoffs and Honest Limitations
- Risk of causing real incidents
- Complexity of chaos infrastructure
- Time investment required
- When chaos engineering isn't appropriate

### 13. What's Next
- Teaser for Part 3: Observability (monitoring chaos experiments)
- How chaos engineering feeds into observability strategy

## Supporting Elements

### Code Examples
- AWS FIS experiment template
- Chaos Toolkit experiment definition
- Custom chaos script (Python)
- Kubernetes pod deletion experiment

### Diagrams
- Chaos engineering workflow (hypothesis → experiment → measure → learn)
- Blast radius expansion strategy
- Game day timeline

### Real Numbers
- Netflix: 99.99% availability with chaos engineering
- MTTR improvements (before/after chaos)
- Incident reduction percentages
- Actual chaos experiment results

## SEO Keywords

Primary: chaos engineering, production testing, resilience testing, fault injection, Netflix Chaos Monkey

Secondary: SRE practices, system reliability, failure testing, AWS FIS, Kubernetes chaos

## Success Metrics

- Reader understands chaos engineering principles
- Reader can design and run basic chaos experiments
- Reader knows how to control blast radius
- Reader can build organizational buy-in for chaos
- Reader measures resilience improvements

## Follow-Up Article Teasers

- Part 3: The $10M Blind Spot (observability for chaos experiments)
- Part 4: When Everything Fails (graceful degradation patterns)

---

**Status**: Proposal | **Created**: 2025-02-08 | **Series**: Resilience Part 2
