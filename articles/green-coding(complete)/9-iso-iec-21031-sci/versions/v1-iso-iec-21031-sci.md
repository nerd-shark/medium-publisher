---
title: "ISO/IEC 21031: Measuring Your Software's Carbon Footprint With One Number"
subtitle: "You've optimized algorithms, picked efficient languages, and shifted workloads to cleaner grids. Now there's an ISO standard that scores all of it. Here's how to actually use it."
series: "Sustainable Software Engineering Part 9 — Series Finale"
reading-time: "10-12 minutes"
target-audience: "Software architects, platform engineers, engineering managers, sustainability leads"
keywords: "ISO 21031, SCI, software carbon intensity, green software foundation, carbon measurement, sustainable software, green coding"
tags: "Green Coding, Sustainable Software, ISO Standards, Carbon Measurement, Software Architecture"
status: "v1-outline"
created: "2026-04-01"
author: "Daniel Stauffer"
changelog: "v1 - Brainstorming outline with exploratory thinking"
---

# ISO/IEC 21031: Measuring Your Software's Carbon Footprint With One Number

Part 9 — and the finale — of my series on Sustainable Software Engineering. We've spent eight articles optimizing algorithms, databases, CI/CD pipelines, ML training, language choices, and microservice architectures. All of it reduces carbon. None of it gives you a single number you can track over time or compare across systems. That's what this article fixes.

---

## Opening Hook — The Reporting Problem

- You optimized your Python service's hot path (Part 2), switched to batch inference (Part 7), right-sized your containers (Part 6)
- Your cloud bill dropped. Your latency improved. But did your carbon footprint actually go down?
- Nobody can answer that question because nobody's measuring it consistently
- The GHG Protocol gives you annual Scope 2 totals — too aggregated, too annual, too disconnected from the software itself
- A CTO can quote the company's total emissions but can't tell a developer whether the code they shipped last sprint was better or worse
- ISO/IEC 21031:2024 (the SCI specification) changes that — one formula, one score, per functional unit of your software
- Published March 2024, developed by the Green Software Foundation, achieved ISO status in under 3 years (typically takes 5-7)
- Already used by Accenture, UBS, NTT DATA, Microsoft, Autostrade per l'Italia

## The Formula — SCI = (E × I + M) per R

- This is the whole standard in one equation
- E = Energy consumed by your software (kWh) — servers, storage, networking, end-user devices
- I = Carbon intensity of that energy (gCO₂/kWh) — varies by location and time
- M = Embodied emissions from hardware manufacturing, amortized over lifespan
- R = Functional unit — per user, per transaction, per API call, per request
- The key insight: it's a RATE, not a total. This is what makes it useful for developers.
- A total tells you "your company emitted 500 tons." A rate tells you "this API emits 0.025 gCO₂ per call."
- The rate is what you can actually optimize against sprint over sprint
- Offsets are explicitly excluded — the only way to improve your score is to genuinely reduce emissions
- That's a deliberate design choice and it's the right one

## E — Energy: What We Covered in Parts 1-3, 7-8

- This is where most of the series lives
- Algorithm efficiency (Part 2): O(n²) vs O(n log n) directly impacts energy per operation
- Database optimization (Part 3): N+1 queries, missing indexes, connection pooling — all energy
- Language choice (Part 8): C is 75x more efficient than Python in benchmarks, 2-5x in real I/O-bound services
- ML training (Part 7): pruning, quantization, mixed precision — 10x efficiency gains
- How to actually measure E for your software
  - Cloud provider tools: AWS Customer Carbon Footprint Tool, Azure Emissions Dashboard, GCP Carbon Footprint
  - Direct measurement: CodeCarbon (Python), Scaphandre (Rust/system-level), PowerAPI
  - Estimation when direct measurement isn't possible — TDP-based models
- The hard part: attributing shared infrastructure energy to your specific software
  - Multi-tenant clusters, shared databases, CDNs
  - Allocation approaches: proportional to CPU time, memory, requests, or revenue

