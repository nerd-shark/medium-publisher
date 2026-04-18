---
document-title: Green Coding Series
document-subtitle: Building Carbon-Aware Applications
document-type: Medium Article Draft
document-date: 2025-02-08
document-revision: 1.0
document-author: Daniel Stauffer
author-email: daniel_stauffer@jabil.com
author-org: Enterprise Architecture
review-cycle: Per Article
---
# Building Carbon-Aware Applications: When and Where You Run Code Matters as Much as How You Write It

*This is Part 4 of my series on Sustainable Software Engineering. Last time, we explored database optimization strategies that cut energy costs and cloud bills. This time: building carbon-aware applications that adapt to grid conditions—when and where you run code matters as much as how you write it. Follow along for more deep dives into green coding practices.*

Here's something that'll mess with your head: The same code, running on the same hardware, can have a 10x difference in carbon emissions depending on when and where you run it.

Not 10%. Ten times.

I'm not talking about optimizing algorithms or database queries (we covered that in Parts 2 and 3). I'm talking about the electrical grid itself—the mix of coal, natural gas, solar, wind, and hydro that powers your data center at any given moment.

At 3 PM on a sunny day in California, your code might be running on 60% solar power. At 3 AM, it's probably running on natural gas. In Norway, it's almost always hydro. In India, it's mostly coal.

Same code. Wildly different carbon footprint.

This is carbon-aware computing: building applications that adapt their behavior based on the real-time cleanliness of the electrical grid.

## The Grid Isn't Static

Most engineers think about electricity like water from a tap—it's just there when you need it, always the same. But the electrical grid is more like a recipe that changes every hour.

Right now, as you're reading this, the grid in your region is some mix of:

- **Coal**: ~900-1000 gCO₂/kWh (grams of CO2 per kilowatt-hour)
- **Natural Gas**: ~400-500 gCO₂/kWh
- **Solar**: ~40-50 gCO₂/kWh
- **Wind**: ~10-15 gCO₂/kWh
- **Hydro**: ~10-20 gCO₂/kWh
- **Nuclear**: ~10-15 gCO₂/kWh

The mix changes constantly based on demand, weather, and what power plants are online. Solar peaks at noon. Wind is often strongest at night. Coal plants run 24/7 because they're expensive to start and stop.

This means the carbon intensity of the grid—measured in gCO₂/kWh—varies dramatically:

- **Norway**: 20-30 gCO₂/kWh (mostly hydro)
- **France**: 50-80 gCO₂/kWh (mostly nuclear)
- **California**: 200-600 gCO₂/kWh (varies by time of day)
- **Virginia**: 300-500 gCO₂/kWh (coal and natural gas)
- **India**: 600-900 gCO₂/kWh (mostly coal)

If you're running workloads in AWS us-east-1 (Virginia) at 3 AM, you're probably burning coal. If you could shift that same workload to 2 PM, you'd catch some solar. If you could route it to AWS eu-north-1 (Stockholm), you'd get hydro and wind.

Same workload. 5-10x difference in carbon emissions.

## The Three Dimensions of Carbon-Aware Computing

Carbon-aware applications adapt along three dimensions:

### 1. When: Time-Shifting Workloads

Not all work needs to happen right now. Batch processing, ML model training, data backups, report generation—these can often wait for cleaner hours.

**Example**: You're training a machine learning model. It'll take 6 hours regardless of when you start it. You could start it at 5 PM (peak demand, dirty grid) or at 2 AM (low demand, cleaner grid).

In California, starting at 2 AM instead of 5 PM could reduce carbon emissions by 40-60% because you're avoiding the evening natural gas peak (when everyone gets home and turns on appliances) and catching the overnight wind power that's often abundant.

**The Pattern**:

```python
import requests
from datetime import datetime, timedelta

def get_carbon_intensity(region="US-CAL-CISO"):
    """Fetch current carbon intensity from Electricity Maps API"""
    response = requests.get(
        f"https://api.electricitymap.org/v3/carbon-intensity/latest",
        params={"zone": region},
        headers={"auth-token": "YOUR_API_KEY"}
    )
    return response.json()["carbonIntensity"]

def should_start_training():
    """Decide if now is a good time to start training"""
    current_intensity = get_carbon_intensity()
  
    # Only start if carbon intensity is below threshold
    THRESHOLD = 300  # gCO₂/kWh
  
    if current_intensity < THRESHOLD:
        return True
  
    # Otherwise, check if we're approaching a clean period
    # (e.g., solar peak at noon, wind peak at night)
    hour = datetime.now().hour
    if 10 <= hour <= 14:  # Solar peak approaching
        return True
    if 22 <= hour or hour <= 4:  # Wind peak
        return True
  
    return False

# In your batch job scheduler
if should_start_training():
    start_ml_training()
else:
    schedule_for_later()
```

