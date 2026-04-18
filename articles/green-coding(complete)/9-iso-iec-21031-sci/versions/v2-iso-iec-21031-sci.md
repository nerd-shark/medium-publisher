---
title: "ISO/IEC 21031: Measuring Your Software's Carbon Footprint With One Number"
subtitle: "You've optimized algorithms, picked efficient languages, and shifted workloads to cleaner grids. Now there's an ISO standard that scores all of it. Here's how to actually use it."
series: "Sustainable Software Engineering Part 9 — Series Finale"
reading-time: "10-12 minutes"
target-audience: "Software architects, platform engineers, engineering managers, sustainability leads"
keywords: "ISO 21031, SCI, software carbon intensity, green software foundation, carbon measurement, sustainable software, green coding"
tags: "Green Coding, Sustainable Software, ISO Standards, Carbon Measurement, Software Architecture"
status: "v2-detailed-outline"
created: "2026-04-01"
updated: "2026-04-01"
author: "Daniel Stauffer"
changelog: "v2 - Detailed outline with rough draft prose. Fleshed out opening hook, formula breakdown, and walkthrough. Some sections still in bullets, others in rough prose."
---

# ISO/IEC 21031: Measuring Your Software's Carbon Footprint With One Number

Part 9 — and the finale — of my series on Sustainable Software Engineering. Last time, we explored programming language efficiency — when your language choice actually impacts energy consumption and when it doesn't. This time: the standard that ties everything together. Follow along for the conclusion of this series.

---

## The Reporting Problem

Over the past eight articles, we've covered a lot of ground. Algorithm optimization. Database efficiency. Carbon-aware computing. CI/CD pipelines. ML training. Language selection. Microservice architecture. All of it reduces the carbon your software emits.

But here's the question I keep getting asked: how do you know it's working?

Your cloud bill dropped after you right-sized those containers. Great. Your latency improved after you fixed the N+1 queries. Wonderful. But did your carbon footprint actually go down? By how much? Compared to what?

Most companies can't answer that. The GHG Protocol gives you annual Scope 2 totals — useful for sustainability reports, useless for engineering decisions. A CTO can quote the company's total emissions but can't tell a developer whether the code they shipped last sprint was better or worse for the climate than the version before it.

[This is the gap. The optimizations work. The measurement doesn't exist. Or didn't, until March 2024.]

ISO/IEC 21031:2024 — the Software Carbon Intensity specification — fills that gap. One formula. One score. Per functional unit of your software. Developed by the Green Software Foundation, it achieved ISO status in under three years, which is fast — the typical timeline is five to seven. It's already being used by Accenture, UBS, NTT DATA, Microsoft, and Autostrade per l'Italia.

The rest of this article is about how to actually use it.

---

## The Formula

The entire standard fits in one equation:

**SCI = (E × I + M) per R**

That's it. Four variables. Let me break them down.

**E** is the energy your software consumes, measured in kilowatt-hours. This includes compute (CPU, GPU), storage, networking, and — if you want to be thorough — end-user devices. This is where most of the series lives. Every algorithm optimization from Part 2, every database fix from Part 3, every ML efficiency gain from Part 7 — all of that reduces E.

**I** is the carbon intensity of that energy, measured in grams of CO₂ per kilowatt-hour. This varies wildly by location and time. France at 56 gCO₂/kWh (mostly nuclear) versus Poland at 670 gCO₂/kWh (mostly coal) — that's a 12x difference for the same computation. Part 4 covered this in detail.

**M** is embodied emissions — the carbon emitted manufacturing the hardware your software runs on, amortized over its expected lifespan. A typical server produces 1,000-2,000 kgCO₂ during manufacturing. Spread that over 4-5 years and your share of utilization, and you get M. For most software, M is 10-30% of total SCI. Not negligible.

**R** is the functional unit — the thing you're measuring per. Per API call. Per transaction. Per user per day. Per document processed. This is the design decision that makes SCI useful for developers. It turns a total into a rate, and a rate is something you can optimize against sprint over sprint.

Two things worth noting. First, SCI is a rate, not a total. A total tells you "your company emitted 500 tons." A rate tells you "this API emits 0.025 gCO₂ per call." The rate is actionable. Second, offsets are explicitly excluded. The only way to improve your SCI score is to genuinely reduce emissions. That's a deliberate design choice and I think it's the right one.

