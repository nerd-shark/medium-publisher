# Modern Software Architecture Tradecraft
## How Senior Architects Actually Make Decisions

Architecture content is drowning in pattern catalogs and reference diagrams. What's missing is the messy reality of how experienced architects actually make decisions — under budget constraints, organizational politics, incomplete information, and deadlines that don't care about your design review schedule.

This series focuses on **decision-making under constraint**, not pattern memorization. Every article starts with a real architectural tension and works through how to resolve it with tradeoffs acknowledged, not hidden.

The audience for this series includes:
- Senior software engineers moving into architecture roles
- Software architects and principal engineers
- Engineering managers who participate in architectural decisions
- Tech leads responsible for system design in their domains

The series deliberately avoids "here's the pattern, here's the diagram" content. Instead, it asks: **when do you use it, when do you NOT use it, and what happens when you get it wrong?**

---

## Article 1 — Prologue
### The Architecture Decisions Nobody Writes Down

Most architectural knowledge lives in people's heads. When those people leave, the knowledge leaves with them. This article makes the case that architecture is a discipline of decision-making — and that the decisions matter more than the diagrams.

Topics include:
- Why architecture diagrams lie — they show structure, not the reasoning behind it
- The gap between "architecture as documentation" and "architecture as decision-making"
- Architectural Decision Records (ADRs) as the most underused tool in software engineering
- The three questions every architectural decision must answer: What did we decide? Why? What did we reject?
- How this series is structured and what it covers

This article establishes the core framing: **architecture isn't about knowing patterns — it's about making defensible decisions under uncertainty.**

---

## Article 2
### When NOT to Use Microservices

The most important architectural skill is knowing when a pattern doesn't apply. Microservices are the poster child — widely adopted, frequently regretted, and almost never evaluated honestly before adoption.

Key topics:
- The microservices adoption curve: why teams adopt them and when they regret it
- The distributed monolith: what happens when you get microservice boundaries wrong
- Operational cost reality: the infrastructure, observability, and coordination tax
- When a modular monolith is the better answer — and how to design one that doesn't become a big ball of mud
- Decision framework: team size, deployment independence, domain boundaries, and operational maturity as inputs
- Real examples of companies that migrated TO microservices and companies that migrated BACK

**The goal isn't to argue against microservices — it's to argue against adopting them by default.**

---

## Article 3
### Event-Driven vs. Workflow-Driven: Choosing Your Coordination Model

Two fundamentally different approaches to system coordination, and most teams pick one without understanding the tradeoffs. This article provides the decision framework.

Topics include:
- Event-driven architecture: choreography, eventual consistency, and the debugging nightmare
- Workflow-driven architecture: orchestration, explicit state machines, and the coupling tradeoff
- The hybrid reality: most production systems use both — the question is where to draw the line
- Saga patterns: choreography-based vs. orchestration-based, and when each makes sense
- The observability gap: why event-driven systems are harder to debug and how to close the gap
- Decision matrix: latency requirements, consistency needs, team autonomy, and failure recovery as inputs

**This article gives architects a structured way to choose — instead of defaulting to whatever the last conference talk recommended.**

---

## Article 4
### Designing for Organizational Reality (Conway's Law in Practice)

Conway's Law isn't a suggestion — it's a force of nature. Your architecture will mirror your org chart whether you plan for it or not. This article shows how to work with that force instead of against it.

Key topics:
- Conway's Law and the Inverse Conway Maneuver — designing org structure to get the architecture you want
- Team cognitive load as an architectural constraint
- Domain-Driven Design's bounded contexts as organizational boundaries, not just technical ones
- The architecture-org mismatch: what happens when your system boundaries don't match your team boundaries
- Practical examples: how team splits, mergers, and reorgs create architectural debt
- The "two-pizza team" myth and what actually determines effective team scope

**Architecture that ignores organizational reality is architecture that will be subverted by organizational reality.**

---

## Article 5
### The Build vs. Buy vs. Compose Decision

Every architect faces this decision repeatedly, and most organizations have no consistent framework for making it. This article provides one.

Key topics:
- The real cost of "build": maintenance, hiring, opportunity cost, and the long tail
- The real cost of "buy": vendor lock-in, integration complexity, feature gaps, and contract negotiation
- The emerging third option — "compose": assembling systems from managed services, open-source components, and thin integration layers
- Decision framework: core competency, differentiation value, operational burden, and switching cost
- The SaaS trap: when buying creates more integration work than building would have
- Vendor evaluation beyond the feature matrix: API quality, data portability, and exit strategy
- Case studies: decisions that looked right at purchase and wrong two years later

**The best architectural decisions aren't about technology — they're about where you want to spend your engineering attention.**

---

## Article 6
### Evolutionary Architecture: Designing for Change You Can't Predict

Systems that can't evolve become liabilities. But "design for change" is vague advice. This article makes it concrete with fitness functions, architectural runways, and incremental migration strategies.

Key topics:
- Architecture fitness functions: automated tests for architectural properties (performance budgets, dependency rules, coupling metrics)
- The architectural runway: how much future-proofing is enough vs. speculative generality
- Strangler fig pattern in practice: incremental migration without big-bang rewrites
- Feature flags as an architectural tool, not just a deployment mechanism
- API versioning strategies that don't create maintenance nightmares
- The YAGNI tension: when to invest in flexibility and when to ship the simplest thing

**Evolutionary architecture isn't about predicting the future — it's about making the future cheaper to respond to.**

---

