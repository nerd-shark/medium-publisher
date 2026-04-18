# The HealthCare.gov Rescue: Every Communication Skill in One Crisis

Part 9 — Series Capstone. Real-world case study that uses every technique from the series.

## Why This Case Study

- HealthCare.gov launched October 1, 2013. Catastrophic failure. Only 6 people enrolled on day one.
- The rescue team (the "ad hoc" team, later became USDS) had to use EVERY communication skill we've covered
- Executive communication with the White House under political firestorm
- Stakeholder dynamics between CMS, multiple contractors (CGI Federal, QSSI, etc.), and political appointees
- Cross-functional collaboration between Silicon Valley engineers and government contractors
- Architecture reviews of a system nobody fully understood
- Technical writing for non-technical government officials
- Technical debt advocacy — the system was built on technical debt
- Incident response — the whole thing was one giant incident
- Perfect capstone because it's real, well-documented, and high-stakes

## The Setup (What Went Wrong)

- $840M+ spent on development across 55+ contractors
- No single technical owner — CMS managed contracts, not technology
- No integration testing until 2 weeks before launch
- Classic "waterfall meets politics" — launch date was immovable (ACA mandate)
- October 1 launch: site crashes immediately. 4.7 million unique visitors, system designed for maybe 50,000 concurrent
- Only 6 enrollments on day one. SIX.
- Political firestorm. Congressional hearings. "Obama's Katrina."

## Part 1 Technique: Speaking Executive (White House Briefings)

- Mikey Dickerson and Todd Park briefing the President and senior staff
- Had to translate "the database connection pool is exhausted and there's no caching layer" into "the system can't handle more than a few hundred users at once, and fixing it requires rebuilding core components"
- The 3-minute demo framework: "Here's what's broken, here's what we're doing, here's when it'll be fixed"
- The "So What?" test: every technical update had to answer "what does this mean for enrollment numbers?"
- Pyramid Principle: lead with "we can fix this by December 1" not "the Oracle database has connection pooling issues"

## Part 2 Technique: Stakeholder Dynamics (CMS, Contractors, White House)

- Multiple stakeholders with competing priorities
- CMS: protect the agency, manage contractor relationships
- Contractors (CGI Federal): protect the contract, minimize blame
- White House: political survival, enrollment numbers
- Congressional oversight: accountability, public hearings
- The rescue team had to navigate all of these simultaneously
- Classic "executives disagreeing in front of you" — CMS leadership vs White House tech team
- The neutral facilitator approach: focus on the system, not the blame

## Part 3 Technique: Presentations to Mixed Audiences

- Daily "war room" briefings with technical staff, CMS leadership, and White House officials
- Had to shift between technical depth (for engineers) and business impact (for political staff)
- The same status update needed three versions: technical (for the team), executive (for CMS), political (for White House)

## Part 4 Technique: Architecture Review Under Fire

- The rescue team had to do an architecture review of a system they didn't build
- Nobody had a complete picture of the architecture — 55+ contractors, no integration documentation
- Had to defend decisions about what to fix vs what to rebuild vs what to work around
- ADR-style documentation: "We're replacing the enrollment queue because [reasons], alternatives considered: [list]"

## Part 5 Technique: Design Reviews (Triage Meetings)

- Daily triage meetings to prioritize fixes
- Facilitating technical discussions between contractors who had never talked to each other
- Preventing bikeshedding when there were 200+ critical bugs
- Decision framework: "Does this block enrollment? If yes, fix it now. If no, it waits."

## Part 6 Technique: Technical Writing for Government

- The rescue team had to write status reports for non-technical government officials
- "The system is experiencing database connection pool exhaustion" → "The system can only serve 1,100 users at a time. We need it to serve 50,000."
- RFC-style proposals for major changes, written for an audience that included lawyers and political staff
- The "inverted pyramid" — most important information first, technical details in appendix

## Part 7 Technique: Communicating Technical Debt

- The entire system was technical debt
- Had to explain to political staff why "just fix it" wasn't possible
- The interest payment metaphor: "Every day we don't fix the database layer, we spend 4 hours on workarounds instead of new features"
- Quantifying the cost: "This technical debt is costing us 2,000 enrollments per day"
- Building the case for a partial rebuild vs patching

## Part 8 Technique: Cross-Functional Collaboration

- Silicon Valley engineers (Google, Oracle, Red Hat) working alongside government contractors
- Completely different cultures, tools, processes, and vocabularies
- Engineers who'd never worked in government + government staff who'd never worked with startup-style engineers
- Finding shared language: enrollment numbers became the universal metric
- "Yes, and" approach: "Yes, the contractor's code has issues, AND here's how we can work with them to fix it"

## The Resolution

- By December 1, 2013: site handling 50,000 concurrent users (up from ~1,100)
- 800,000+ enrollments in December alone
- The rescue team became the United States Digital Service (USDS)
- The communication skills were as critical as the technical skills

## Lessons and Series Recap

- Every technique from the series was used in a single 60-day crisis
- The engineers who succeeded weren't just technically excellent — they could communicate across every audience
- Communication IS the multiplier — the best fix in the world doesn't matter if you can't coordinate the team, brief the executives, and align the stakeholders

Target: ~500 words outline
