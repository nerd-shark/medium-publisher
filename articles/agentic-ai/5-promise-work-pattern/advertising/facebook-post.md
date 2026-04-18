# Facebook Post

**Article**: The Promise/Work Pattern: Kubernetes-Style Orchestration for AI Agents
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

Last October, an agent I helped build crashed at 3:17 AM. Mid-task. Processing contract #3,247 out of 5,000.

When it restarted, it had no idea where it left off. Which contracts were done? Which were half-processed with partial data in the output table? Which ones never got touched?

The on-call engineer spent the next morning manually reconciling 200 contracts against the database. About four hours. He was not happy. Third time that quarter.

The LLM failure wasn't the problem — transient errors are just life with external APIs. The real problem was that our orchestration had no concept of durable state. Fire and forget. When it worked, invisible. When it failed, a mess.

Kubernetes solved this exact problem for infrastructure over a decade ago. You don't tell K8s what to do step by step. You declare the desired state. A reconciliation loop makes reality match. Pod crashes? Loop notices, spins up a new one. No human needed.

So we built the same pattern for agents. But we went further — we added an orchestrator agent that actually understands its team's capabilities.

**Promise** = a declaration of desired outcome. "Analyze this contract batch and produce risk assessments." Doesn't specify how — just what the end state should look like. Persists in durable storage.

**Work units** = discrete, executable steps with dependencies. "Extract text from pages 1-50." "Classify risk level." "Generate summary." Each independently retriable. The orchestrator models which steps depend on which.

**Orchestrator** = the brain. Decomposes Promises into Work units. Maintains a capability registry — not just what each agent can do, but how well it handles edge cases. Routes ambiguous work to specialist agents. When multiple agents disagree on a grey area, flags it for human review instead of silently picking one. Re-plans when things fail permanently.

**Agents** = claim Work units they can handle. Execute independently. Report results back. Don't need to know about each other or the overall workflow.

**Reconciler** = runs continuously. Monitors progress. Detects stalls. Retries failures. Reassigns crashed work. Respects dependencies. Tracks everything.

Agent crashes mid-task? Work unit gets reassigned in 30 seconds. LLM returns an error? Automatic retry with backoff. Need to scale? Add more agents. No code changes. Edge case? Orchestrator routes to the agent that handles ambiguity best.

The results were pretty dramatic:

→ Document processing: 8 hours sequential → 45 minutes with 20 agents
→ Edge case accuracy improved from 71% to 89% over three months
→ Human review queue dropped 40% — consensus routing caught disagreements early
→ Failure recovery: manual investigation → automatic retry in 30 seconds

When NOT to use it: simple single-agent workflows (just call a function), real-time chatbots (reconciliation adds latency), creative tasks you can't decompose into steps. This is for batch processing, compliance pipelines, document workflows — stuff where failures are expensive and edge cases matter.

Full guide with Python implementation, orchestrator architecture, and a 5-week build plan:

[ARTICLE URL]

Part 5 of my Agentic AI series.

#AgenticAI #AIAgents #Kubernetes #DistributedSystems #ProductionAI #Python #SoftwareArchitecture #MachineLearning

---

**Character count**: ~2,600
**Hashtags**: 8
