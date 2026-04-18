---
title: "Carbon-Aware Workload Placement: Running Code Where and When the Grid Is Cleanest"
subtitle: "The same computation emits 12x more carbon in Poland than in France. Your scheduler doesn't know that. It should."
series: "Sustainable Software Engineering Part 9 — Series Finale"
reading-time: "10 minutes"
target-audience: "Platform engineers, architects, SREs, DevOps engineers, sustainability leads"
keywords: "carbon-aware computing, workload placement, grid carbon intensity, sustainable software, green coding, carbon-aware scheduling, electricity maps"
tags: "Green Coding, Sustainable Software, Carbon-Aware Computing, Cloud Architecture, DevOps, Climate Tech"
status: "v3-draft"
created: "2026-03-29"
author: "Daniel Stauffer"
---

# Carbon-Aware Workload Placement: Running Code Where and When the Grid Is Cleanest

Part 9 — and the finale — of my series on Sustainable Software Engineering. Last time, we explored [programming language efficiency](link) — when your language choice actually impacts energy consumption and when it doesn't. This time: the biggest lever most teams never pull. Where and when you run code matters as much as how you write it. Follow along for the conclusion of this series.

## The 12x Carbon Gap

Right now, somewhere in your infrastructure, a batch job is running. Maybe it's crunching overnight reports. Maybe it's retraining a model. Maybe it's running your integration test suite for the third time today because someone pushed to main without checking CI.

That job consumes electricity. And here's something that genuinely surprised me when I first dug into the data: the carbon intensity of that electricity varies wildly depending on where and when it runs. At 2 PM in France, the grid runs at roughly 56 gCO₂/kWh — mostly nuclear. At the same moment in Poland, it's 670 gCO₂/kWh — mostly coal. That's not a small difference. That's 12x. For the exact same computation producing the exact same result.

Your scheduler doesn't know any of this. It picks the cheapest region, or the closest one, or whatever region has capacity. Carbon intensity? Not a factor. For most companies, it never has been.

But here's what caught my attention: shifting workloads to cleaner grids is often the single highest-impact change you can make for your software's carbon footprint. Not algorithm optimization. Not language choice. Not right-sizing instances. Just running the same code somewhere else, or at a different time.

