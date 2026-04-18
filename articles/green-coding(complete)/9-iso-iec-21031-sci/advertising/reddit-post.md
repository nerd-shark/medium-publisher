# Reddit Post

**Article**: Stop Guessing, Start Measuring: The ISO Standard for Software Carbon Intensity
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Suggested Subreddits
- r/programming
- r/softwarearchitecture
- r/ExperiencedDevs
- r/devops
- r/sustainability
- r/greentech
- r/sre

## Post Title
ISO/IEC 21031 (SCI): A practical walkthrough of measuring software carbon intensity — with Python code, real case studies, and honest limitations

## Post Body

I just wrapped up a nine-part series on sustainable software engineering. The last eight articles covered algorithm optimization, database efficiency, carbon-aware computing, CI/CD, ML training, language efficiency, and microservice architecture. All of it reduces carbon emissions from software.

The problem I kept running into: how do you actually measure whether any of it is working?

The GHG Protocol gives you annual Scope 2 totals, which is fine for sustainability reports but doesn't help with engineering decisions. A CTO can quote the company's total emissions but can't tell a developer whether the code they shipped last sprint was better or worse for the climate.

ISO/IEC 21031:2024 — the Software Carbon Intensity specification from the Green Software Foundation — addresses this with a single equation:

**SCI = (E × I + M) per R**

- E = energy consumed by your software (kWh)
- I = carbon intensity of the electricity grid (gCO₂/kWh)
- M = embodied emissions from hardware manufacturing, amortized over lifespan
- R = functional unit (per API call, per transaction, per user/day — whatever's meaningful)

Two design decisions that matter: it's a rate (not a total), so developers can optimize against it sprint over sprint. And offsets are explicitly excluded — the only way to improve your score is to genuinely reduce emissions.

**Real implementations:**

- Accenture: 0.025 gCO₂ per API call on a production app (890K monthly requests)
- UBS: Applied SCI to two on-prem banking apps — had to work with facilities teams for power data since there's no cloud dashboard equivalent
- Autostrade per l'Italia: Measured 60 applications, averaged 15.1% CO₂ savings. Some fixes took 4 person-days per app for 400 kg CO₂/year reduction
- Texas State University: Used SCI to compare AI models — GPT-Neo 1.3B used 27% of GPT-J 6B's energy with comparable output quality

**The walkthrough in the article:**

I walk through calculating SCI for a document processing API (30K docs/month, two EC2 instances, us-east-1). The breakdown: E × I was 98% of the score, embodied emissions barely registered. That surprised me and completely changed where I focused optimization.

The article includes a Python script that pulls carbon intensity from Electricity Maps and calculates SCI automatically, plus guidance on choosing R (the functional unit — this is where most teams get stuck), the CSRD compliance angle for EU-facing companies, and an honest section on limitations (rough embodied data, cross-type comparison challenges, young tooling).

**The series connection:**

Every article in the series maps to a variable in the SCI equation. Parts 2, 3, 6, 7, 8 reduce E. Part 4 reduces I. Part 5 reduces E and M. This article (Part 9) measures all of it with one number — which is where I was heading with the series from the start.

[ARTICLE URL]

Happy to discuss SCI implementation approaches, the functional unit design problem, or the practical challenges of getting energy data from shared infrastructure.

---

**Format**: No hashtags, technical, discussion-focused
