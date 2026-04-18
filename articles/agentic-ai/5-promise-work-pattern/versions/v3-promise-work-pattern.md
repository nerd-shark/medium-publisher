---
title: "The Promise/Work Pattern: Kubernetes-Style Orchestration for AI Agents"
subtitle: "Your agent crashed mid-task. The user's request is gone. There's no retry, no recovery, no record it ever happened."
series: "Agentic AI Part 5"
reading-time: "11 minutes"
target-audience: "Backend engineers, AI engineers, platform engineers building production agent systems"
keywords: "promise work pattern, agent orchestration, kubernetes, declarative AI, multi-agent systems, agentic AI, reconciliation loop"
tags: "Agentic AI, Agent Orchestration, Kubernetes, Distributed Systems, Multi-Agent Systems, Production AI"
status: "v3-draft"
created: "2026-03-29"
author: "Daniel Stauffer"
---

# The Promise/Work Pattern: Kubernetes-Style Orchestration for AI Agents

Part 5 of my series on Agentic AI. Last time, we built [your first agentic AI system](link) — from weekend project to production-ready agent with evaluation, guardrails, and observability. This time: what happens when your agent crashes mid-task, and nobody knows. Follow along for more deep dives into building AI systems that actually work.

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

Here's the flow. A user or system creates a Promise: "Analyze contract batch #4721." The orchestrator decomposes the Promise into Work units. Available agents claim Work units they can handle. Agents execute Work, reporting status back. A reconciliation loop monitors progress and handles failures. When all Work completes, the Promise is fulfilled.

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
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
```

The critical difference from imperative orchestration: if an agent crashes while processing a Work unit, the Work unit's status remains IN_PROGRESS. The reconciliation loop detects the stall (no progress update in N seconds), marks it as failed, and reassigns it to another agent. The Promise tracks overall progress. Nothing is lost.

## The Reconciliation Loop

The reconciliation loop is the heart of the pattern. It runs continuously, comparing desired state (what Promises expect) against actual state (what Work units report).

```python
import asyncio
from datetime import timedelta

class Reconciler:
    def __init__(self, store, agent_pool, stall_timeout=300):
        self.store = store          # Durable state store
        self.agent_pool = agent_pool
        self.stall_timeout = stall_timeout  # seconds
    
    async def run(self):
        while True:
            promises = await self.store.get_active_promises()
            for promise in promises:
                await self._reconcile_promise(promise)
            await asyncio.sleep(10)  # Check every 10 seconds
    
    async def _reconcile_promise(self, promise):
        for work in promise.work_units:
            if work.status == Status.PENDING:
                await self._assign_work(work)
            
            elif work.status == Status.IN_PROGRESS:
                if self._is_stalled(work):
                    await self._handle_stall(work)
            
            elif work.status == Status.FAILED:
                if work.retry_count < work.max_retries:
                    work.status = Status.RETRYING
                    work.retry_count += 1
                    await self._assign_work(work)
                else:
                    await self._handle_permanent_failure(work, promise)
        
        # Check if Promise is fulfilled
        if all(w.status == Status.COMPLETED for w in promise.work_units):
            promise.status = Status.COMPLETED
            promise.completed_at = datetime.utcnow()
            await self.store.update_promise(promise)
    
    def _is_stalled(self, work) -> bool:
        elapsed = datetime.utcnow() - work.last_heartbeat
        return elapsed > timedelta(seconds=self.stall_timeout)
    
    async def _assign_work(self, work):
        agent = await self.agent_pool.get_available_agent(work.task_type)
        if agent:
            work.assigned_agent = agent.id
            work.status = Status.IN_PROGRESS
            await agent.execute(work)
    
    async def _handle_stall(self, work):
        work.status = Status.FAILED
        work.assigned_agent = None
        await self.store.update_work(work)
    
    async def _handle_permanent_failure(self, work, promise):
        promise.status = Status.FAILED
        await self.store.update_promise(promise)
        await self._notify_failure(promise, work)