## I — Carbon Intensity: What We Covered in Part 4

- Grid carbon intensity varies 12x between Poland (670 gCO₂/kWh) and France (56 gCO₂/kWh)
- Same computation, same result, 12x different carbon cost
- Data sources: Electricity Maps (real-time), WattTime (marginal emissions)
- Time-shifting and geographic shifting — Google got 24% reduction, Microsoft got 16%
- For SCI calculation: use location-based or market-based intensity?
  - Location-based: actual grid mix where your code runs
  - Market-based: accounts for renewable energy purchases (RECs, PPAs)
  - The standard allows both but location-based is more honest for optimization decisions
  - Market-based can mask inefficiency behind certificate purchases

## M — Embodied Emissions: The Part Nobody Thinks About

- Manufacturing a server emits carbon before it ever runs a line of code
- A typical server: 1,000-2,000 kgCO₂ in manufacturing
- Amortized over expected lifespan (typically 4-5 years for servers, 3-4 for laptops)
- For cloud: your share of the hardware's embodied emissions proportional to your usage
- This is why extending hardware life matters — Part 5 touched on this with right-sizing
- Cloud Carbon Footprint tool estimates embodied emissions for major cloud providers
- For most software, M is 10-30% of total SCI — not negligible
- Edge cases where M dominates: low-utilization servers, short-lived hardware, IoT devices
- The honest take: embodied emissions data is still rough. Manufacturers don't publish detailed LCA data. You're working with estimates. That's OK — directionally correct beats precisely wrong.

## R — Functional Unit: The Design Decision That Changes Everything

- This is where teams get stuck and it's the most important choice you make
- R must be meaningful to YOUR software, not generic
  - E-commerce: per transaction, per order
  - API service: per API call, per request
  - Streaming: per minute of video delivered
  - ML inference: per prediction, per batch
  - SaaS: per active user per day
  - CI/CD: per pipeline run, per build
- Why R matters: it determines what "improvement" means
  - If R = per user and you add users, your total emissions go up but your SCI might go down
  - That's the point — you're measuring efficiency, not total impact
  - A growing company with improving SCI is doing the right thing
- Bad R choices: per server (incentivizes fewer, overloaded servers), per year (too aggregated), per line of code (meaningless)
- The test: can a developer look at the SCI score and know what to optimize? If yes, good R. If no, pick again.

## Calculating Your First SCI Score — A Walkthrough

- Pick one application. Not your whole infrastructure. One service.
- Step 1: Define R (functional unit)
  - Example: an internal API that processes document uploads
  - R = per document processed
- Step 2: Measure or estimate E
  - Cloud provider billing data → kWh (AWS, Azure, GCP all expose this now)
  - Or: CPU utilization × TDP × hours = estimated kWh
  - Include networking and storage, not just compute
- Step 3: Get I for your region
  - Electricity Maps API or static annual averages
  - US average: ~400 gCO₂/kWh, EU average: ~230 gCO₂/kWh
- Step 4: Estimate M
  - Cloud Carbon Footprint tool or manual calculation
  - Server embodied emissions / lifespan / your share of utilization
- Step 5: Calculate
  - SCI = ((E × I) + M) / R
  - Example: ((0.5 kWh × 400 gCO₂/kWh) + 2g) / 1000 documents = 0.202 gCO₂/document
- Step 6: Now you have a baseline. Ship it. Track it. Improve it.

- [Code example: Python script that calculates SCI using Cloud Carbon Footprint + Electricity Maps API]
- [Maybe a simple dashboard concept — SCI score per service, trend over time]

## Real-World Case Studies

### Accenture — First Enterprise SCI Implementation
- Measured production application: 0.025 gCO₂ per API call
- 890,000 monthly requests
- Included operational AND embodied emissions
- Key learning: the measurement itself changed how the team thought about optimization