### 2. Where: Geographic Workload Shifting

If you're running multi-region infrastructure, you can route workloads to regions with cleaner grids.

**Example**: You're encoding videos for a streaming service. The work can happen anywhere—users don't care which data center processes their upload.

You could route encoding jobs to:

- **Quebec (AWS ca-central-1)**: 20-30 gCO₂/kWh (hydro)
- **Stockholm (AWS eu-north-1)**: 30-50 gCO₂/kWh (hydro + wind)
- **Virginia (AWS us-east-1)**: 300-500 gCO₂/kWh (coal + gas)

Routing to Quebec instead of Virginia reduces carbon emissions by 90%.

**The Pattern**:

```python
def select_encoding_region():
    """Choose the cleanest available region for video encoding"""
    regions = {
        "ca-central-1": get_carbon_intensity("CA-QC"),
        "eu-north-1": get_carbon_intensity("SE"),
        "us-east-1": get_carbon_intensity("US-VA"),
        "us-west-2": get_carbon_intensity("US-CAL-CISO")
    }
  
    # Sort by carbon intensity (cleanest first)
    sorted_regions = sorted(regions.items(), key=lambda x: x[1])
  
    # Check capacity and latency constraints
    for region, intensity in sorted_regions:
        if has_capacity(region) and meets_latency_sla(region):
            return region
  
    # Fallback to default region
    return "us-east-1"

# Route encoding job to cleanest region
region = select_encoding_region()
submit_encoding_job(video_id, region)
```

### 3. What: Workload Prioritization

When the grid is dirty, you can reduce or defer non-critical work.

**Example**: You're running a recommendation engine. During high-carbon periods, you could:

- Serve cached recommendations instead of computing fresh ones
- Use a simpler (faster, less carbon-intensive) model
- Reduce recommendation quality slightly
- Skip personalization for anonymous users

Users get slightly less personalized recommendations during peak carbon hours, but the service stays fast and you cut carbon emissions by 30-50%.

**The Pattern**:

```python
def get_recommendations(user_id, context):
    """Get recommendations with carbon-aware quality adjustment"""
    intensity = get_carbon_intensity()
  
    # High carbon: use cached or simple recommendations
    if intensity > 500:
        return get_cached_recommendations(user_id)
  
    # Medium carbon: use fast model
    elif intensity > 300:
        return get_fast_recommendations(user_id, context)
  
    # Low carbon: use full personalization
    else:
        return get_personalized_recommendations(user_id, context)
```

## Carbon-Aware Kubernetes

If you're running Kubernetes, you can build carbon-awareness into your scheduling decisions.

**The Idea**: Schedule pods on nodes in regions with cleaner grids. When carbon intensity is high, scale down non-critical workloads.

**Tools**:

- **KEDA (Kubernetes Event-Driven Autoscaling)**: Scale based on external metrics (like carbon intensity)
- **Carbon-Aware KEDA Operator**: Open-source operator that scales workloads based on grid carbon intensity
- **Custom Schedulers**: Write your own scheduler that considers carbon intensity

**Example with KEDA**:

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: carbon-aware-batch-processor
spec:
  scaleTargetRef:
    name: batch-processor
  minReplicaCount: 0
  maxReplicaCount: 10
  triggers:
  - type: external
    metadata:
      scalerAddress: carbon-intensity-scaler:8080
      threshold: "300"  # gCO₂/kWh
      query: "US-CAL-CISO"