```

This loop handles every failure mode automatically. Agent crashes mid-task — the stall detector catches it and reassigns. LLM returns an error — the Work unit fails and retries with exponential backoff. An entire agent pool goes down — Work units queue up and execute when agents recover. A Work unit is permanently broken — the Promise fails gracefully with a clear error trail.

Compare this to imperative orchestration where you'd need explicit try/catch blocks, manual retry logic, state tracking in application memory (lost on crash), and custom recovery procedures for every failure mode. The reconciliation loop handles all of this with one mechanism.

## Declarative vs. Imperative: Why It Matters

Most agent frameworks today use imperative orchestration. You write a script that says: "First, call the extraction agent. Then, take the output and pass it to the classification agent. Then, take that output and pass it to the report agent." Step by step, in order, with explicit error handling at each step.

This works fine for simple, linear workflows. But it breaks down fast.

Imperative orchestration couples the orchestration logic to the execution order. If you want to parallelize two steps, you rewrite the orchestrator. If you want to add a new step, you modify the pipeline. If a step fails, you need explicit recovery logic for that specific failure at that specific point in the pipeline.

Declarative orchestration decouples what from how. The Promise says "I want a risk assessment of this contract." The orchestrator figures out the Work units, the execution order, the parallelization opportunities, and the failure recovery. Adding a new step means adding a new Work unit type — the orchestrator picks it up automatically.

| Aspect | Imperative | Declarative (Promise/Work) |
|--------|-----------|---------------------------|
| Failure recovery | Manual try/catch per step | Automatic via reconciliation |
| State persistence | In-memory (lost on crash) | Durable store (survives crashes) |
| Parallelization | Explicit async/await | Automatic (independent Work units) |
| Adding new steps | Modify pipeline code | Add new Work unit type |
| Observability | Custom logging per step | Built-in progress tracking |
| Retry logic | Per-step implementation | Centralized in reconciler |
| Scaling | Rewrite for distribution | Add more agents to pool |

The tradeoff is upfront complexity. Imperative orchestration is simpler to build initially — it's just a script. Promise/Work requires a state store, a reconciliation loop, and agent registration. But the operational complexity inverts quickly. At 100 tasks per day, imperative is fine. At 10,000 tasks per day with 5% failure rates, you'll spend more time debugging imperative recovery logic than you spent building it.

## Implementation Strategies

You don't need to build this from scratch. Several infrastructure patterns map directly to Promise/Work.

**Kubernetes Custom Resources**: If you're already running on Kubernetes, define Promise and Work as Custom Resource Definitions (CRDs). Write a controller that watches for new Promises, creates Work units, and reconciles state. This gives you Kubernetes-native retry, scheduling, and observability for free.

**Message Queue + State Store**: Use Kafka or RabbitMQ for Work distribution and PostgreSQL or Redis for Promise/Work state. Agents consume Work from queues, update state in the store, and the reconciler polls the store. This is the most common production implementation because it uses infrastructure teams already have.

**Lightweight REST API**: For simpler deployments, a FastAPI service that manages Promise/Work state in PostgreSQL. Agents poll for available Work, claim it, execute, and report back. The reconciler runs as a background task in the same service. Less infrastructure, easier to deploy, works well up to a few thousand tasks per day.

```python
# Lightweight Promise/Work API example
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start reconciler as background task
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
    work_units = decompose(promise)  # Break into Work units
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
            {"id": w.id, "type": w.task_type, "status": w.status.value}
            for w in promise.work_units
        ]
    }

@app.post("/work/claim")
async def claim_work(agent_id: str, task_types: list[str]):
    work = await store.claim_available_work(agent_id, task_types)
    if work:
        return {"work_id": work.id, "task_type": work.task_type, "input": work.input_data}
    return {"work_id": None}  # No work available

@app.post("/work/{work_id}/complete")
async def complete_work(work_id: str, output: dict):
    await store.complete_work(work_id, output)
    return {"status": "completed"}
