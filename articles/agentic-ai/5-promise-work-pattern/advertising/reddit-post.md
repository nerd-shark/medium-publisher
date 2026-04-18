# Reddit Post

**Article**: The Promise/Work Pattern: Kubernetes-Style Orchestration for AI Agents
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Suggested Subreddits
- r/MachineLearning
- r/artificial
- r/programming
- r/softwarearchitecture
- r/ExperiencedDevs
- r/devops
- r/kubernetes

## Post Title
The Promise/Work Pattern: Applying Kubernetes reconciliation to AI agent orchestration, with a capability-aware orchestrator (Python implementation)

## Post Body

Most AI agent frameworks use imperative orchestration — a script that says "call agent A, pass output to agent B, then agent C." Works for demos. Breaks in production. I learned this the hard way last October.

An agent I helped build crashed at 3 AM processing contract #3,247 out of 5,000. When it restarted — no state, no checkpoint, no idea where it left off. On-call engineer spent 4 hours reconciling. Third time that quarter. The LLM failure wasn't the problem. The problem was fire-and-forget orchestration with no durable state.

Kubernetes solved this for infrastructure with declarative state management and reconciliation loops. I've been applying the same pattern to agent orchestration — and in v4 of this writeup, I've added the piece most frameworks skip entirely: a capability-aware orchestrator agent.

**The Pattern**

- **Promise**: A declaration of desired outcome. "Analyze this contract batch." Not how — just what.
- **Work Units**: Discrete, independently executable steps with dependency tracking. Extract text → classify risk → check compliance → generate report. The orchestrator models these as a DAG.
- **Orchestrator Agent**: The brain. Decomposes Promises into Work units using an LLM. Maintains a capability registry for every agent — not just what they can do, but how well they handle edge cases. Routes ambiguous work to specialists. Runs consensus when confidence is low. Re-plans when things fail permanently.
- **Agents**: Claim Work units they can handle. Execute independently. Report results. Self-register their capabilities.
- **Reconciler**: Runs continuously. Compares desired state (Promises) against actual state (Work units). Assigns pending work (respecting dependencies). Detects stalls. Retries failures. Delegates permanent failures to the orchestrator for re-planning.

**The Orchestrator — Why It Matters**

The orchestrator maintains an `AgentProfile` for every agent with per-task-type metrics: success rate, average latency, and edge case accuracy. These update via exponential moving average after every Work unit completion.

When routing, the orchestrator weighs these differently based on complexity:
- Standard work: 50% success rate, 30% availability, 20% speed
- Edge cases: 60% edge case accuracy, 30% success rate, 10% availability

For genuinely ambiguous work (contract clause that two lawyers would disagree on), the orchestrator routes to multiple agents and compares:
- Results agree → use it
- One agent highly confident (>0.85) → trust it
- No consensus, low confidence → flag for human review

This creates a feedback loop. Every confirmed result updates the registry. Over time, the orchestrator learns who handles what well.

**Re-planning on Failure**

When a Work unit fails permanently (retries exhausted), the orchestrator doesn't just cascade the failure. It asks the LLM: given what's completed and what failed, can we still fulfill the Promise? Options: alternative approach, partial fulfillment, or graceful failure. This recovered about 15% of Promises that would have been total failures under a static pipeline.

**Why it works**

The reconciliation loop handles mechanical failure recovery. The orchestrator handles intelligent adaptation. Keeping them separate means:
- Reconciler is deterministic and testable
- Orchestrator is probabilistic and adaptive
- You can evolve them independently

**Implementation options**

1. **Kubernetes CRDs**: Promise/Work as Custom Resources. Controller + orchestrator deployment. K8s-native retry, scheduling, observability.
2. **Kafka + PostgreSQL**: Most common production approach. Kafka for work distribution, Postgres for state and registry.
3. **FastAPI + PostgreSQL**: Lightweight. Agents self-register via REST, poll for work. Reconciler + orchestrator as background tasks.

**Real results**

Document processing pipeline (5,000 contracts/day):
- Sequential script: 8 hours, manual failure recovery
- Promise/Work + orchestrator with 20 agents: 45 minutes, automatic recovery
- Edge case accuracy: 71% → 89% over three months (orchestrator learned routing)
- Human review queue: down 40% (consensus caught disagreements early)
- Promise recovery rate: ~15% of permanent failures salvaged via re-planning

**Comparison table**

| Aspect | Imperative | Promise/Work + Orchestrator |
|--------|-----------|---------------------------|
| Failure recovery | Manual try/catch | Automatic reconciliation + re-planning |
| State persistence | In-memory | Durable store |
| Parallelization | Explicit async/await | Automatic (dependency DAG) |
| Adding steps | Modify pipeline | Add Work unit type |
| Adding agents | Modify routing | Self-register in capability registry |
| Edge cases | Hard-coded rules | Learned from performance history |
| Adaptation | None — static | Dynamic re-planning on failure |
| Scaling | Rewrite | Add agents |

**When NOT to use it**

- Simple, linear, single-agent workflows (just use a function call)
- Real-time sub-second interactions (reconciliation adds 10-30s latency)
- Non-decomposable creative tasks (can't define Work units upfront)

Sweet spot: decomposable, repeatable, failure-sensitive workflows where edge cases matter. Document processing, data pipelines, compliance checking, report generation.

The article includes full Python implementation (data models, orchestrator with capability registry, consensus routing, re-planning, reconciliation loop, FastAPI endpoints, agent self-registration) and a 5-week build plan.

[ARTICLE URL]

Part 5 of my Agentic AI series. Happy to discuss the orchestrator design, capability registry approaches, consensus mechanisms, or war stories from production.

---

**Format**: No hashtags, technical, discussion-focused
