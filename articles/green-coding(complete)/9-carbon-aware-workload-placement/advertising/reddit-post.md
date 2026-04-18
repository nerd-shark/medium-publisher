# Reddit Post

**Article**: Carbon-Aware Workload Placement
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Suggested Subreddits
- r/programming
- r/devops
- r/aws
- r/cloudcomputing
- r/sustainability
- r/ExperiencedDevs
- r/softwarearchitecture

## Post Title
The same computation emits 12x more carbon in Poland than France — here's how to make your scheduler carbon-aware

## Post Body

I just wrapped up a 9-part series on sustainable software engineering. The final article covers what I think is the most underappreciated lever in the whole space: where and when you run code.

Here's what surprised me when I first looked at the data: electricity grids have wildly different carbon intensities depending on location and time of day. France runs at ~56 gCO₂/kWh (nuclear). Poland runs at ~670 gCO₂/kWh (coal). That's 12x for the exact same computation. California swings from 150 at noon (solar) to 500 at 7 PM (gas peakers). Your cloud region choice is implicitly a carbon choice, and most of us never think about it.

**Real results from big tech:**
- Google: 24% carbon reduction from carbon-aware load balancing (no code changes)
- Microsoft: 16% reduction from time-shifting ML training by 4-8 hours

**Three strategies**:

1. **Time-shifting**: Defer non-urgent workloads (batch jobs, ML training, CI/CD, ETL) to hours when carbon intensity is lowest. Solar grids are cleanest midday, wind grids overnight. This requires zero infrastructure changes — just adjust your cron schedule based on carbon forecasts.

2. **Geographic shifting**: Route workloads to the cloud region with lowest current carbon intensity. Requires multi-region infrastructure but delivers the largest reductions. The tradeoff is data transfer cost ($0.02/GB cross-region on AWS) and latency.

3. **Demand shaping**: Actively reduce compute during high-carbon periods. Classify workloads by priority — critical always runs, standard runs during medium/low carbon, deferrable only runs during low carbon. This is the most sophisticated approach but requires workload classification.

**The data is free**:
- Electricity Maps: real-time carbon intensity for grids worldwide (free API for personal use)
- WattTime: marginal emissions data for North America and Europe
- Cloud providers: AWS Customer Carbon Footprint Tool, Google Cloud Carbon Footprint, Azure Emissions Impact Dashboard

**The tradeoffs**:
- Latency vs carbon (geographic shifting adds 80-120ms cross-region)
- Data residency (GDPR, HIPAA constrain where data can go)
- Measurement uncertainty (grid data is directionally correct but not precise)
- Complexity (each strategy adds operational overhead)

**Implementation**: The article includes Python code for querying Electricity Maps API, selecting the greenest region, scheduling batch jobs for optimal carbon hours, and a priority-based carbon-aware scheduler.

**The series retrospective**: Over 9 articles I covered the full stack — algorithms, databases, carbon-aware applications, microservices, DevOps, AI/ML, language efficiency, and workload placement. The thing that kept coming up: efficient code is green code. Performance optimization and carbon optimization are basically the same thing in most cases.

[ARTICLE URL]

Happy to discuss carbon-aware scheduling, multi-region tradeoffs, or the Electricity Maps API in the comments.

---

**Format**: No hashtags, technical, data-driven