```

Agents become simple workers that poll for available Work, execute it, and report results. They don't need to know about Promises, other agents, or the overall workflow. They just do their job and report back.

## Real-World Example: Document Processing Pipeline

Let's make this concrete. A legal tech company processes 5,000 contracts per day. Each contract needs text extraction, clause identification, risk classification, compliance checking, and report generation.

Without Promise/Work: A Python script iterates through contracts, calling each processing step sequentially. If the script crashes at contract #3,247, you restart from the beginning (or build custom checkpoint logic). If the LLM is slow on one contract, everything behind it waits. If you need to scale, you rewrite the script for parallel execution.

With Promise/Work: Each contract becomes a Promise. Each processing step becomes a Work unit. Ten extraction agents, five classification agents, and three report agents pull Work from the queue independently. If an agent crashes, its Work unit is reassigned in 30 seconds. If the LLM is slow, other agents keep processing other contracts. Scaling means adding more agents — no code changes.

The results in production: processing time dropped from 8 hours (sequential) to 45 minutes (parallel with 20 agents). Failure recovery went from "manual investigation" to "automatic retry within 30 seconds." Observability went from "check the logs" to "real-time dashboard showing every Promise and Work unit status."

## When Not to Use This Pattern

Promise/Work is not always the right answer. It adds infrastructure complexity that isn't justified for every use case.

Don't use it for simple, linear, single-agent workflows. If your agent does one thing and doesn't need retry or recovery, a simple function call is fine. Don't use it for real-time, sub-second interactions. The reconciliation loop adds latency (10-30 seconds for failure detection). Chatbots and real-time assistants need immediate responses, not eventual consistency. Don't use it for exploratory or creative tasks where the workflow isn't decomposable into discrete steps. If you can't define the Work units upfront, the pattern doesn't apply.

Use it when you have high-volume batch processing (hundreds or thousands of tasks), when failures are expensive (reprocessing costs time or money), when you need observability into long-running workflows, when you need to scale agents independently, or when regulatory requirements demand audit trails of every processing step.

The sweet spot is workflows that are decomposable, repeatable, and failure-sensitive. Document processing, data pipelines, compliance checking, report generation — these are ideal. Creative writing, open-ended research, and conversational AI — these are not.

## What to Build Monday Morning

Start small. Pick one batch workflow your team runs manually or with a fragile script.

Week 1: Model it as a Promise with Work units. Just the data model — Promise, Work, Status. Store it in PostgreSQL. Don't build the reconciler yet.

Week 2: Build a simple reconciler that polls every 30 seconds. Assign Work to a single agent. Handle the happy path.

Week 3: Add failure handling. Stall detection, retry logic, permanent failure handling. Run it against your real workflow.

Week 4: Add a second agent type. See how the pattern handles parallel execution and mixed workloads without changing the orchestration logic.

You'll know it's working when your first agent crash happens and the system recovers automatically — without a 3 AM page and without four hours of manual reconciliation.

---

**Resources**:
- [Kubernetes: Declarative Management](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/)
- [The Reconciliation Pattern — Kubernetes Design](https://book.kubebuilder.io/cronjob-tutorial/controller-overview)
- [LangGraph: Stateful Agent Workflows](https://langchain-ai.github.io/langgraph/)
- [Temporal: Durable Execution for Workflows](https://temporal.io/)
- [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)

---

## Series Navigation

**Previous Article**: [Building Your First Agentic AI System: A Practical Guide](link)

**Next Article**: [Memory Systems for AI Agents: Beyond Context Windows](link) *(Coming soon!)*

**Coming Up**: Long-term memory architectures, vector databases, memory consolidation, and the economics of agentic AI

---

*This is Part 5 of the Agentic AI series. Read [Part 1: From Chatbots to Co-Workers](link), [Part 2: The Anatomy of an AI Agent](link), [Part 3: Multi-Agent Systems](link), and [Part 4: Building Your First Agentic AI System](link).*

**About the Author**: Daniel Stauffer is an Enterprise Architect who designs production AI systems using Kubernetes-native patterns. He believes the best agent orchestration borrows from infrastructure, not from chatbot frameworks.

**Tags**: #AgenticAI #AIAgents #Kubernetes #PromiseWork #DistributedSystems #ProductionAI #AgentOrchestration #Python #SoftwareArchitecture
