# Writing Technical Documents That Non-Technical People Actually Read

Part 6 of my series on Technical Communication. Last time we covered facilitating design reviews. Now: the written word.

## Opening Hook - The RFC Nobody Read

- You spent 3 weeks writing a 47-page RFC
- It had everything: architecture diagrams, sequence diagrams, risk analysis, cost projections
- Two people read it. One skimmed the conclusion. The other read the title and asked "can you just summarize this in Slack?"
- The project got approved anyway — based on a 5-minute hallway conversation
- Your RFC was technically perfect and practically useless
- The problem isn't your technical depth. It's your document structure.

## The Fundamental Problem

- Engineers write documents for engineers
- But the people who approve, fund, and prioritize your work aren't engineers
- Executive reads: title, first paragraph, conclusion. Maybe a diagram if it's simple.
- Product manager reads: impact, timeline, dependencies. Skips implementation.
- Fellow engineer reads: everything. Wants more detail.
- One document, three audiences, three completely different reading patterns
- Most technical documents fail because they're written for one audience (engineers) and read by three

## The One-Page Executive Summary

- This is the most important page you'll ever write
- If your exec only reads one page, this is it
- Structure: Problem → Solution → Impact → Ask
- 300 words max. Seriously.
- No jargon. No acronyms without expansion. No "we need to refactor the service mesh."
- Instead: "Our checkout system fails 3% of the time during peak traffic, costing $2.1M annually. We propose X, which reduces failures to 0.1% and pays for itself in 4 months."
- The "So What?" test from Part 1 applies here too
- Every sentence must answer: why should the reader care?

## RFC Structure That Actually Works

- Problem statement (what's broken, who's affected, what it costs)
- Proposed solution (high-level, not implementation details)
- Alternatives considered (shows you did your homework)
- Tradeoffs (honest about what you're giving up)
- Implementation plan (phases, timeline, milestones)
- Risks and mitigation (what could go wrong)
- Open questions (what you don't know yet — this builds trust)
- Appendix: deep technical details (for engineers who want them)

The key insight: front-load the business value, back-load the technical details. Executives read top-down and stop when they've decided. Engineers read everything.

## Architecture Decision Records (ADRs)

- Short, focused, one decision per record
- Context: what's the situation and constraints?
- Decision: what did we decide?
- Consequences: what happens because of this decision?
- Status: proposed, accepted, deprecated, superseded
- Link ADRs together to form decision history
- ADRs are for future you — the person who asks "why did we do it this way?"
- Keep them short. If it's more than one page, it's not an ADR, it's an RFC.

## Writing for Different Audiences

- The layered document approach
- Layer 1: Executive summary (1 page, business value)
- Layer 2: Technical overview (3-5 pages, architecture and approach)
- Layer 3: Implementation details (appendix, unlimited, for engineers)
- Each layer is self-contained — reader can stop at any layer and have a complete picture
- Think of it like a newspaper article: headline, lead paragraph, full story, background

## Visual Communication

- A good diagram replaces 1,000 words of explanation
- A bad diagram adds 1,000 words of confusion
- Architecture diagrams: show components and connections, not implementation details
- Data flow diagrams: show how data moves through the system
- Decision trees: show branching logic for complex decisions
- Sequence diagrams: show interactions between components over time
- The #1 mistake: too much detail. If your diagram needs a legend with 20 symbols, simplify it.
- Use color intentionally (red = problem, green = solution, gray = existing)

## The "Inverted Pyramid" for Technical Writing

- Journalism technique: most important info first
- Works perfectly for technical documents
- Paragraph 1: the conclusion (what you want the reader to know/do)
- Paragraph 2: the evidence (why this is the right answer)
- Paragraph 3: the context (background for those who need it)
- Most people read the first paragraph of each section and move on
- Make sure that first paragraph carries the weight

## Getting Feedback Before Formal Submission

- Don't surprise stakeholders with a 40-page RFC
- Pre-align with key decision makers
- Share drafts early, get feedback, iterate
- The formal submission should be a formality, not a surprise
- "I'd love your input on this before I formalize it" is magic

## Common Mistakes

- Writing a novel when a memo would do
- Burying the ask on page 37
- Using jargon the audience doesn't know
- No executive summary
- Diagrams that need a PhD to interpret
- Not acknowledging tradeoffs (makes you look naive)
- Treating the document as the decision (the conversation is the decision, the document is the record)

## What to Do Monday Morning

- Take your last RFC/proposal
- Add a one-page executive summary at the top
- Move all implementation details to an appendix
- Ask a non-technical colleague to read the first page
- If they can't explain what you're proposing and why, rewrite it

Target: ~2,500 words at v4, 8-9 min read
