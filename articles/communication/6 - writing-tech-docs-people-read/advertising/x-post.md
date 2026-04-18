# X/Twitter Post

**Article**: Writing Technical Documents That Non-Technical People Actually Read
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Main Post

I once spent 3 weeks on a 47-page RFC. Two people opened it. One skimmed the conclusion.

The project got approved because I explained it in 5 minutes near the coffee machine.

That RFC was technically perfect and practically useless. Here's what I do differently now 🧵

---

## Thread

**2/7**
Your document has three audiences and they read completely differently.

Executives: title, first paragraph, conclusion. 30 seconds.
PMs: impact, timeline, dependencies. Skip implementation.
Engineers: everything. Want more.

You wrote for engineers. Everyone else bailed by page 3.

**3/7**
The one-page executive summary changed everything for me.

300 words max. Problem → Solution → Cost → Ask.

No jargon. No "refactoring the service mesh." Instead: "We lost $3.2M last year from downtime. Fix costs $400K. Pays for itself in one Black Friday."

One gets filed. The other gets funded.

**4/7**
Most RFC templates are structured backwards. Background first, recommendation on page 15.

Flip it. Executive summary on page 1. Business value up front. Technical details in the appendix.

Executives read top-down and stop when they've decided. Let them.

**5/7**
ADRs are criminally underused.

One decision per record. One page max. Context → Decision → Consequences (good AND bad).

Future you will be grateful when someone asks "why did we build it this way?" and there's an actual answer.

**6/7**
Biggest mistake isn't the writing — it's the process.

Don't disappear for 3 weeks and surprise stakeholders with a 47-page doc.

Pre-align incrementally. "I'd love your input before I formalize this" has gotten me more projects approved than any amount of technical rigor.

**7/7**
Monday test: hand page 1 of your last RFC to a non-technical colleague.

If they can't explain what you're proposing and why — rewrite it.

Full guide: [ARTICLE URL]

#TechnicalWriting #RFC

---

**Thread length**: 7 tweets
