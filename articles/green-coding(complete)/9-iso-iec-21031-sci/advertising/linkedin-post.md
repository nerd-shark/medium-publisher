# LinkedIn Post

**Article**: Stop Guessing, Start Measuring: The ISO Standard for Software Carbon Intensity
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

Nine articles on sustainable software engineering. Algorithm optimization, database efficiency, carbon-aware computing, CI/CD pipelines, ML training, language selection, microservice architecture. All of it reduces carbon.

None of it gave me a single number I could track over time.

That bothered me. You can't manage what you can't measure, and for software carbon emissions, the measurement didn't exist in any form a developer could act on. The GHG Protocol gives you annual Scope 2 totals — useful for sustainability reports, useless for sprint planning.

ISO/IEC 21031:2024 fixes that. The Software Carbon Intensity specification, developed by the Green Software Foundation, boils everything down to one equation:

SCI = (E × I + M) per R

E is energy consumed. I is carbon intensity of the grid. M is embodied emissions from hardware manufacturing. R is your functional unit — per API call, per transaction, per document processed. Whatever's meaningful to your software.

Two design choices make this standard worth paying attention to. First, it's a rate, not a total. "This API emits 0.025 gCO₂ per call" is something a developer can optimize against. "Your company emitted 500 tons" is not. Second, offsets are explicitly excluded. You can't buy your way to a better score. The only path is genuine reduction.

Accenture measured a production app at 0.025 gCO₂ per API call across 890K monthly requests. Autostrade per l'Italia measured 60 applications and averaged 15.1% CO₂ savings — with some fixes taking just 4 person-days of effort per app.

The first time I ran the calculation on one of my own services, I expected embodied emissions to be the big number. It wasn't close. E × I was 98% of the score. That reframed where I spent my optimization time.

The article walks through calculating your first SCI score step by step, with working Python code, case studies from Accenture/UBS/Autostrade, the CSRD compliance angle, and honest limitations.

Series finale — every article in the series maps to a variable in this equation.

[ARTICLE URL]

---

**Character count**: ~1,750 (body only, no hashtags)
**Hashtags**: None (per LinkedIn policy)