Google reported a [24% reduction in carbon emissions](https://blog.google/outreach-initiatives/sustainability/carbon-aware-computing-location/) from carbon-aware load balancing. No code changes. No architecture changes. Just smarter placement. Microsoft hit [16% reduction](https://www.microsoft.com/en-us/research/publication/carbon-aware-computing-for-datacenters/) by time-shifting ML training to low-carbon hours.

Those are big numbers for what amounts to a scheduling change. And almost nobody outside of big tech is doing it yet.

## Why Carbon Intensity Varies

Electricity grids are a mix of generation sources. Some are clean — solar, wind, nuclear, hydro. Some are dirty — coal, natural gas, oil. The mix changes constantly based on demand, weather, time of day, and season.

At noon on a sunny day in California, solar generation peaks and carbon intensity drops to 150-200 gCO₂/kWh. At 7 PM when the sun sets and everyone turns on their air conditioning, natural gas peaker plants fire up and intensity jumps to 400-500 gCO₂/kWh. That's a 2-3x swing within the same region on the same day.

Across regions, the differences are even more dramatic. Iceland runs almost entirely on geothermal and hydro — carbon intensity near zero. Norway is 95%+ hydro. France is 70%+ nuclear. Meanwhile, Poland is 70%+ coal, and parts of India and China run above 700 gCO₂/kWh.

Cloud providers have data centers in all of these regions. When you deploy to `us-east-1` or `eu-west-1`, you're implicitly choosing a carbon intensity. Most teams choose based on latency, cost, and compliance — carbon never enters the equation.

The data to make carbon-aware decisions is freely available. [Electricity Maps](https://app.electricitymaps.com/) provides real-time carbon intensity for grids worldwide. [WattTime](https://www.watttime.org/) provides marginal emissions data for North America and Europe. Cloud providers are starting to expose carbon data directly — Google Cloud's [Carbon Footprint dashboard](https://cloud.google.com/carbon-footprint), AWS's [Customer Carbon Footprint Tool](https://aws.amazon.com/aws-cost-management/aws-customer-carbon-footprint-tool/), and Azure's [Emissions Impact Dashboard](https://www.microsoft.com/en-us/sustainability/emissions-impact-dashboard).

## Three Strategies for Carbon-Aware Placement

There are three levers you can pull: time-shifting, geographic shifting, and demand shaping. Each has different tradeoffs and different levels of implementation complexity.

### Time-Shifting: Run Later When the Grid Is Cleaner

The simplest strategy. Defer non-urgent workloads to hours when carbon intensity is lowest.

Most grids have predictable daily patterns. Solar-heavy grids are cleanest midday. Wind-heavy grids are often cleanest overnight. Coal-heavy grids have less variation but are still cleaner during low-demand hours when peaker plants aren't running.

What to time-shift: batch processing, ML training, CI/CD pipelines, report generation, data backups, ETL jobs, integration tests. Anything that doesn't need to run right now.

What not to time-shift: user-facing requests, real-time APIs, payment processing, alerting, anything with an SLA that requires immediate execution.

```python
import httpx
from datetime import datetime, timedelta

async def get_optimal_run_time(region: str, window_hours: int = 24) -> datetime:
    """Find the lowest carbon intensity hour in the next N hours."""
    response = await httpx.get(
        f"https://api.electricitymap.org/v3/carbon-intensity/forecast",
        params={"zone": region},
        headers={"auth-token": ELECTRICITY_MAPS_TOKEN}
    )
    forecasts = response.json()["forecast"]
    
    # Find the hour with lowest carbon intensity within our window
    cutoff = datetime.utcnow() + timedelta(hours=window_hours)
    valid = [f for f in forecasts if datetime.fromisoformat(f["datetime"]) < cutoff]
    optimal = min(valid, key=lambda f: f["carbonIntensity"])
    
    return datetime.fromisoformat(optimal["datetime"])

# Schedule ML training for the cleanest hour in the next 12 hours
optimal_time = await get_optimal_run_time("US-CAL-CISO", window_hours=12)
scheduler.schedule(train_model, run_at=optimal_time)
```

Microsoft's research team found that time-shifting ML training workloads by just 4-8 hours reduced carbon emissions by 16% with zero impact on model quality or delivery timelines. The training still completed within the same day — it just started at 2 AM instead of 10 AM.

### Geographic Shifting: Run Where the Grid Is Cleanest

Route workloads to the cloud region with the lowest current carbon intensity. This requires multi-region infrastructure but delivers the largest carbon reductions.

The implementation depends on your workload type. For batch jobs, submit to the region with the lowest current intensity. For stateless services, route traffic to the cleanest region that meets latency requirements. For data processing, replicate input data to the cleanest region, process there, and sync results back.

```python
REGIONS = {
    "us-east-1": "US-NY-NYIS",      # New York grid
    "us-west-2": "US-NW-PACW",      # Pacific Northwest (hydro-heavy)
    "eu-west-1": "IE",               # Ireland
    "eu-north-1": "SE",              # Sweden (hydro + nuclear)
    "eu-central-1": "DE",            # Germany
}

async def get_greenest_region(eligible_regions: list[str]) -> str:
    """Select the region with lowest current carbon intensity."""
    intensities = {}
    for aws_region, grid_zone in REGIONS.items():
        if aws_region not in eligible_regions:
            continue
        response = await httpx.get(
            f"https://api.electricitymap.org/v3/carbon-intensity/latest",
            params={"zone": grid_zone},
            headers={"auth-token": ELECTRICITY_MAPS_TOKEN}
        )
        intensities[aws_region] = response.json()["carbonIntensity"]
    
    return min(intensities, key=intensities.get)

# Route batch job to cleanest eligible region
region = await get_greenest_region(["us-east-1", "us-west-2", "eu-north-1"])
submit_batch_job(region=region, job=nightly_etl)
```

The tradeoff is data transfer cost and latency. Cross-region data transfer on AWS costs $0.02/GB. If your batch job processes 1TB of data, that's $20 per run in transfer costs. For most workloads, the carbon savings justify the cost. For data-heavy workloads, you need to do the math.

Google's carbon-intelligent computing platform does this automatically for internal workloads. They shift flexible compute tasks — like YouTube video processing and Gmail spam filtering — to data centers running on cleaner energy. The result: 24% carbon reduction across their fleet with no user-visible impact.

### Demand Shaping: Reduce Load When the Grid Is Dirty

The most sophisticated strategy. Actively reduce your compute footprint during high-carbon periods and increase it during low-carbon periods.

This goes beyond scheduling. It means your system adapts its behavior based on real-time grid conditions. During high-carbon hours, reduce batch sizes, defer non-critical processing, lower cache refresh rates, reduce ML inference quality (use a smaller model), and disable non-essential background jobs. During low-carbon hours, process backlogs, run full-quality inference, refresh all caches, and execute deferred maintenance tasks.

```python
class CarbonAwareScheduler:
    THRESHOLDS = {
        "low": 100,      # gCO2/kWh - run everything
        "medium": 300,    # gCO2/kWh - defer non-critical
        "high": 500,      # gCO2/kWh - essential only
    }
    
    async def should_run(self, job_priority: str) -> bool:
        intensity = await self.get_current_intensity()
        
        if job_priority == "critical":
            return True  # Always run critical jobs
        elif job_priority == "standard":
            return intensity < self.THRESHOLDS["medium"]
        elif job_priority == "deferrable":
            return intensity < self.THRESHOLDS["low"]
        return False
```

This requires classifying your workloads by priority — which is a useful exercise regardless of carbon awareness. Critical workloads (checkout, payments, real-time APIs) always run. Standard workloads (reports, notifications, sync jobs) run during medium or low carbon periods. Deferrable workloads (ML training, backups, analytics) only run during low carbon periods.

## The Tradeoffs Nobody Mentions

Carbon-aware placement isn't free. There are real costs and constraints.

Latency vs. carbon: Geographic shifting adds latency. If your users are in New York and you route their requests to Sweden because the grid is cleaner, response times increase by 80-120ms. For batch jobs, this doesn't matter. For user-facing APIs, it might be unacceptable.

Data residency: GDPR requires EU user data to stay in the EU. HIPAA has its own constraints. Financial regulations may require data to stay in specific jurisdictions. Carbon-aware placement must respect these boundaries — you can optimize within the allowed regions, but you can't ignore compliance.

Complexity: Every strategy adds operational complexity. Time-shifting requires a scheduling system that understands carbon forecasts. Geographic shifting requires multi-region infrastructure. Demand shaping requires workload classification and adaptive behavior. Start with the simplest strategy that delivers meaningful impact.

Cost: Multi-region infrastructure costs more. Data transfer costs money. Carbon-aware scheduling systems need maintenance. For most companies, the cost is modest relative to the carbon savings. But if you're running a small startup with a single-region deployment, the infrastructure investment may not be justified yet.

Measurement uncertainty: Carbon intensity data is an estimate, not a measurement. Grid-level data doesn't account for your specific power purchase agreements. Marginal vs. average intensity gives different answers. The numbers are directionally correct but not precise — which is fine for optimization but not for compliance reporting.

## What This Series Taught Us

Over nine articles, we've covered the full stack of sustainable software engineering.

We started with awareness — understanding that software has a carbon footprint and learning to measure it. We moved to algorithms — the specific code patterns that reduce computational waste by orders of magnitude. We optimized databases — often the biggest energy consumer in any system. We built carbon-aware applications that adapt to grid conditions. We designed sustainable microservices that don't waste energy on network overhead. We greened our DevOps pipelines — the infrastructure that runs thousands of times. We tackled AI/ML — the fastest-growing source of compute carbon. We compared programming languages — understanding when language choice actually matters. And now we've placed workloads where and when the grid is cleanest — the highest-impact lever most teams never pull.

The through-line across all nine articles is this: efficient code is green code. When you optimize for performance, you're usually optimizing for energy efficiency too. The practices that make your software faster, cheaper, and more reliable also make it more sustainable. Green coding isn't a separate discipline — it's good engineering with a carbon lens.

## What to Do Monday Morning

Start with measurement. You can't optimize what you don't measure. Set up carbon tracking for your cloud infrastructure using your provider's carbon dashboard or Cloud Carbon Footprint.

Then pick the lowest-effort, highest-impact strategy. For most teams, that's time-shifting batch jobs. Check your grid's carbon intensity pattern (Electricity Maps is free for personal use), identify your deferrable workloads, and shift them to low-carbon hours. No infrastructure changes required — just a cron job adjustment.

If you're already multi-region, add carbon intensity as a factor in your routing decisions. Even a simple "prefer the cleaner region when latency difference is under 50ms" rule can reduce emissions by 10-20%.

The goal isn't perfection. It's progress. A 10% reduction in carbon emissions across your infrastructure is meaningful. A 24% reduction — like Google achieved — is transformative. And it starts with the same question we've been asking throughout this series: where is the waste, and how do we eliminate it?

Your code runs on electricity. That electricity has a carbon cost. Now you know how to minimize it.

---

**Resources**:
- [Electricity Maps — Real-Time Carbon Intensity](https://app.electricitymaps.com/)
- [WattTime — Marginal Emissions Data](https://www.watttime.org/)
- [Google: Carbon-Aware Computing](https://blog.google/outreach-initiatives/sustainability/carbon-aware-computing-location/)
- [Microsoft: Carbon-Aware Datacenters](https://www.microsoft.com/en-us/research/publication/carbon-aware-computing-for-datacenters/)
- [Green Software Foundation](https://greensoftware.foundation/)
- [Cloud Carbon Footprint — Open Source Tool](https://www.cloudcarbonfootprint.org/)
- [AWS Customer Carbon Footprint Tool](https://aws.amazon.com/aws-cost-management/aws-customer-carbon-footprint-tool/)

---

## Series Navigation

**Previous Article**: [Programming Language Efficiency Deep Dive: Choosing the Right Tool for the Job](link) *(Part 8)*

**This is the final article in the Sustainable Software Engineering series.** Thank you for following along through all nine parts. If you found this series valuable, the best thing you can do is apply one practice from each article — that's nine changes that compound into meaningful impact.

---

*This is Part 9 and the finale of the Sustainable Software Engineering series. Read the full series: [Part 1: Why Your Code's Carbon Footprint Matters](link), [Part 2: Energy-Efficient Algorithm Patterns](link), [Part 3: Database Optimization Strategies](link), [Part 4: Building Carbon-Aware Applications](link), [Part 5: Sustainable Microservices Architecture](link), [Part 6: Green DevOps Practices](link), [Part 7: Sustainable AI/ML and MLOps](link), and [Part 8: Programming Language Efficiency Deep Dive](link).*

**About the Author**: Daniel Stauffer is an Enterprise Architect who believes efficient code and sustainable code are the same thing. He designs systems that are fast, cheap, reliable, and low-carbon — because those goals are more aligned than most people think.

**Tags**: #GreenCoding #SustainableSoftware #CarbonAwareComputing #CloudArchitecture #DevOps #ClimateTech #ElectricityMaps #SoftwareEngineering #Sustainability
