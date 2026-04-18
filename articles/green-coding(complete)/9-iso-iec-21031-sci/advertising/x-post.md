# X/Twitter Post

**Article**: Stop Guessing, Start Measuring: The ISO Standard for Software Carbon Intensity
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Main Post

Your company reports annual carbon totals. Your developers have no idea if the code they shipped last sprint was better or worse.

ISO/IEC 21031 fixes that. One equation. One score. Per API call.

SCI = (E × I + M) per R

Series finale — full walkthrough:

[ARTICLE URL]

---

## Thread

**2/7**
The SCI equation in plain English:

E = energy your software uses (kWh)
I = how dirty the grid is (gCO₂/kWh)
M = carbon cost of manufacturing the hardware
R = your functional unit (per call, per user, per doc)

It's a rate, not a total. And offsets don't count.

**3/7**
Why a rate matters:

"Your company emitted 500 tons" — nobody on the engineering team knows what to do with that.

"This API emits 0.025 gCO₂ per call" — now you can optimize it sprint over sprint.

**4/7**
Real numbers from production:

Accenture: 0.025 gCO₂/API call (890K monthly requests)
Autostrade: 15.1% avg CO₂ savings across 60 apps
Fix: 4 person-days → 400 kg CO₂ reduced/year per app

**5/7**
The variable that surprised me: when I ran this on my own service, I expected embodied emissions (M) to dominate.

E × I was 98% of the score. Hardware lifecycle barely mattered. Completely changed where I focused optimization.

**6/7**
Every article in my 9-part green coding series maps to a variable:

Parts 2,3,6,7,8 → reduce E
Part 4 → reduce I
Part 5 → reduce E and M

Part 9 (this one) → measure all of it with one number.

**7/7**
The article has:
- Step-by-step SCI calculation walkthrough
- Working Python code
- Case studies (Accenture, UBS, Autostrade)
- CSRD compliance angle
- Honest limitations

[ARTICLE URL]

---

**Thread length**: 7 tweets
