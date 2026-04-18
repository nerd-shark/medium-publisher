# X/Twitter Post

**Article**: The Promise/Work Pattern: Kubernetes-Style Orchestration for AI Agents
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Main Post

An agent I helped build crashed at 3 AM. Mid-task. Contract #3,247 out of 5,000.

When it restarted — no state. No checkpoint. No idea where it left off.

Kubernetes solved this for infrastructure a decade ago. Same pattern works for agents. But you also need an orchestrator that knows its team.

[ARTICLE URL]

#AgenticAI #SystemDesign

---

## Thread

**2/8**
The pattern is simple once you see it.

Promise = desired outcome ("analyze this contract batch")
Work = discrete steps with dependencies
Orchestrator = decomposes promises, routes intelligently
Agents = claim work, execute, report back
Reconciler = watches everything, retries failures

Agent crashes? Work gets reassigned in 30 seconds.

**3/8**
Most agent frameworks are still imperative. "Call A, pass output to B, then C."

That's a script. Scripts don't recover from failures.

Declarative: "I want this outcome." The orchestrator figures out how — including dependencies, parallelization, and recovery.

**4/8**
The orchestrator isn't a dumb dispatcher. It maintains a capability registry for every agent.

Not just "agent X does extraction." But how well. How fast. And critically — how it handles edge cases.

Messy scanned PDF? Routes to the agent with 94% edge case accuracy, not the fastest one.

**5/8**
When work is ambiguous, the orchestrator routes to multiple agents and compares.

Consensus → use it.
One agent highly confident → trust it.
Everyone disagrees, low confidence → flag for human review.

No silent wrong answers. And the routing improves over time from the feedback.

**6/8**
When a work unit fails permanently, the orchestrator doesn't just cascade the failure.

It re-plans. Alternative approach? Partial result? Graceful failure?

An LLM decides — based on what's already completed and what's still possible.

**7/8**
Real results from a document processing pipeline:

Sequential script: 8 hours, manual recovery
Promise/Work + orchestrator: 45 minutes, auto-recovery
Edge case accuracy: 71% → 89% over 3 months
Human review queue: down 40%

**8/8**
Don't use this for everything.

Simple single-agent tasks? Just call a function.
Real-time chatbots? Too much latency.
Creative tasks you can't decompose? Doesn't fit.

Sweet spot: batch processing where failures are expensive and edge cases matter.

Full guide with Python code: [ARTICLE URL]

---

**Thread length**: 8 tweets