---

## Measuring E — Energy Consumption

[This section needs more detail on practical measurement approaches]

The energy component is the one most teams can actually influence directly. Three approaches, from easiest to most accurate:

**Cloud provider tools** — AWS Customer Carbon Footprint Tool, Azure Emissions Impact Dashboard, GCP Carbon Footprint. These give you kWh data at the account or project level. Easy to get, but coarse-grained. You know your total energy, not which service consumed what.

**Direct measurement tools** — CodeCarbon (Python library, wraps your code and measures energy), Scaphandre (Rust-based, system-level power monitoring), PowerAPI (middleware approach). These give you per-process or per-function energy data. More accurate, more setup.

**TDP-based estimation** — When you can't measure directly: CPU utilization × Thermal Design Power × hours = estimated kWh. Rough but better than nothing. Works for on-prem where you don't have cloud provider dashboards.

The hard part is attribution. Your service runs on a shared Kubernetes cluster with 40 other services, a shared PostgreSQL instance, and a CDN. How much of the cluster's energy is yours? Allocation approaches: proportional to CPU time, memory usage, request count, or revenue. None are perfect. Pick one, be consistent, document it.

[Need a code example here — maybe CodeCarbon wrapping a function]

---

## Carbon Intensity — The I Variable

Covered this extensively in Part 4, so I'll keep it brief here.

Grid carbon intensity varies by location (12x between Poland and France) and by time of day (2-3x swing in California between solar peak and evening gas peakers). Data sources: Electricity Maps for real-time global data, WattTime for marginal emissions in North America and Europe.

For SCI calculation, you need to decide: location-based or market-based intensity?

Location-based uses the actual grid mix where your code runs. Market-based accounts for renewable energy purchases — RECs, PPAs, green tariffs. The standard allows both. My take: use location-based for optimization decisions. Market-based can mask inefficiency behind certificate purchases. If you buy RECs but your code is still wasteful, your location-based SCI will tell you that. Your market-based SCI won't.

[Maybe a small table: region → typical carbon intensity → what it means for SCI]

---

## Embodied Emissions — The M Nobody Thinks About

This is the variable most teams skip, and they shouldn't.

Manufacturing a server emits carbon before it ever runs a line of code. The mining, refining, fabrication, assembly, shipping — all of it has a carbon cost. A typical rack server: 1,000-2,000 kgCO₂. A laptop: 300-400 kgCO₂. A smartphone: 50-80 kgCO₂.

For cloud workloads, your M is your share of the hardware's embodied emissions, proportional to your utilization. If you use 5% of a server's capacity over its 4-year lifespan, you own 5% of its embodied emissions.

Cloud Carbon Footprint estimates this for AWS, Azure, and GCP. For on-prem, you'll need to dig into manufacturer specs or use industry averages.

The honest take: embodied emissions data is still rough. Most manufacturers don't publish detailed lifecycle assessment data. You're working with estimates and industry averages. That's OK. Directionally correct beats precisely wrong. And for most software, getting E and I right matters more than perfecting M.

Edge cases where M dominates: low-utilization servers (you own a big share of embodied emissions for little compute), short-lived hardware (less time to amortize), IoT devices (tiny energy use, significant manufacturing footprint per unit).

---

## Choosing R — The Decision That Changes Everything

This is where teams get stuck, and it's the most important choice you make.

R must be meaningful to your software. Not generic. Not abstract. Something a developer can look at and know what to optimize.

Good R choices by software type:
- E-commerce platform: per transaction or per order
- API service: per API call or per request
- Video streaming: per minute of video delivered
- ML inference service: per prediction or per batch
- SaaS application: per active user per day
- CI/CD pipeline: per pipeline run or per build