```

When carbon intensity drops below 300 gCO₂/kWh, KEDA scales up your batch processor. When it rises above 300, KEDA scales it back down.

## Real-World Example: ML Training at Microsoft

Microsoft's Azure team implemented carbon-aware scheduling for their internal ML training workloads.

**The Setup**:

- ML models that take 6-12 hours to train
- Multi-region infrastructure (US, Europe, Asia)
- Real-time carbon intensity data from WattTime API

**The Strategy**:

1. **Time-shift**: Defer training to low-carbon hours (night for wind, noon for solar)
2. **Geo-shift**: Route training jobs to regions with cleanest grids
3. **Prioritize**: Critical models train immediately, experimental models wait for clean hours

**The Results**:

- **16% reduction** in carbon emissions for ML training workloads
- **No impact** on model quality or delivery timelines
- **Minimal complexity**: Carbon-aware scheduler integrated with existing job queue

The key insight: Most ML training isn't urgent. Waiting 4-6 hours for cleaner grid conditions is acceptable, and the carbon savings are substantial.

## How to Measure Carbon Intensity (The Basics)

Before you can build carbon-aware applications, you need to understand how carbon intensity is actually measured.

### Location-Based vs Market-Based Accounting

There are two ways to measure the carbon intensity of electricity:

**Location-Based**: What's actually on the grid right now

- Measures the real-time mix of power sources (coal, gas, solar, wind)
- Changes every 5-15 minutes based on supply and demand
- This is what carbon-aware applications use for real-time decisions
- Example: California grid at 2 PM might be 40% solar, 30% natural gas, 20% hydro, 10% imports

**Market-Based**: What you've purchased through contracts

- Based on Power Purchase Agreements (PPAs) and Renewable Energy Certificates (RECs)
- Doesn't change in real-time
- Used for annual carbon reporting and compliance
- Example: Your company bought RECs for 100% renewable energy, so you report 0 gCO₂/kWh

**For carbon-aware computing, use location-based**. Market-based accounting is for reporting, not for real-time optimization.

### The Three Scopes of Carbon Emissions

When measuring software carbon emissions, you'll hear about "scopes":

**Scope 1**: Direct emissions you control

- Your company's generators, vehicles, facilities
- Usually not relevant for software

**Scope 2**: Indirect emissions from purchased electricity

- The electricity your data center or cloud provider uses
- **This is what carbon-aware computing optimizes**
- Measured in gCO₂/kWh

**Scope 3**: Everything else in your value chain

- Embodied carbon in hardware (manufacturing, shipping)
- Employee commutes, business travel
- End-user device energy consumption
- Much harder to measure and optimize

**For carbon-aware applications, focus on Scope 2**. It's the biggest lever you can pull in real-time.

### Marginal vs Average Carbon Intensity

Here's a nuance that matters:

**Average Carbon Intensity**: The average gCO₂/kWh of all power on the grid

- Example: Grid is 50% coal (900 gCO₂/kWh) + 50% solar (40 gCO₂/kWh) = 470 gCO₂/kWh average

**Marginal Carbon Intensity**: The gCO₂/kWh of the *next* unit of power added to the grid

- When demand increases, which power plant turns on?
- Usually natural gas (400-500 gCO₂/kWh) or coal (900-1000 gCO₂/kWh)
- Solar and wind can't "turn on" - they're already running at capacity

**Why this matters**: When you run a workload, you're adding demand to the grid. The marginal power source is what actually powers your workload, not the average.

Most carbon intensity APIs report average intensity because marginal is harder to calculate. For practical carbon-aware computing, average is good enough—the trends are what matter (cleaner at noon, dirtier at 6 PM).

### ISO 21031: The Emerging Standard

There's an emerging international standard for measuring software carbon intensity: **ISO/IEC 21031** (Software Carbon Intensity Specification).

**What it defines**:

- How to measure software carbon emissions
- How to calculate carbon per functional unit (e.g., per API request, per video encoded)
- How to report and compare carbon intensity across applications

**Why it matters**: Standardized measurement means you can compare carbon intensity across teams, companies, and industries.

We'll dive deep into ISO 21031 in a future article. For now, know that it exists and it's becoming the standard for measuring software carbon emissions.

## Measuring Impact

How do you know if carbon-aware computing is working?

**Metrics to Track**:

1. **Carbon Intensity**: Average gCO₂/kWh for your workloads
2. **Carbon Emissions**: Total kg CO₂ per day/week/month
3. **Workload Shifts**: Percentage of jobs time-shifted or geo-shifted
4. **Carbon Savings**: Emissions avoided compared to baseline

**Example Dashboard**:

```
Carbon-Aware Batch Processing
------------------------------
Current Carbon Intensity: 245 gCO₂/kWh (California)
Status: RUNNING (below threshold)

