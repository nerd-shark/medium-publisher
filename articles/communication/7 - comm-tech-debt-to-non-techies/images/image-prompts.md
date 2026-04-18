# Featured Image Prompts — Communicating Technical Debt

## Prompt 1: The Velocity Decline
A dramatic illustration of a futuristic speedometer or gauge dashboard. The main gauge shows a needle that has been steadily declining — a glowing trail behind the needle shows its path from the green zone (top, fast) down through amber to the red zone (bottom, slow). The gauge face is cracked and worn in the red zone. Around the main gauge, smaller gauges show: bug rate (climbing), incident frequency (climbing), developer satisfaction (declining). The overall feel is a control panel showing systemic degradation. In the background, faint outlines of code or circuit patterns are visible, slightly corroded or rusted. Style: dashboard/cockpit aesthetic, dramatic lighting, warm-to-cool gradient showing decline. Dark background. 16:9 landscape. No text, no numbers on gauges.

## Prompt 2: The Compound Interest
A visual metaphor showing a building (representing a codebase) where the foundation and lower floors are made of crumbling, patched, duct-taped materials (technical debt) while the upper floors are sleek and modern (new features). The building is visibly leaning and stressed. Cracks propagate upward from the foundation into the newer floors. Construction workers on the upper floors are trying to build new additions, but the unstable foundation makes their work precarious. A large weight labeled-style hangs from the building representing accumulated interest. In contrast, a smaller building next to it has a solid, clean foundation and stands straight — representing a well-maintained codebase. Style: architectural cross-section, contrast between decay and stability. Warm tones for debt, cool tones for health. 16:9 landscape. No text, no labels.

## Prompt 3: The Hidden Iceberg
A dramatic illustration of a glowing digital iceberg in a dark ocean. Above the waterline (visible to stakeholders): a small tip showing "slow features" and "bugs" — represented by a few red warning lights. Below the waterline (invisible): a massive structure of tangled wires, corroded circuits, patched connections, and accumulated complexity — glowing amber and red. The underwater portion is 10x larger than the visible tip. A beam of light from above (representing communication/visibility) illuminates part of the underwater structure, making it visible for the first time. Small figures on a boat above peer down at the revealed complexity. Style: dramatic, underwater/above-water split composition, glowing digital elements. Dark blue-black background. 16:9 landscape. No text.

---

# In-Article Graphic Prompts

## In-Article 1: Velocity Death Spiral Chart
**Placement**: After "The Velocity Death Spiral" section opening, replacing the `> Graphic idea` callout.