Bad R choices:
- Per server (incentivizes fewer, overloaded servers — gaming the metric)
- Per year (too aggregated, same problem as GHG Protocol totals)
- Per line of code (meaningless — more code doesn't mean more emissions)

Why R matters so much: it determines what "improvement" means. If R = per user and you add users, your total emissions go up but your SCI might go down. That's the point. You're measuring efficiency, not total impact. A growing company with an improving SCI score is doing the right thing — serving more people with less carbon per person.

The test I use: hand the SCI score to a developer on the team. Can they look at it and know what to optimize? If yes, good R. If they shrug, pick again.

---

## Calculating Your First SCI Score

Pick one application. Not your whole infrastructure. Not your entire platform. One service. The simpler the better for your first attempt.

I'll walk through an example: an internal API that processes document uploads. About 30,000 documents per month.

**Step 1: Define R.** Per document processed. Simple, meaningful, trackable.

**Step 2: Measure E.** Pull cloud billing data for the service's compute, storage, and networking. Let's say it's 150 kWh/month total. That's 0.005 kWh per document (150 / 30,000).

**Step 3: Get I.** The service runs in us-east-1. Annual average carbon intensity for the PJM grid: ~380 gCO₂/kWh. Use Electricity Maps or WattTime for more precise data.

**Step 4: Estimate M.** The service runs on 2 EC2 instances. Cloud Carbon Footprint estimates embodied emissions at ~0.8 kgCO₂/month for your share. That's 0.027g per document (800g / 30,000).

**Step 5: Calculate.**

SCI = ((E × I) + M) / R
SCI = ((0.005 kWh × 380 gCO₂/kWh) + 0.027g) / 1 document
SCI = (1.9 + 0.027) / 1
SCI = 1.927 gCO₂ per document

**Step 6: Now you have a baseline.** Ship it. Track it monthly. Set a reduction target.

[Need to add: Python code that automates this using Electricity Maps API + cloud billing data]
[Maybe: a simple tracking spreadsheet or dashboard concept]

Notice that E × I dominates (1.9g) and M is small (0.027g). That tells you where to focus: reduce energy consumption or move to a cleaner region. Extending hardware life won't move the needle much for this particular service.

---

## Real-World Case Studies

### Accenture — First Enterprise SCI Implementation

Accenture was one of the first organizations to calculate an SCI score for a production application. The result: 0.025 gCO₂ per API call across 890,000 monthly requests. They included both operational and embodied emissions.

The interesting part wasn't the number itself — it was what happened after. The team started thinking about optimization differently. Instead of "make it faster," the conversation became "make it more efficient per call." The SCI gave them a metric that connected code changes to environmental impact in a way that annual carbon reports never could.

[Need to verify: is the Accenture case study publicly available with enough detail to cite?]

### UBS — Banking Applications

UBS applied SCI to two on-premises banking applications — one in Investment Banking, one in Asset Management. They documented operational emissions, embodied emissions, and scaled by functional unit.

The challenge with on-prem: hardware data is harder to get than cloud. No dashboard tells you your server's energy consumption. They had to work with facilities teams to get power data and estimate allocation. It's doable but requires cross-team coordination that cloud-native teams don't need.

[One of the first published financial services case studies — important for credibility with enterprise audience]

### Autostrade per l'Italia — Scale Implementation

This is the one that gets engineering managers' attention. Working with CAST, Autostrade measured SCI across 60 applications. Average result: 15.1% CO₂ savings per application.

The kicker: fixing just 10 green code deficiencies with 4 person-days of effort reduced annual CO₂ by an estimated 400 kg and saved over 1,000 kWh per year. Per application. Across 60 applications, that adds up fast.

4 person-days. 400 kg CO₂. 1,000 kWh. That's the kind of ROI that doesn't need a sustainability argument — it's just good engineering.

### Texas State University — AI Model Comparison

Researchers used SCI to evaluate foundation AI models: GPT-J 6B, GPT-Neo variants, GPT-2. The finding: GPT-Neo 1.3B consumed only 27% of GPT-J 6B's energy while producing comparable output quality.

SCI made the tradeoff visible in a way that accuracy benchmarks alone couldn't. You could see exactly what you were paying in carbon for each marginal improvement in model quality. For teams choosing between models, that's actionable information.

[This connects directly to Part 7 — sustainable AI/ML. Nice series callback.]

---

## The CSRD Connection

[This section needs to be concise — compliance angle, not a deep dive on EU regulation]

The EU Corporate Sustainability Reporting Directive (CSRD) requires detailed emissions reporting from companies operating in or selling to the EU. SCI isn't a requirement of ESRS E1 (the climate standard within CSRD), but it provides the granularity that ESRS E1 totals can't.

Think of it this way: CSRD asks "what are your total emissions?" SCI answers "here's the emissions rate per unit of software output, and here's how we're reducing it." The first satisfies compliance. The second drives engineering action.

The Green Software Foundation published specific guidance on SCI-CSRD alignment. Even if your company isn't directly subject to CSRD, your customers might be — and they'll increasingly ask about the carbon footprint of the software they're buying.

---

## What SCI Doesn't Do

I want to be honest about the limitations because overselling a standard is worse than not having one.

SCI doesn't account for Scope 3 upstream emissions — developer commutes, office energy, the carbon cost of the meetings where you argued about architecture. It's focused on the software itself.

Embodied emissions data is still rough. Manufacturers don't publish detailed lifecycle assessment data for most hardware. You're working with estimates and industry averages. The standard acknowledges this.

Comparing SCI scores across fundamentally different software types is tricky. An API that serves JSON responses and a video encoder that transcodes 4K streams have very different energy profiles. Comparing their SCI scores isn't apples to apples, even if both use "per request" as R.

The standard is young. Tooling is improving but not mature. The Impact Framework helps, but you'll still spend time wrangling data from multiple sources.

For small teams with a handful of services, the measurement overhead might not be worth it yet. Start with the biggest, most resource-intensive service and expand from there.

And SCI is a rate — it doesn't tell you total impact. A very efficient service running at massive scale still emits a lot of carbon in absolute terms. SCI tells you you're efficient. It doesn't tell you you're small.

The honest take: SCI is the best tool we have for measuring software carbon intensity. It's not perfect. Use it directionally, improve your data quality over time, and don't let perfect be the enemy of good.

---

## Tying the Series Together

This is the part I've been wanting to write since Part 1.

Every article in this series maps to a variable in the SCI equation:

- **Part 1** (Why Your Code's Carbon Footprint Matters): You learned software has a carbon footprint → SCI gives you the number
- **Part 2** (Energy-Efficient Algorithm Patterns): You optimized algorithms → that's reducing **E**
- **Part 3** (Database Optimization Strategies): You fixed database queries → that's reducing **E**
- **Part 4** (Building Carbon-Aware Applications): You shifted to cleaner grids → that's reducing **I**
- **Part 5** (Sustainable Microservices Architecture): You right-sized microservices → that's reducing **E** and **M**
- **Part 6** (Green DevOps Practices): You optimized CI/CD → that's reducing **E** per pipeline run
- **Part 7** (Sustainable AI/ML): You made ML training efficient → that's reducing **E** dramatically
- **Part 8** (Programming Language Efficiency): You chose the right language → that's reducing **E** per operation
- **Part 9** (This article): Now you measure all of it with one score and track it over time

The series was always building toward this. Every optimization we covered is a lever on one of the SCI variables. The standard gives you a way to measure whether pulling those levers is actually working.

---

## What to Do Monday

Week 1: Pick one service. Define R. Get a rough SCI baseline using cloud billing data and regional carbon intensity averages. Don't overthink it — a rough number is infinitely better than no number.

Week 2: Set up automated SCI tracking. Cloud Carbon Footprint for energy and embodied emissions. Electricity Maps API for carbon intensity. Put it in a dashboard next to your latency and error rate metrics.

Week 3: Identify the biggest lever. Is it E (code efficiency)? I (region or timing)? M (hardware lifecycle)? The SCI breakdown tells you where to focus. Don't optimize everything at once.

Week 4: Set a reduction target. 10% in 6 months is realistic for most teams. Track it like you track any other engineering metric. Review it in sprint retros.

---

## Resources

- [Green Software Foundation — SCI Specification](https://greensoftware.foundation/standards/sci)
- [ISO/IEC 21031:2024 — Official ISO Page](https://www.iso.org/standard/86612.html)
- [Impact Framework — Open-Source SCI Calculator](https://if.greensoftware.foundation/)
- [Cloud Carbon Footprint](https://www.cloudcarbonfootprint.org/)
- [Electricity Maps](https://app.electricitymaps.com/)
- [WattTime](https://www.watttime.org/)
- [SCI-CSRD Compliance Guidance](https://greensoftware.foundation/policy/research/sci-csrd-compliance/)
- [Accenture SCI Case Study](https://greensoftware.foundation/stories/sci-measurement/)

---

Target: ~4,000-4,500 words when fully written
Reading time: ~10-12 minutes