Today's Stats:
- Jobs Completed: 1,247
- Jobs Time-Shifted: 412 (33%)
- Jobs Geo-Shifted: 89 (7%)
- Carbon Saved: 127 kg CO2 (vs baseline)

This Week:
- Total Carbon Emissions: 2,340 kg CO2
- Carbon Savings: 890 kg CO2 (27% reduction)
- Average Carbon Intensity: 287 gCO₂/kWh
```

## The Tradeoffs (Let's Be Honest)

Carbon-aware computing isn't free. Here's what you're trading:

### Increased Complexity

You're adding another dimension to your scheduling logic. More code, more monitoring, more things that can break.

**When it's worth it**: Batch processing, ML training, data pipelines—workloads that can tolerate delays.

**When it's not**: Real-time APIs, user-facing services, anything latency-sensitive.

### Latency Implications

Geographic shifting adds latency. Routing a job from Virginia to Quebec adds 20-30ms. For batch jobs, that's nothing. For API calls, that might violate your SLA.

**When it's worth it**: Async workloads, background jobs, anything where users don't notice.

**When it's not**: Synchronous APIs, real-time processing, anything user-facing.

### Data Availability

Carbon intensity data isn't perfect. APIs can be down, data can be stale, coverage varies by region.

**Mitigation**: Cache data, have fallback strategies, don't make carbon-awareness a hard requirement.

### Cost Implications

Multi-region infrastructure costs more. Data transfer between regions costs more. You're trading carbon for dollars.

**When it's worth it**: When carbon reduction is a business priority, when you're already multi-region.

**When it's not**: When you're optimizing for cost above all else.

## When NOT to Use Carbon-Aware Patterns

Let's be clear about when this doesn't make sense:

1. **User-facing APIs**: Don't add latency to user requests for carbon savings
2. **Real-time processing**: Don't delay time-sensitive workloads
3. **Single-region deployments**: Geographic shifting requires multi-region infrastructure
4. **Small workloads**: The overhead isn't worth it for tiny jobs
5. **Cost-constrained environments**: Multi-region and data transfer costs add up

Carbon-aware computing is for workloads that are:

- **Deferrable**: Can wait hours for cleaner grid conditions
- **Location-flexible**: Can run in any region
- **Large enough**: Carbon savings justify the complexity
- **Non-user-facing**: Users don't notice delays

## Resources and Tools

**Carbon Intensity APIs**:

- **Electricity Maps**: Real-time carbon intensity for 200+ regions
- **WattTime**: Grid carbon data with forecasting
- **Carbon Intensity API (UK)**: Free API for UK grid data

**Open Source Tools**:

- **Carbon-Aware KEDA Operator**: Kubernetes autoscaling based on carbon intensity
- **Carbon-Aware SDK**: Microsoft's SDK for carbon-aware applications
- **Green Software Foundation**: Standards and best practices

**Cloud Provider Data**:

- **Google Cloud Carbon Footprint**: Per-project carbon emissions
- **AWS Customer Carbon Footprint Tool**: Account-level carbon tracking
- **Azure Carbon Optimization**: Carbon intensity data for Azure regions

## What's Next

In Part 5, we'll look at **Sustainable Microservices Architecture**—how to design service meshes and distributed systems that minimize carbon emissions through intelligent routing, caching, and resource optimization.

We'll cover:

- Service mesh carbon optimization
- Intelligent caching strategies
- Request routing for carbon efficiency
- Distributed tracing for carbon hotspots

Carbon-aware computing is just one piece of the green coding puzzle. Combined with efficient algorithms (Part 2), optimized databases (Part 3), and sustainable architecture (Part 5), you can build systems that are both performant and planet-friendly.

## The Bottom Line

Your code doesn't run in a vacuum—it runs on an electrical grid that's constantly changing. By making your applications aware of that grid's carbon intensity, you can reduce emissions by 20-50% without sacrificing functionality.

Time-shift batch jobs to clean hours. Route workloads to clean regions. Prioritize critical work during dirty hours. It's not rocket science, but it does require thinking about when and where your code runs, not just how it runs.

The grid is getting cleaner every year as more renewables come online. But until we're at 100% clean energy, carbon-aware computing is one of the most impactful things you can do to reduce your software's environmental footprint.

**Question for you**: What workloads in your system could be time-shifted to cleaner hours? What would it take to implement carbon-aware scheduling?

---

## References

### Carbon Intensity Data Sources

1. **Electricity Maps** - Real-time carbon intensity data by region

   - https://app.electricitymaps.com/
   - Source for regional carbon intensity ranges (Norway, France, California, Virginia, India)
2. **U.S. Energy Information Administration (EIA)** - Carbon dioxide emissions coefficients

   - https://www.eia.gov/environment/emissions/co2_vol_mass.php
   - Source for gCO₂/kWh by fuel type (coal, natural gas, solar, wind, hydro, nuclear)
3. **International Energy Agency (IEA)** - Electricity generation by source

   - https://www.iea.org/data-and-statistics
   - Source for global electricity mix data

### Microsoft Azure Carbon-Aware Example

4. **Microsoft Research: Carbon-Aware Computing**

   - "Towards Carbon-Aware Computing" - Microsoft Research Blog (2021)
   - https://www.microsoft.com/en-us/research/blog/towards-carbon-aware-computing/
   - Source for 16% carbon reduction in ML training workloads
5. **Microsoft Sustainability: Carbon Aware SDK**

   - https://github.com/Green-Software-Foundation/carbon-aware-sdk
   - Open-source SDK for building carbon-aware applications
6. **Azure Carbon Optimization**

   - "Building Carbon Aware Applications on Azure" - Microsoft Learn
   - https://learn.microsoft.com/en-us/azure/carbon-optimization/
   - Source for Azure carbon-aware scheduling practices

### Tools and APIs

7. **WattTime API** - Grid carbon intensity with forecasting

   - https://www.watttime.org/api-documentation/
   - Real-time and forecast carbon intensity data
8. **Carbon Intensity API (UK)** - UK National Grid carbon data

   - https://carbonintensity.org.uk/
   - Free API for UK grid carbon intensity
9. **KEDA (Kubernetes Event-Driven Autoscaling)**

   - https://keda.sh/
   - Kubernetes autoscaling based on external metrics
10. **Carbon-Aware KEDA Operator**

    - https://github.com/Azure/carbon-aware-keda-operator
    - Open-source Kubernetes operator for carbon-aware scaling

### Standards and Best Practices

11. **Green Software Foundation** - Software Carbon Intensity (SCI) Specification

    - https://greensoftware.foundation/
    - Standards for measuring and reducing software carbon emissions
12. **ISO/IEC 21031** - Software Carbon Intensity Specification

    - https://www.iso.org/standard/86612.html
    - International standard for measuring and reporting software carbon emissions
    - Based on Green Software Foundation's SCI specification
13. **Cloud Carbon Footprint** - Open-source carbon tracking

    - https://www.cloudcarbonfootprint.org/
    - Tool for measuring cloud carbon emissions (AWS, Azure, GCP)

### Additional Reading

14. **"Principles of Sustainable Software Engineering"** - Microsoft Learn

    - https://learn.microsoft.com/en-us/learn/modules/sustainable-software-engineering-overview/
    - Comprehensive guide to sustainable software practices
15. **"Carbon-Aware Kubernetes"** - CNCF Blog

    - https://www.cncf.io/blog/2023/10/11/carbon-aware-kubernetes/
    - Kubernetes-specific carbon-aware scheduling strategies

---

*Daniel Stauffer is an Enterprise Architect specializing in sustainable software practices and platform engineering. This is Part 4 of the Green Coding series.*

---

## Series Navigation

**Previous Article**: [Part 3: Database Optimization Strategies - Your Database is Probably Your Biggest Energy Hog](#)

**Coming Up in This Series**:

- Part 5: Sustainable Microservices Architecture - Building Distributed Systems That Don't Waste Energy
- Part 6: Green DevOps Practices - Sustainable CI/CD and Infrastructure Management
- Part 7: Sustainable AI/ML and MLOps - Training Models Without Burning the Planet
- Part 8: Programming Language Efficiency Deep Dive - Choosing the Right Tool for the Job
- Part 9: Carbon-Aware Workload Placement Strategies - The Geography of Green Computing

---

**Tags**: #GreenCoding #SustainableSoftware #CarbonAware #CloudComputing #DevOps #Kubernetes #ClimateAction

---

**Word Count**: ~2,100 words | **Reading Time**: ~7 minutes