A realistic screenshot of a Jira Velocity Report widget, as it would appear inside a Jira Software board's "Reports" tab. White background, standard Jira UI chrome — the left sidebar is partially visible with navigation items, and the top shows the board name and "Velocity Report" heading in Jira's default font. The chart area shows a bar chart spanning eight sprints (Sprint 14 through Sprint 21). The bars represent completed story points: the first four sprints are tall and consistent (around 42–46 points, colored Jira's standard green-blue), then a visible drop begins at Sprint 18, and the last three sprints are noticeably shorter (28–32 points, same color but the decline is obvious). A gray "commitment" line sits above the bars, staying roughly flat, making the growing gap between commitment and completion clearly visible. Below the chart, the standard Jira sprint summary row shows sprint names and dates. A red hand-drawn circle annotation (as if someone used a screenshot markup tool) circles the drop-off point at Sprint 18 with a short handwritten arrow pointing to it. The overall feel is a real tool screenshot someone would paste into a Slack message or a slide deck to say "look at this." Style: photorealistic Jira UI screenshot, standard browser rendering, light theme. 16:9 landscape.

## In-Article 2: Loan Interest Diagram
**Placement**: After "The Interest Payment Metaphor" section, replacing the `> Graphic idea` callout.

A realistic screenshot of a simple spreadsheet or Google Sheets chart that an engineering manager would actually build to pitch debt paydown. The spreadsheet is visible behind the chart — a few columns: "Feature #", "Extra Days (Interest)", "Cumulative Cost ($)". The embedded chart is a combo chart: orange bars showing extra engineering days per feature (growing from 2 to 5 days over 14 features), and a red cumulative line climbing steeply to the right. A single green bar on the far left, separated by a gap, represents the original 10-day shortcut labeled "Initial Shortcut." The cumulative line crosses a horizontal dashed reference line near the top, where the total interest ($84K) has far exceeded the original savings ($20K). The Google Sheets UI chrome is visible — toolbar, sheet tabs at the bottom ("Debt Analysis"), cell grid behind the chart. The chart title reads "Payment Module: Accumulated Technical Debt Cost." A yellow sticky-note-style comment box is anchored to the crossover point, as if a collaborator left a comment. Style: photorealistic Google Sheets screenshot, standard browser rendering, light theme, slightly messy real-world spreadsheet feel. 16:9 landscape.

## In-Article 3: Three-Panel Visualization Suite
**Placement**: After "Visualizing the Invisible" section, replacing the `> Graphic idea` callout.

A realistic composite screenshot showing three side-by-side tool panels, as if someone arranged three browser windows or dashboard widgets on a wide monitor and took a screenshot. Light backgrounds, real tool UI chrome.

**Left panel**: A GitLab Value Stream Analytics or Jira Control Chart screenshot. Shows a time-series line chart of cycle time or velocity over roughly 6 months. The line trends clearly upward (cycle time increasing) or downward (velocity dropping). Standard GitLab/Jira chart styling — gray gridlines, blue or teal data line, axis labels showing months. The GitLab left nav or Jira report header is partially visible.

**Center panel**: A SonarQube project dashboard screenshot showing the code-quality overview. The familiar SonarQube layout: the project name at top, the letter-grade badges (A/B/C/D/E) for Reliability, Security, and Maintainability — with Reliability showing a C (yellow) and Maintainability showing a B. Below, the metrics tiles show bugs count, vulnerabilities, code smells (a high number like 84), coverage percentage, and duplications percentage. The "Technical Debt" metric is prominently displayed showing something like "25d" (25 days). Standard SonarQube light theme UI.

**Right panel**: A Grafana or Datadog dashboard panel showing an incident-frequency time series. A bar chart or area chart with weekly incident counts over 6 months, trending upward. Orange/red coloring for severity. The Grafana panel header with the gear icon and time-range selector is visible. A threshold line in red sits near the top, and recent bars are approaching or exceeding it.

The three panels are arranged in a clean row with thin gaps between them, as if pasted into a slide deck or Confluence page. Style: photorealistic tool screenshots composited together, light themes, standard browser rendering. 16:9 landscape.

## In-Article 4: Pain vs. Effort Prioritization Quadrant
**Placement**: After "Prioritization: What to Fix First" section, replacing the `> Graphic idea` callout.

A realistic screenshot of a Miro or FigJam whiteboard showing a hand-built prioritization matrix that a tech lead would actually create during a planning session. White canvas background with the characteristic Miro/FigJam toolbar visible at the bottom or side. Two hand-drawn-style axes divide the board into four quadrants — vertical axis labeled "Pain / Impact" and horizontal axis labeled "Effort." Each quadrant has a colored background tint and a label in a sticky-note or text box:

**Top-left** (high pain, low effort): Light green tint, labeled "Quick Wins — Start Here." Contains 5–6 small sticky notes in green and yellow, each with short realistic text like "Fix payment retry logic," "Update auth token caching," "Remove deprecated API v1 calls." A star or fire emoji on a couple of them.

**Top-right** (high pain, high effort): Light orange tint, labeled "Plan as Project." Contains 2–3 larger sticky notes in orange: "Migrate to event-driven checkout," "Replace legacy ORM layer."

**Bottom-left** (low pain, low effort): Light blue tint, labeled "Do When Nearby." Contains 3–4 small sticky notes in blue: "Clean up unused env vars," "Update logging format," "Remove dead feature flags."

**Bottom-right** (low pain, high effort): Light gray or light red tint, labeled "Probably Not Worth It." Contains 1–2 faded or crossed-out sticky notes in gray/pink: "Full database migration to NoSQL," "Rewrite notification service."

A few Miro cursor avatars (small colored circles with initials) are scattered on the board, as if multiple team members were collaborating. One cursor is dragging a sticky note. Connector arrows link a couple of related items across quadrants. The overall feel is a real working session artifact — slightly messy, clearly collaborative, obviously from a real tool. Style: photorealistic Miro/FigJam screenshot, standard browser rendering, light theme. 16:9 landscape.

---

## Usage Notes

### Featured Image
- All featured prompts 16:9 landscape for Medium featured images
- Recommended: Prompt 3 (Hidden Iceberg) for featured image — strongest metaphor for invisible debt

### In-Article Graphics
- In-Article 1 (Jira Velocity Report): 16:9 — place after the opening anecdote
- In-Article 2 (Google Sheets Debt Chart): 16:9 — place after the interest-payment metaphor
- In-Article 3 (Tool Triptych — GitLab/SonarQube/Grafana): 16:9 — place after "Visualizing the Invisible"
- In-Article 4 (Miro Prioritization Board): 16:9 — place after "Prioritization: What to Fix First"

### General
- Featured images: artistic/metaphorical, dark backgrounds, no text
- In-article graphics: photorealistic tool screenshots (Jira, Google Sheets, SonarQube, Grafana, Miro), light themes, real UI chrome visible
- The contrast between artistic featured image and realistic in-article graphics reinforces the article's message: making the invisible tangible with real tools
- Color coding for featured images: red/amber = debt/decay, green/blue = health, gold = visibility/communication
