# Teams Post — Carbon-Aware Workload Placement

**Channel**: Jabil Developer Network — Architecture Community
**Subject Line**: The same computation emits 12x more carbon in Poland than in France. Your scheduler doesn't know that. It should.
**Featured Image**: `images/featured_image.png`
**Article URL**: https://medium.com/@the-architect-ds/stop-guessing-start-measuring-the-iso-standard-for-software-carbon-intensity-629ce8e99d57

---

![Featured Image](../images/featured_image.png)

## Where and When You Run Code Matters

Grid carbon intensity varies dramatically by region and time of day. Running a batch job in Iowa at 2 PM (wind-heavy grid) produces a fraction of the carbon compared to running it in Virginia at 6 PM (gas-heavy grid). The computation is identical. The carbon footprint isn't.

## What Carbon-Aware Scheduling Looks Like

The article covers practical strategies for reducing your workloads' carbon footprint without sacrificing performance:

- **Temporal shifting** — defer non-urgent workloads to low-carbon windows (overnight when wind/solar is available)
- **Spatial shifting** — route workloads to regions with cleaner grids (using real-time carbon intensity data from Electricity Maps or WattTime)
- **Demand shaping** — adjust compute intensity based on grid conditions
- **Carbon-aware Kubernetes scheduling** — custom schedulers that factor carbon intensity into pod placement decisions

The key insight: you don't need to sacrifice performance for sustainability. Most organizations have significant batch, ML training, CI/CD, and analytics workloads that are time-flexible. Shifting those to clean windows is free carbon reduction.

**Part 9 and series finale of the Green Coding series** — [Read the full article](https://medium.com/@the-architect-ds/stop-guessing-start-measuring-the-iso-standard-for-software-carbon-intensity-629ce8e99d57)