## Article 7
### Data Architecture Decisions That Haunt You

Data decisions are the hardest to reverse. Wrong database choice, wrong consistency model, wrong data ownership boundaries — these mistakes compound for years. This article covers the decisions that matter most.

Key topics:
- Polyglot persistence: when multiple databases make sense and when they create operational hell
- CQRS and event sourcing: powerful patterns with hidden operational costs
- Data mesh vs. data lakehouse vs. centralized data platform — cutting through the marketing
- Data ownership at service boundaries: who owns the data when services share it?
- Schema evolution strategies that don't break consumers
- The consistency spectrum: strong, eventual, causal — and how to choose based on business requirements, not technical preference

**Data architecture mistakes are the most expensive to fix because data outlives every other architectural decision.**

---

## Article 8
### API Design as Architecture

APIs are the most durable architectural decisions you make. Internal APIs become external APIs. External APIs become contracts you can't break. This article treats API design as a first-class architectural concern.

Key topics:
- REST vs. GraphQL vs. gRPC: decision framework based on consumer needs, not developer preference
- API-first design: designing the contract before the implementation
- Backward compatibility as an architectural constraint — and the versioning strategies that preserve it
- API gateways as architectural components: routing, rate limiting, authentication, and the aggregation layer
- Internal API standards: consistency across teams without a central API committee
- The API lifecycle: design, review, publish, deprecate, sunset — and why most orgs skip the last two

**Your API is your architecture's public face. Design it like it matters — because it's the one thing you can't easily change.**

---

## Article 9
### Architectural Fitness for Cloud-Native Systems

Cloud-native architecture has its own set of tradeoffs that traditional architecture guidance doesn't cover. This article addresses the decisions specific to cloud-native systems.

Key topics:
- The twelve-factor app revisited: what still holds, what's outdated, and what's missing
- Container orchestration decisions: when Kubernetes is overkill and what the alternatives are
- Serverless architecture tradeoffs: cold starts, vendor lock-in, debugging complexity, and cost unpredictability
- Multi-cloud as an architectural strategy: when it's justified and when it's resume-driven
- Cloud-native anti-patterns: over-decomposition, premature optimization for scale, and infrastructure complexity that exceeds application complexity
- The managed services spectrum: how much operational responsibility to hand to your cloud provider

**Cloud-native doesn't mean "use every cloud service available." It means making deliberate decisions about what to manage and what to delegate.**

---

## Article 10
### Architecture Under Regulatory Constraint

Regulated industries (finance, healthcare, defense, government) face architectural constraints that most architecture content ignores. This article covers how regulation shapes — and sometimes improves — architectural decisions.

Key topics:
- Data residency and sovereignty: how GDPR, HIPAA, and FedRAMP constrain your deployment architecture
- Audit trail requirements as architectural drivers: immutable logs, event sourcing, and tamper-evident systems
- Encryption at rest and in transit: architectural implications beyond "just encrypt everything"
- Third-party risk management: how vendor dependencies become compliance liabilities
- Air-gapped and disconnected architectures: designing for environments without internet access
- The compliance-as-code movement: encoding regulatory requirements into architectural guardrails

**Regulation isn't a constraint on good architecture — it's a forcing function for disciplined architecture.**

---

## Article 11
### The Architecture Review That Actually Works

Most architecture reviews are either rubber stamps or adversarial interrogations. This article redesigns the architecture review as a collaborative decision-making process.

Key topics:
- Why most architecture reviews fail: wrong audience, wrong timing, wrong format
- The lightweight ADR review: asynchronous, focused on decisions, not diagrams
- The design review vs. the architecture review: different purposes, different formats
- Review checklists that catch real problems: operational readiness, failure modes, data ownership, security boundaries
- How to present architectural decisions to reviewers who disagree with your approach
- Scaling architecture review: how to maintain quality when you have 50 teams and 3 architects
- The architecture guild model: distributed review with centralized standards

**An architecture review should make the architecture better — not just validate that someone drew a diagram.**

---

## Article 12 — Capstone
### The Spotify Model Didn't Work (Even at Spotify): Architecture Decisions in Organizational Context

The capstone examines one of the most influential — and most misunderstood — architectural and organizational models in software engineering. The "Spotify Model" of squads, tribes, chapters, and guilds was widely copied across the industry, but the architectural decisions it implied often failed when transplanted to different organizational contexts.

The narrative covers:
- **The original vision**: how Spotify's engineering culture and architecture co-evolved — autonomous squads owning microservices, aligned through missions not mandates
- **The reality gap**: what Spotify themselves said didn't work — coordination overhead, duplicated effort, inconsistent quality, and the "autonomous teams" that couldn't actually ship independently
- **The copycat problem**: organizations that adopted the org model without understanding the architectural prerequisites — and ended up with distributed monoliths staffed by "squads" that couldn't deploy independently
- **The architectural lesson**: Conway's Law in reverse — teams that copied the org structure got an architecture they didn't want, because the architecture requires specific technical foundations (service boundaries, API contracts, platform capabilities) that most orgs hadn't built
- **The course correction**: how mature organizations adapted the model — keeping autonomy where it mattered, adding coordination where it was missing, and investing in platform engineering to make independence actually possible
- **The meta-lesson**: why architectural decisions can't be separated from organizational decisions — and why the best architects understand both

The capstone closes the series with a clear message:
**Architecture is not a technical discipline practiced in organizational isolation. The best architectural decisions account for the humans, teams, incentives, and constraints that will determine whether the architecture survives contact with reality.**
