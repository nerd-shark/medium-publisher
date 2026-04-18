# LinkedIn Post

**Article**: Carbon-Aware Workload Placement: Running Code Where and When the Grid Is Cleanest
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

Something that genuinely surprised me when I started digging into the data: the same computation emits 12x more carbon in Poland than in France.

France runs at ~56 gCO₂/kWh (mostly nuclear). Poland runs at ~670 gCO₂/kWh (mostly coal). Same code. Same result. 12x difference in carbon.

Your scheduler doesn't know any of this. It picks the cheapest region, or the closest one, or whatever has capacity. Carbon intensity isn't a factor.

Part 9 — and the finale — of my Sustainable Software Engineering series.

What caught my attention was how big the impact is for how little effort it takes. Google reported a 24% carbon reduction from carbon-aware load balancing. Not from rewriting code. Not from changing architecture. Just from routing workloads to cleaner grids.

Microsoft hit 16% by shifting ML training to low-carbon hours. Literally just changing when the cron job runs.

Three strategies, in order of complexity:

Time-shifting is the easiest. Defer batch jobs to hours when the grid is cleanest. Solar grids peak midday. Wind grids peak overnight. This is a cron job adjustment, not an architecture change.

Geographic shifting is more impactful but needs multi-region infra. Route workloads to the region with lowest current carbon intensity. Scandinavia runs near-zero. The tradeoff is data transfer cost and latency.

Demand shaping is the most sophisticated. Actually reduce compute during high-carbon periods. Critical stuff always runs. Deferrable work waits for clean energy.

The data to make these decisions is freely available. Electricity Maps gives you real-time carbon intensity worldwide. Cloud providers all have carbon dashboards now.

This wraps up 9 articles covering the full stack of sustainable software — algorithms, databases, carbon-aware apps, microservices, DevOps, AI/ML, language efficiency, and now workload placement.

The through-line across all of it: efficient code is green code. When you optimize for performance, you're usually optimizing for sustainability too. They're the same thing.

Full guide with Python code and API examples:

[ARTICLE URL]

#GreenCoding #SustainableSoftware #CarbonAwareComputing #CloudArchitecture #DevOps #ClimateTech #SoftwareEngineering #Sustainability #CleanEnergy #ElectricityMaps

---

**Character count**: ~2,000
**Hashtags**: 10