### UBS — Banking Applications
- Applied SCI to two on-premises banking apps (Investment Banking + Asset Management)
- Documented operational emissions, embodied emissions, scaling by functional unit
- One of the first published financial services case studies
- Challenge: on-prem hardware data is harder to get than cloud

### Autostrade per l'Italia — Scale Implementation
- Worked with CAST to measure SCI across 60 applications
- Average 15.1% CO₂ savings per application
- Found that fixing just 10 green code deficiencies with 4 person-days of effort reduced annual CO₂ by ~400 kg and saved 1,000+ kWh/year
- That's the kind of ROI that gets engineering managers' attention

### Texas State University — AI Model Comparison
- Used SCI to evaluate foundation models: GPT-J 6B, GPT-Neo variants, GPT-2
- Found GPT-Neo 1.3B consumed only 27% of GPT-J 6B's energy with comparable output quality
- SCI made the tradeoff visible — you could see exactly what you were paying in carbon for marginal quality improvement

## The CSRD Connection — Why This Matters for Compliance

- EU Corporate Sustainability Reporting Directive (CSRD) requires detailed emissions reporting
- SCI is a complementary tool that supports CSRD compliance
- Not a requirement of ESRS E1, but provides the granularity that ESRS E1 totals can't
- For companies operating in the EU or with EU customers, this is becoming relevant fast
- The Green Software Foundation published specific guidance on SCI-CSRD alignment
- Even if you're not in the EU, your customers might be — and they'll ask about your software's emissions

## What SCI Doesn't Do — Honest Limitations

- Doesn't account for Scope 3 upstream (developer commutes, office energy)
- Embodied emissions data is still rough — manufacturer LCA data is sparse
- Comparing SCI scores across different software types is tricky (an API vs a video encoder)
- The standard is young — tooling is improving but not mature
- Small teams may find the measurement overhead isn't worth it yet
- SCI is a rate — it doesn't tell you total impact. A very efficient service at massive scale still emits a lot.
- The honest take: SCI is the best tool we have, not a perfect one. Use it directionally.

## Tying the Series Together

- Part 1: You learned software has a carbon footprint → SCI gives you the number
- Part 2: You optimized algorithms → that's reducing E
- Part 3: You fixed database queries → that's reducing E
- Part 4: You shifted to cleaner grids → that's reducing I
- Part 5: You right-sized microservices → that's reducing E and M
- Part 6: You optimized CI/CD → that's reducing E per pipeline run
- Part 7: You made ML training efficient → that's reducing E dramatically
- Part 8: You chose the right language → that's reducing E per operation
- Part 9: Now you measure all of it with one score and track it over time

- The series was always building toward this. Every optimization we covered maps to a variable in the SCI equation.

## What to Do Monday

- Week 1: Pick one service. Define R. Get a rough SCI baseline using cloud billing data + regional carbon intensity averages.
- Week 2: Set up automated SCI tracking. Cloud Carbon Footprint + Electricity Maps API. Dashboard it.
- Week 3: Identify the biggest lever. Is it E (code efficiency)? I (region/timing)? M (hardware lifecycle)? Focus there.
- Week 4: Set a reduction target. 10% in 6 months is realistic for most teams. Track it like you track latency or error rates.

## Resources

- Green Software Foundation SCI specification: https://greensoftware.foundation/standards/sci
- ISO/IEC 21031:2024 official page: https://www.iso.org/standard/86612.html
- Impact Framework (open-source SCI calculator): GSF Impact Framework
- Cloud Carbon Footprint: https://www.cloudcarbonfootprint.org/
- Electricity Maps: https://app.electricitymaps.com/
- WattTime: https://www.watttime.org/
- SCI-CSRD compliance guidance: GSF policy research
- Accenture case study, UBS case study, CAST/Autostrade case study — all linked from GSF

---

Target: ~4,000-4,500 words when fully written
Reading time: ~10-12 minutes
