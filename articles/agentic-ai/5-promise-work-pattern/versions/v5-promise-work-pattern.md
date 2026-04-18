---
title: "The Promise/Work Pattern: Kubernetes-Style Orchestration for AI Agents"
subtitle: "Your agent crashed mid-task. The user's request is gone. There's no retry, no recovery, no record it ever happened."
series: "Agentic AI Part 5"
reading-time: "14 minutes"
target-audience: "Backend engineers, AI engineers, platform engineers building production agent systems"
keywords: "promise work pattern, agent orchestration, kubernetes, declarative AI, multi-agent systems, agentic AI, reconciliation loop, orchestrator agent"
tags: "Agentic AI, Agent Orchestration, Kubernetes, Distributed Systems, Multi-Agent Systems, Production AI"
status: "v5-draft"
created: "2026-03-29"
updated: "2026-03-31"
author: "Daniel Stauffer"
changes-from-v4: "Anti-AI-voice final pass applied per steering doc. Eliminated fake contrast patterns, softened absolute language, broke up too-perfect rhythm, removed performative importance framing."
---

# The Promise/Work Pattern: Kubernetes-Style Orchestration for AI Agents

Part 5 of my series on Agentic AI. Last time, we built [your first agentic AI system](https://medium.com/@the-architect-ds/building-your-first-agentic-ai-system-a-practical-guide-eab2a281de62) — from weekend project to production-ready agent with evaluation, guardrails, and observability. This time: what happens when your agent crashes mid-task, and nobody knows. Follow along for more deep dives into building AI systems that actually work.

## The 3 AM Agent Failure

Last October, a document processing agent I helped build was humming along nicely. Ten thousand contracts a day. Extract clauses, classify risk levels, flag compliance issues, generate summary reports. Three months in production without a hiccup. The team had stopped worrying about it.

Then at 3:17 AM on a Tuesday, Anthropic's API had a transient error. Just a blip — maybe 30 seconds of elevated error rates. Our agent was mid-way through a batch of 200 contracts. The process crashed. When it restarted, it had no idea where it left off. Which contracts were done? Which were half-processed with partial data sitting in the output table? Which ones never got touched?

The on-call engineer — a senior guy who'd been at the company for four years — spent the next morning manually reconciling 200 contracts against the output database. Took him about four hours. He was not happy. And this was the third time it had happened that quarter.

The LLM failure wasn't the problem. Transient errors happen. That's just life with external APIs. The real problem was that our orchestration had no concept of durable state. Fire and forget. When it worked, nobody thought about it. When it failed, it was a mess.

I kept thinking: Kubernetes solved this exact problem for infrastructure over a decade ago. Why are we still building agent orchestration like it's a bash script?

## What Kubernetes Got Right

Here's what Kubernetes figured out that most agent frameworks haven't: don't tell things what to do step by step. Describe what you want the end state to look like, and let a reconciliation loop figure out how to get there.

You don't say "start 3 pods, then configure networking, then attach storage." You say "I want 3 replicas of this service with 2GB of memory each." Kubernetes takes it from there. If a pod crashes, the loop notices — hey, there are 2 pods but I wanted 3 — and spins up a new one. No human intervention. No runbook. No 3 AM page.

That's the declarative model. You describe what, not how. The system handles the how, including all the ugly parts — retries, failures, partial state, recovery.

Most agent frameworks today are still imperative. "Call agent A. Take the output. Pass it to agent B. Then agent C." It's a script. And scripts don't recover gracefully from failures because they weren't designed to.

## The Pattern: Promises and Work Units

The pattern has two core concepts.

A Promise is a declaration of desired outcome. "I promise to analyze this document and produce a risk assessment." It doesn't specify how — just what the end state should look like. A Promise has a status (pending, in_progress, completed, failed), tracks progress, and persists in durable storage.

A Work unit is a discrete, executable step toward fulfilling a Promise. "Extract text from pages 1-50." "Classify risk level of extracted clauses." "Generate summary report." Each Work unit is independently executable, independently retriable, and independently trackable.

Here's the flow. A user or system creates a Promise: "Analyze contract batch #4721." An orchestrator agent decomposes the Promise into Work units, modeling dependencies between them. Available agents claim Work units they can handle. Agents execute Work, reporting status back. A reconciliation loop monitors progress and handles failures. When all Work completes, the Promise is fulfilled.


```python
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Optional
import uuid

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"

@dataclass
class Promise:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    desired_outcome: str = ""
    status: Status = Status.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    work_units: list = field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3
    
    @property
    def progress(self) -> float:
        if not self.work_units:
            return 0.0
        completed = sum(1 for w in self.work_units if w.status == Status.COMPLETED)
        return completed / len(self.work_units)

@dataclass
class WorkUnit:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    promise_id: str = ""
    task_type: str = ""
    input_data: dict = field(default_factory=dict)
    output_data: dict = field(default_factory=dict)
    status: Status = Status.PENDING
    assigned_agent: Optional[str] = None
    depends_on: list = field(default_factory=list)  # IDs of Work units this depends on
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
```

The critical difference from imperative orchestration: if an agent crashes while processing a Work unit, the Work unit's status remains IN_PROGRESS. The reconciliation loop detects the stall (no progress update in N seconds), marks it as failed, and reassigns it to another agent. The Promise tracks overall progress. Nothing is lost.

Notice the `depends_on` field on WorkUnit. Not all Work units are independent — "classify risk" can't run until "extract text" finishes. The orchestrator models these dependencies, and the reconciler respects them. More on that shortly.


## The Orchestrator Agent

Here's the piece most agent frameworks skip entirely: who decides what Work to create and who should do it?

In the Kubernetes world, this is the controller — the brain that watches desired state and drives toward it. In a multi-agent system, this is the orchestrator agent. It's an AI-powered agent that understands the intent behind a Promise, knows the capabilities of every agent in the pool, and makes decisions about decomposition, routing, and adaptation when things go wrong.

The orchestrator has three jobs: decompose Promises into Work units with dependency awareness, route Work to the right agent based on capability and track record, and re-plan when things go sideways.

### Capability-Aware Agent Registry

The orchestrator maintains a living registry of every agent in the system — not just what they can do, but how well they do it.

```python
@dataclass
class AgentCapability:
    task_type: str
    confidence_threshold: float  # Minimum confidence for solo assignment
    avg_latency_ms: float
    success_rate: float          # Historical success rate (0.0-1.0)
    edge_case_accuracy: float    # Performance on ambiguous inputs
    last_updated: datetime = field(default_factory=datetime.utcnow)

@dataclass
class AgentProfile:
    id: str
    name: str
    capabilities: list[AgentCapability] = field(default_factory=list)
    current_load: int = 0
    max_concurrent: int = 5
    total_completed: int = 0
    total_failed: int = 0
    
    def get_capability(self, task_type: str) -> Optional[AgentCapability]:
        return next((c for c in self.capabilities if c.task_type == task_type), None)
    
    @property
    def overall_reliability(self) -> float:
        total = self.total_completed + self.total_failed
        return self.total_completed / total if total > 0 else 0.0

class AgentRegistry:
    def __init__(self, store):
        self.store = store
    
    async def find_best_agent(self, task_type: str, 
                               complexity: str = "standard") -> Optional[AgentProfile]:
        agents = await self.store.get_agents_for_task(task_type)
        if not agents:
            return None
        
        if complexity == "edge_case":
            # For ambiguous work, prioritize edge case accuracy
            return max(agents, key=lambda a: (
                a.get_capability(task_type).edge_case_accuracy * 0.6 +
                a.get_capability(task_type).success_rate * 0.3 +
                (1 - a.current_load / a.max_concurrent) * 0.1
            ))
        
        # Standard routing: balance reliability, speed, and load
        return max(agents, key=lambda a: (
            a.get_capability(task_type).success_rate * 0.5 +
            (1 - a.current_load / a.max_concurrent) * 0.3 +
            (1 - a.get_capability(task_type).avg_latency_ms / 10000) * 0.2
        ))
    
    async def update_performance(self, agent_id: str, task_type: str,
                                  succeeded: bool, latency_ms: float,
                                  was_edge_case: bool = False):
        profile = await self.store.get_agent(agent_id)
        cap = profile.get_capability(task_type)
        
        # Exponential moving average for metrics
        alpha = 0.1
        cap.avg_latency_ms = (1 - alpha) * cap.avg_latency_ms + alpha * latency_ms
        cap.success_rate = (1 - alpha) * cap.success_rate + alpha * (1.0 if succeeded else 0.0)
        
        if was_edge_case:
            cap.edge_case_accuracy = (
                (1 - alpha) * cap.edge_case_accuracy + alpha * (1.0 if succeeded else 0.0)
            )
        
        cap.last_updated = datetime.utcnow()
        await self.store.update_agent(profile)
```

The registry doesn't just track "agent X can do text extraction." It tracks how well agent X does text extraction, how fast it is, and — this is the part that took us a while to figure out — how it performs on edge cases.

Why track edge case performance separately? Because in real workflows, the easy cases aren't where you lose sleep. Any halfway decent extraction agent handles clean, well-formatted contracts. The problem is the scanned PDF with handwritten annotations, the contract written in legalese so dense it might as well be encrypted, the clause that's ambiguous enough that two human lawyers would disagree on the classification.

The orchestrator learns which agents handle these grey areas well. In our system, Agent A had a 98% success rate on standard extractions but dropped to 71% on messy inputs. Agent B was slower overall but maintained 94% accuracy on edge cases. When the orchestrator sees a Work unit flagged as complex or ambiguous, it routes to Agent B — even though Agent A is faster for the average case.


### Intelligent Decomposition

The orchestrator doesn't use a static mapping of "Promise type → Work units." It uses an LLM to reason about the Promise intent and produce a dependency-aware execution plan.

```python
class OrchestratorAgent:
    def __init__(self, llm_client, registry: AgentRegistry, store):
        self.llm = llm_client
        self.registry = registry
        self.store = store
    
    async def decompose_promise(self, promise: Promise) -> list[WorkUnit]:
        # Ask the LLM to plan the work breakdown
        available_capabilities = await self.registry.get_all_capabilities()
        
        plan = await self.llm.generate(
            system="""You are a work decomposition planner. Given a desired outcome 
            and available agent capabilities, produce a plan of work units with 
            dependencies. Each work unit should map to an available capability.
            Flag any work units that may involve edge cases or ambiguity.""",
            prompt=f"""
            Promise: {promise.description}
            Desired outcome: {promise.desired_outcome}
            
            Available capabilities: {available_capabilities}
            
            Produce a JSON plan with:
            - work_units: list of {{task_type, description, input_spec, complexity, depends_on}}
            - complexity should be "standard" or "edge_case"
            - depends_on should reference other work unit indices
            """,
            response_format="json"
        )
        
        work_units = []
        for i, item in enumerate(plan["work_units"]):
            work = WorkUnit(
                promise_id=promise.id,
                task_type=item["task_type"],
                input_data={
                    "description": item["description"],
                    "input_spec": item["input_spec"],
                    "complexity": item["complexity"]
                },
                depends_on=[work_units[dep].id for dep in item.get("depends_on", [])]
            )
            work_units.append(work)
        
        return work_units
    
    async def assign_work(self, work: WorkUnit):
        complexity = work.input_data.get("complexity", "standard")
        agent = await self.registry.find_best_agent(work.task_type, complexity)
        
        if not agent:
            # No agent available — check if we can split the work differently
            await self._handle_no_agent(work)
            return
        
        work.assigned_agent = agent.id
        work.status = Status.IN_PROGRESS
        await self.store.update_work(work)
```

The decomposition is dynamic. The same Promise — "analyze this contract" — might produce different Work unit plans depending on the contract type, the available agents, and what the orchestrator has learned from previous runs. A straightforward employment agreement might get three Work units. A complex multi-party derivatives contract might get seven, with two flagged as edge cases and routed to the specialist agents.

The orchestrator adapts the plan to the work. A static pipeline can't do that — it treats every input the same regardless of complexity.


### Consensus Routing for Grey Areas

Here's a pattern that emerged from production use: when the orchestrator isn't confident about a Work unit's outcome, it doesn't just pick the best agent. It routes to multiple agents and compares results.

```python
async def route_with_consensus(self, work: WorkUnit, 
                                confidence_threshold: float = 0.85):
    """For ambiguous work, get multiple opinions and compare."""
    task_type = work.task_type
    agents = await self.registry.get_top_agents(task_type, n=3)
    
    if len(agents) < 2:
        # Not enough agents for consensus — route to best available
        return await self.assign_work(work)
    
    # Create shadow work units for consensus
    results = []
    for agent in agents[:3]:
        shadow_work = WorkUnit(
            promise_id=work.promise_id,
            task_type=work.task_type,
            input_data=work.input_data,
            assigned_agent=agent.id
        )
        result = await agent.execute(shadow_work)
        results.append({
            "agent_id": agent.id,
            "output": result,
            "confidence": result.get("confidence", 0.0)
        })
    
    # Check agreement
    if self._results_agree(results):
        # Consensus reached — use the fastest result
        work.output_data = results[0]["output"]
        work.status = Status.COMPLETED
    elif any(r["confidence"] > confidence_threshold for r in results):
        # One agent is highly confident — trust it
        best = max(results, key=lambda r: r["confidence"])
        work.output_data = best["output"]
        work.status = Status.COMPLETED
    else:
        # No consensus, no high confidence — flag for human review
        work.output_data = {
            "needs_review": True,
            "agent_results": results,
            "reason": "No consensus among agents, low confidence across the board"
        }
        work.status = Status.COMPLETED  # Completed but flagged
    
    await self.store.update_work(work)
    
    # Update performance metrics for all participating agents
    for r in results:
        was_correct = r["output"] == work.output_data  # Simplified
        await self.registry.update_performance(
            r["agent_id"], task_type, was_correct,
            latency_ms=r.get("latency_ms", 0),
            was_edge_case=True
        )
```

Think of it like a senior engineer who knows when to ask for a second opinion. The orchestrator doesn't treat every Work unit the same. Standard, clear-cut work goes to the fastest available agent. Ambiguous work gets routed to the agents with the best edge case track records. And when even those agents disagree, the system flags it for human review instead of silently picking a potentially wrong answer.

This creates a feedback loop. Every time a consensus result is confirmed (by a human reviewer or by downstream validation), the orchestrator updates its understanding of each agent's capabilities. Over time, it gets better at knowing who to ask and when to ask for backup.


### Dynamic Re-Planning

Static plans break. An agent that was available when the plan was created might be overloaded by the time its Work unit is ready. A Work unit might fail permanently, making downstream Work units impossible. New information from a completed Work unit might change what remaining Work needs to happen.

```python
async def replan_on_failure(self, failed_work: WorkUnit, promise: Promise):
    """When a Work unit fails permanently, adapt the remaining plan."""
    # Find all Work units that depend on the failed one
    dependents = [w for w in promise.work_units if failed_work.id in w.depends_on]
    
    if not dependents:
        # No downstream impact — just mark the failure
        return
    
    # Ask the LLM: given this failure, can we still fulfill the Promise?
    remaining_work = [w for w in promise.work_units 
                      if w.status not in (Status.COMPLETED, Status.FAILED)]
    
    replan = await self.llm.generate(
        system="""You are a work re-planner. A work unit has permanently failed.
        Determine if the promise can still be fulfilled with an alternative approach,
        or if it should fail gracefully with a partial result.""",
        prompt=f"""
        Promise: {promise.description}
        Failed work: {failed_work.task_type} — {failed_work.input_data}
        Failure reason: {failed_work.output_data.get('error', 'unknown')}
        Remaining work: {[(w.task_type, w.status.value) for w in remaining_work]}
        Completed work outputs: {[w.output_data for w in promise.work_units 
                                   if w.status == Status.COMPLETED]}
        
        Options:
        1. Alternative approach: different work units that achieve the same goal
        2. Partial fulfillment: complete what we can, mark promise as partially done
        3. Fail: the promise cannot be meaningfully fulfilled
        """,
        response_format="json"
    )
    
    if replan["decision"] == "alternative":
        # Replace failed branch with new work units
        new_units = self._create_work_units(replan["new_work"], promise)
        promise.work_units.extend(new_units)
        # Update dependents to point to new units
        for dep in dependents:
            dep.depends_on = [
                new_units[-1].id if d == failed_work.id else d 
                for d in dep.depends_on
            ]
    elif replan["decision"] == "partial":
        # Cancel dependent work, mark promise as partially complete
        for dep in dependents:
            dep.status = Status.FAILED
            dep.output_data = {"skipped": "dependency_failed"}
        promise.status = Status.COMPLETED  # Partial
        promise.output_data = {"partial": True, "reason": replan["reason"]}
    else:
        promise.status = Status.FAILED
    
    await self.store.update_promise(promise)
```

Without re-planning, a single permanent failure cascades into a full Promise failure. With it, the orchestrator can find alternative paths — maybe a different extraction method, maybe a fallback to a simpler analysis, maybe completing 80% of the work and flagging the rest for manual handling. In practice, this turned about 30% of what would have been full failures into partial successes that still delivered usable results.


## The Reconciliation Loop

The reconciliation loop is the heartbeat of the pattern. It runs continuously, comparing desired state (what Promises expect) against actual state (what Work units report). The loop works hand-in-hand with the orchestrator — the loop detects problems, the orchestrator decides what to do about them.

```python
import asyncio
from datetime import timedelta

class Reconciler:
    def __init__(self, store, orchestrator: OrchestratorAgent, stall_timeout=300):
        self.store = store
        self.orchestrator = orchestrator
        self.stall_timeout = stall_timeout  # seconds
    
    async def run(self):
        while True:
            promises = await self.store.get_active_promises()
            for promise in promises:
                await self._reconcile_promise(promise)
            await asyncio.sleep(10)  # Check every 10 seconds
    
    async def _reconcile_promise(self, promise):
        for work in promise.work_units:
            # Skip work whose dependencies aren't met yet
            if not self._dependencies_met(work, promise):
                continue
            
            if work.status == Status.PENDING:
                await self.orchestrator.assign_work(work)
            
            elif work.status == Status.IN_PROGRESS:
                if self._is_stalled(work):
                    await self._handle_stall(work)
            
            elif work.status == Status.FAILED:
                if work.retry_count < work.max_retries:
                    work.status = Status.RETRYING
                    work.retry_count += 1
                    await self.orchestrator.assign_work(work)
                else:
                    # Permanent failure — let the orchestrator re-plan
                    await self.orchestrator.replan_on_failure(work, promise)
        
        # Check if Promise is fulfilled
        completed = [w for w in promise.work_units if w.status == Status.COMPLETED]
        failed = [w for w in promise.work_units if w.status == Status.FAILED]
        
        if len(completed) + len(failed) == len(promise.work_units):
            if failed:
                promise.status = Status.FAILED
            else:
                promise.status = Status.COMPLETED
            promise.completed_at = datetime.utcnow()
            await self.store.update_promise(promise)
    
    def _dependencies_met(self, work: WorkUnit, promise: Promise) -> bool:
        if not work.depends_on:
            return True
        completed_ids = {w.id for w in promise.work_units 
                        if w.status == Status.COMPLETED}
        return all(dep_id in completed_ids for dep_id in work.depends_on)
    
    def _is_stalled(self, work) -> bool:
        elapsed = datetime.utcnow() - work.last_heartbeat
        return elapsed > timedelta(seconds=self.stall_timeout)
    
    async def _handle_stall(self, work):
        work.status = Status.FAILED
        work.assigned_agent = None
        await self.store.update_work(work)
```

The loop respects dependencies — a Work unit won't be assigned until everything it depends on has completed. When retries are exhausted, instead of just marking the Promise as failed, it hands the problem to the orchestrator for re-planning.

Why keep the reconciler and orchestrator separate? The reconciler is deterministic and testable — given this state, take this action. The orchestrator is probabilistic and adaptive — given this situation, figure out the best path forward. You can test, monitor, and evolve them independently. When the orchestrator's LLM-powered re-planning makes a bad call, you can trace it without wading through reconciliation logic. When the reconciler has a timing bug, you can fix it without touching the routing intelligence.


## Declarative vs. Imperative: Why It Matters

Most agent frameworks today use imperative orchestration. You write a script that says: "First, call the extraction agent. Then, take the output and pass it to the classification agent. Then, take that output and pass it to the report agent." Step by step, in order, with explicit error handling at each step.

This works fine for simple, linear workflows. But it falls apart once you need parallelism, failure recovery, or the ability to add new agents without rewriting the pipeline.

Imperative orchestration couples the orchestration logic to the execution order. Want to parallelize two steps? Rewrite the orchestrator. Want to add a new step? Modify the pipeline. A step fails? You need explicit recovery logic for that specific failure at that specific point.

Declarative orchestration decouples what from how. The Promise says "I want a risk assessment of this contract." The orchestrator agent figures out the Work units, the execution order, the parallelization opportunities, the agent assignments, and the failure recovery. Adding a new step means adding a new Work unit type — the orchestrator picks it up. Adding a new agent means registering it in the capability registry — the orchestrator starts routing to it based on its strengths.

| Aspect | Imperative | Declarative (Promise/Work) |
|--------|-----------|---------------------------|
| Failure recovery | Manual try/catch per step | Automatic via reconciliation + re-planning |
| State persistence | In-memory (lost on crash) | Durable store (survives crashes) |
| Parallelization | Explicit async/await | Automatic (dependency-aware DAG) |
| Adding new steps | Modify pipeline code | Add new Work unit type |
| Adding new agents | Modify routing code | Register in capability registry |
| Edge case handling | Hard-coded rules | Learned from performance history |
| Observability | Custom logging per step | Built-in progress tracking |
| Retry logic | Per-step implementation | Centralized in reconciler |
| Adaptation | None — static pipeline | Dynamic re-planning on failure |
| Scaling | Rewrite for distribution | Add more agents to pool |

The tradeoff is real, though. Imperative orchestration is simpler to build initially — it's just a script. Promise/Work requires a state store, a reconciliation loop, an orchestrator agent, and an agent registry. That's a lot of moving parts for a system that processes 50 tasks a day.

But the operational complexity inverts quickly. At 100 tasks per day, imperative is fine. At 10,000 tasks per day with 5% failure rates, you'll spend more time debugging imperative recovery logic than you spent building it. We learned that the hard way.


## Implementation Strategies

You don't need to build this from scratch. Several infrastructure patterns map directly to Promise/Work.

**Kubernetes Custom Resources**: If you're already running on Kubernetes, define Promise and Work as Custom Resource Definitions (CRDs). Write a controller that watches for new Promises, creates Work units, and reconciles state. The orchestrator agent runs as a separate deployment that the controller calls for decomposition and routing decisions. This gives you Kubernetes-native retry, scheduling, and observability for free.

**Message Queue + State Store**: Use Kafka or RabbitMQ for Work distribution and PostgreSQL or Redis for Promise/Work state. The orchestrator agent decomposes Promises and publishes Work to topic-specific queues. Worker agents consume from queues matching their capabilities, update state in the store, and the reconciler polls the store. This is probably the most common production implementation because it uses infrastructure teams already have.

**Lightweight REST API**: For simpler deployments, a FastAPI service that manages Promise/Work state in PostgreSQL. The orchestrator runs as a module within the service. Agents poll for available Work, claim it, execute, and report back. The reconciler runs as a background task. Less infrastructure, easier to deploy, works well up to a few thousand tasks per day.

```python
# Lightweight Promise/Work API with orchestrator
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(reconciler.run())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.post("/promises")
async def create_promise(request: PromiseRequest):
    promise = Promise(
        description=request.description,
        desired_outcome=request.desired_outcome
    )
    # Orchestrator decomposes with dependency awareness
    work_units = await orchestrator.decompose_promise(promise)
    promise.work_units = work_units
    await store.save_promise(promise)
    return {"promise_id": promise.id, "work_units": len(work_units)}

@app.get("/promises/{promise_id}")
async def get_promise(promise_id: str):
    promise = await store.get_promise(promise_id)
    return {
        "id": promise.id,
        "status": promise.status.value,
        "progress": promise.progress,
        "work_units": [
            {"id": w.id, "type": w.task_type, "status": w.status.value,
             "assigned_to": w.assigned_agent, "depends_on": w.depends_on}
            for w in promise.work_units
        ]
    }

@app.post("/work/claim")
async def claim_work(agent_id: str, task_types: list[str]):
    work = await store.claim_available_work(agent_id, task_types)
    if work:
        return {"work_id": work.id, "task_type": work.task_type, "input": work.input_data}
    return {"work_id": None}

@app.post("/work/{work_id}/complete")
async def complete_work(work_id: str, output: dict):
    work = await store.complete_work(work_id, output)
    # Update agent performance metrics
    await registry.update_performance(
        work.assigned_agent, work.task_type,
        succeeded=True, latency_ms=output.get("latency_ms", 0),
        was_edge_case=work.input_data.get("complexity") == "edge_case"
    )
    return {"status": "completed"}

@app.post("/agents/register")
async def register_agent(profile: AgentProfileRequest):
    """Agents self-register with their capabilities."""
    agent = AgentProfile(
        id=profile.id,
        name=profile.name,
        capabilities=[AgentCapability(**c) for c in profile.capabilities]
    )
    await registry.register(agent)
    return {"status": "registered", "agent_id": agent.id}
```

Agents become simple workers that self-register their capabilities, poll for available Work, execute it, and report results. They don't need to know about Promises, other agents, or the overall workflow. The orchestrator handles the decomposition, routing, and adaptation. The agents just do their job and report back.


## Real-World Example: Document Processing Pipeline

Let's make this concrete. A legal tech company processes 5,000 contracts per day. Each contract needs text extraction, clause identification, risk classification, compliance checking, and report generation.

Without Promise/Work: A Python script iterates through contracts, calling each processing step sequentially. If the script crashes at contract #3,247, you restart from the beginning (or build custom checkpoint logic). If the LLM is slow on one contract, everything behind it waits. If you need to scale, you rewrite the script for parallel execution. Every contract gets the same treatment regardless of complexity.

With Promise/Work and an orchestrator: Each contract becomes a Promise. The orchestrator examines the contract metadata — type, length, language, number of parties — and produces a tailored Work plan. A standard employment agreement gets three Work units. A complex multi-jurisdictional derivatives contract gets seven, with the risk classification flagged as an edge case and routed to the specialist agent that handles ambiguous financial instruments well.

Ten extraction agents, five classification agents, and three report agents self-register their capabilities. The orchestrator routes based on the registry — standard extractions go to the fastest available agent, messy scanned PDFs go to the agent with the best OCR edge case accuracy. When two classification agents disagree on a borderline clause, the consensus mechanism flags it for human review instead of silently picking one.

The results we saw in production: processing time dropped from 8 hours (sequential) to 45 minutes (parallel with 20 agents). Failure recovery went from "manual investigation" to "automatic retry within 30 seconds, with re-planning for permanent failures." Edge case accuracy improved from 71% to 89% over three months as the orchestrator learned which agents handled which types of ambiguity. Human review queue dropped by about 40% because the consensus routing caught disagreements before they became downstream errors.

I should note — those numbers came from a specific deployment with specific contract types. Your mileage will vary depending on the complexity of your documents and how much ambiguity your domain has. The pattern helps most when you have a mix of easy and hard cases.

## When Not to Use This Pattern

Promise/Work adds infrastructure complexity that isn't justified for every use case.

Skip it for simple, linear, single-agent workflows. If your agent does one thing and doesn't need retry or recovery, a function call is fine. You'd be over-engineering.

Skip it for real-time, sub-second interactions. The reconciliation loop adds latency — typically 10-30 seconds for failure detection. Chatbots and real-time assistants need immediate responses, not eventual consistency.

And skip it for exploratory or creative tasks where the workflow isn't decomposable into discrete steps. If you can't define the Work units upfront, the pattern doesn't fit.

Where it works well: high-volume batch processing (hundreds or thousands of tasks), workflows where failures are expensive (reprocessing costs time or money), systems that need observability into long-running workflows, environments where you need to scale agents independently, domains with enough ambiguity that intelligent routing pays off, and regulated industries that demand audit trails of every processing step.

The sweet spot is workflows that are decomposable, repeatable, and failure-sensitive. Document processing, data pipelines, compliance checking, report generation — these are good candidates. Creative writing, open-ended research, and conversational AI — probably not.


## What to Build Monday Morning

Start small. Pick one batch workflow your team runs manually or with a fragile script.

**Week 1**: Model it as a Promise with Work units. Just the data model — Promise, Work, Status, dependencies. Store it in PostgreSQL. Don't build the reconciler yet. Get comfortable with how the data looks.

**Week 2**: Build a simple reconciler that polls every 30 seconds. Assign Work to a single agent. Handle the happy path. Respect dependency ordering. This is where you'll discover whether your Work unit boundaries make sense.

**Week 3**: Add the orchestrator. Start with static decomposition rules, then add LLM-powered decomposition. Build the agent registry with basic capability tracking — task types and success rates. You'll probably rewrite the decomposition logic at least once here.

**Week 4**: Add failure handling. Stall detection, retry logic, permanent failure handling with re-planning. Add a second agent type and see how the orchestrator routes between them. This is also when you'll find out if your stall timeout is set too aggressively.

**Week 5**: Add edge case tracking. Log confidence scores from agent outputs. Start building the performance history that lets the orchestrator make smarter routing decisions. Add consensus routing for your most ambiguous Work unit type.

You'll know it's working when your first agent crash happens and the system recovers without anyone getting paged. You'll know the orchestrator is pulling its weight when you see it routing a tricky edge case to the right agent — the one you would have picked yourself — without anyone telling it to.

---

**Resources**:
- [Kubernetes: Declarative Management](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/)
- [The Reconciliation Pattern — Kubernetes Design](https://book.kubebuilder.io/cronjob-tutorial/controller-overview)
- [LangGraph: Stateful Agent Workflows](https://langchain-ai.github.io/langgraph/)
- [Temporal: Durable Execution for Workflows](https://temporal.io/)
- [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)

---

## Series Navigation

**Previous Article**: [Building Your First Agentic AI System: A Practical Guide](https://medium.com/@the-architect-ds/building-your-first-agentic-ai-system-a-practical-guide-eab2a281de62)

**Next Article**: [Memory Systems for AI Agents: Beyond Context Windows](link) *(Coming soon!)*

**Coming Up**: Long-term memory architectures, vector databases, memory consolidation, and the economics of agentic AI

---

*This is Part 5 of the Agentic AI series. Read [Part 1: From Chatbots to Co-Workers](https://medium.com/gitconnected/from-chatbots-to-co-workers-understanding-the-agentic-ai-revolution-03f59ae90227), [Part 2: The Anatomy of an AI Agent](https://medium.com/gitconnected/the-anatomy-of-an-ai-agent-planning-memory-and-tool-use-f8dcbc4351af), [Part 3: Multi-Agent Systems](https://medium.com/gitconnected/multi-agent-systems-when-ai-agents-collaborate-4e825322dd2e), and [Part 4: Building Your First Agentic AI System](https://medium.com/@the-architect-ds/building-your-first-agentic-ai-system-a-practical-guide-eab2a281de62).*

**About the Author**: Daniel Stauffer is an Enterprise Architect who designs production AI systems using Kubernetes-native patterns. He believes the best agent orchestration borrows from infrastructure, not from chatbot frameworks.

**Tags**: #AgenticAI #AIAgents #Kubernetes #PromiseWork #DistributedSystems #ProductionAI #AgentOrchestration #Python #SoftwareArchitecture #OrchestratorAgent
