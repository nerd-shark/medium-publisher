# X/Twitter Post

**Article**: Carbon-Aware Workload Placement
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Main Post

Same computation. Same code. Same result.

France: 56 gCO₂/kWh. Poland: 670 gCO₂/kWh. 12x difference.

Google cut emissions 24% just by routing workloads to cleaner grids. No code changes.

Your scheduler should probably know about this.

[ARTICLE URL]

#GreenCoding #ClimateTech

---

## Thread

**2/6**
Why the variation is so wild:

California at noon (solar peak): ~150 gCO₂/kWh
California at 7 PM (gas peakers): ~500 gCO₂/kWh

3x swing. Same region. Same day.

Across regions it's even crazier. Iceland ≈ 0. Norway ≈ 20. Poland ≈ 670.

Your cloud region choice is a carbon choice whether you think about it or not.

**3/6**
Three strategies, simplest first:

Time-shift: move batch jobs to low-carbon hours. Microsoft cut 16% by shifting ML training 4-8 hours. That's a cron job change.

Geo-shift: route to cleanest region. Needs multi-region infra but biggest impact.

Demand-shape: reduce compute when grid is dirty. Most sophisticated.

**4/6**
What to time-shift:
Batch processing, ML training, CI/CD, ETL, backups, reports

What NOT to time-shift:
User-facing APIs, payments, real-time alerts, anything with an SLA

Most teams have way more deferrable work than they think.

**5/6**
The data is free:

Electricity Maps — real-time global carbon intensity
WattTime — marginal emissions (NA + Europe)
AWS/Google/Azure all have carbon dashboards now

You can query carbon intensity via API and schedule accordingly. ~20 lines of Python.

**6/6**
This wraps up 9 articles on sustainable software engineering.

The consistent finding across all of them: efficient code is green code. Performance optimization and carbon optimization are basically the same thing.

Series finale: [ARTICLE URL]

---

**Thread length**: 6 tweets
