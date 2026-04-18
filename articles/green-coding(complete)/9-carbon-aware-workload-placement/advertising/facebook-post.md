# Facebook Post

**Article**: Carbon-Aware Workload Placement
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

Something that genuinely surprised me when I started digging into the data: the same computation emits 12x more carbon in Poland than in France.

At 2 PM in France, the grid runs at roughly 56 gCO₂/kWh — mostly nuclear. At the same moment in Poland, it's 670 gCO₂/kWh — mostly coal. Same code, same result, 12x difference in carbon emissions.

Your scheduler doesn't know any of this. It picks the cheapest region, or the closest, or whatever has capacity. Carbon intensity isn't a factor. For most companies, it never has been.

But what caught my attention was how big the impact is for how little effort. Google reported a 24% reduction in carbon emissions from carbon-aware load balancing — no code changes, no architecture changes, just routing workloads to cleaner grids. Microsoft hit 16% by shifting ML training to low-carbon hours. Literally changing when the cron job runs.

**Three strategies, simplest first:**

**Time-shifting** is the easiest. Defer batch jobs to hours when carbon intensity is lowest. Solar grids are cleanest midday. Wind grids are cleanest overnight. Microsoft found that shifting ML training by 4-8 hours cut carbon 16% with zero impact on delivery timelines. This is a scheduling change, not an architecture change.

**Geographic shifting** is more impactful but needs multi-region infrastructure. Route workloads to the cloud region with lowest current carbon intensity. Scandinavia runs near-zero carbon. The tradeoff is data transfer cost ($0.02/GB cross-region on AWS) and latency.

**Demand shaping** is the most sophisticated. Actually reduce compute during high-carbon periods. Critical stuff always runs. Standard work runs during medium/low carbon. Deferrable work waits for clean energy.

The data to make these decisions is freely available. Electricity Maps gives you real-time carbon intensity for grids worldwide. Cloud providers all have carbon dashboards now.

**The tradeoffs are real though.** Geographic shifting adds latency. Data residency rules (GDPR, HIPAA) constrain where data can go. Multi-region infra costs more. Start with the simplest strategy — time-shifting batch jobs requires zero infrastructure changes.

This wraps up 9 articles covering the full stack of sustainable software — algorithms, databases, carbon-aware apps, microservices, DevOps, AI/ML, language efficiency, and now workload placement.

The consistent finding across all of them: efficient code is green code. When you optimize for performance, you're usually optimizing for sustainability too.

Full guide with Python code and API examples:

[ARTICLE URL]

#GreenCoding #SustainableSoftware #CarbonAwareComputing #ClimateTech #CloudArchitecture #DevOps #Sustainability #CleanEnergy

---

**Character count**: ~2,300
**Hashtags**: 8
