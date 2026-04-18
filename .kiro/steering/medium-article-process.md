---
inclusion: manual
keywords: medium, article, blog, writing, publication, social media, advertising
description: Loads the complete Medium article writing process including versioning, advertising infrastructure, and publication workflow
---

# Medium Article Writing Process - Steering Guide

**Trigger Keywords**: medium, article, blog, writing, publication, social media, advertising

**Purpose**: When working on Medium articles, this steering guide ensures you follow the established process for version control, advertising infrastructure, and publication.

---

## Core Process Document

**Location**: `for-approval/medium/ARTICLE-WRITING-PROCESS.md`

**MANDATORY**: Read this document completely before working on any Medium article.

---

## Quick Process Overview

### Phase 1: Pre-Writing Setup
1. Create article directory structure
2. Review writing samples for tone
3. Research market opportunity (optional)

### Phase 2: Proposal Creation
1. Create initial proposal
2. Get feedback and refine

### Phase 3: Version 1 - Initial Draft
1. Write first complete draft (v1)
2. Create TODO list
3. **Create advertising infrastructure** (MANDATORY after v1 complete)
   - linkedin-post.md
   - x-post.md
   - instagram-post.md
   - facebook-post.md
   - threads-post.md
   - reddit-post.md
   - hashtag-strategy.md

### Phase 4: Iterative Refinement
1. Create new versions (v2, v3, v4, etc.)
2. **Review and update advertising materials after each major revision**
3. Document changes in TODO.md

### Phase 5: Version Control
- Never modify existing versions
- Always create new version files
- Track changes in TODO.md

### Phase 6: Content Guidelines
- Conversational but authoritative tone
- Concrete examples with real numbers
- Short paragraphs (2-4 sentences)
- Self-documenting code

### Phase 7: Pre-Publication Checklist
- Content review
- Technical accuracy
- Readability
- SEO optimization (MANDATORY)
- Supporting materials

### Phase 8: Publication and Promotion
- Select final version
- Publish on Medium
- Use pre-created advertising infrastructure
- Post to all platforms according to schedule

### Phase 9: Post-Publication
- Monitor engagement
- Track metrics
- Iterate based on feedback

### Phase 10: Series Management
- Plan article series
- Cross-link articles
- Create series landing page

---

## Critical Rules

### Advertising Infrastructure (MANDATORY)

**When to Create**: After v1 is complete (Phase 3.3)
**When to Update**: After each major revision (Phase 4.6)

**Required Files**:
```
{article-name}/
└── advertising/
    ├── linkedin-post.md      (700-1,000 chars, provocative hook + summary, no hashtags, link at bottom)
    ├── x-post.md             (280 chars + thread, 5 hashtags)
    ├── instagram-post.md     (2,200 chars, 30 hashtags)
    ├── facebook-post.md      (1,000-2,000 chars, 20-30 hashtags)
    ├── threads-post.md       (500 chars, 15-20 hashtags)
    ├── reddit-post.md        (no hashtags, subreddit list)
    ├── teams-post.md         (internal, images/formatting OK, no hashtags)
    └── hashtag-strategy.md   (platform-specific tags)
```

**Update Decision Matrix**:
| Change Type | Update Advertising? |
|-------------|---------------------|
| New major section | Yes |
| Better example/number | Yes |
| Expanded existing section | Maybe |
| Added nuance/balance | Maybe |
| Removed redundancy | No |
| Typo fixes | No |

### Version Control (MANDATORY)

**Never modify existing versions** - Always create new version files

**Version Naming**: `v{N}-{article-name}.md`

**Version Increment Triggers**:
- Adding new major section
- Expanding existing section significantly
- Replacing examples or content
- Addressing feedback requiring structural changes

**Don't Create New Version For**:
- Typo fixes
- Minor wording changes
- Formatting adjustments
- Link updates

### SEO Optimization (MANDATORY)

**Title**: 60-70 characters, include primary keyword
**Subtitle**: 140-160 characters, include secondary keywords
**First Paragraph**: Include primary keyword within first 100 words
**Subheadings**: Include keywords, use question format
**Tags**: Use all 5 tags (primary tag first)
**Internal Links**: 3-5 links to related articles
**External Links**: 3-5 links to authority sources

### Series Articles (MANDATORY)

**Published Article URLs**: `articles/published.md`

**MANDATORY**: When writing or revising any series article, look up actual published URLs from `articles/published.md` and use them in series navigation links and inline cross-references. Never leave placeholder `(link)` values when the article has already been published. Check `published.md` before finalizing any version.

**Opening Blurb**:
```markdown
Part {N} of my series on {Series Name}. Last time, we explored {previous topic} — {brief description}. This time: {current topic}. Follow along for more {series theme}.
```

**Series Navigation** (at end):
```markdown
---

## Series Navigation

**Previous Article**: [Title](link)
**Next Article**: [Title](link) *(Coming soon!)*
**Coming Up**: Topic 1, Topic 2, Topic 3
```

---

## Directory Structure

```
for-approval/medium/{series}/
├── {article-name}/
│   ├── versions/
│   │   ├── v1-{article-name}.md
│   │   ├── v2-{article-name}.md
│   │   └── v3-{article-name}.md
│   ├── advertising/          (created after v1)
│   │   ├── linkedin-post.md
│   │   ├── x-post.md
│   │   ├── instagram-post.md
│   │   ├── facebook-post.md
│   │   ├── threads-post.md
│   │   ├── reddit-post.md
│   │   └── hashtag-strategy.md
│   ├── {article-name}-proposal.md
│   └── TODO.md
```

---

## Posting Schedule (Day of Publication)

| Time | Platform | File Reference |
|------|----------|----------------|
| 9:00 AM | Medium | Publish article |
| 9:15 AM | LinkedIn | `advertising/linkedin-post.md` |
| 9:30 AM | X/Twitter | `advertising/x-post.md` (main) |
| 10:00 AM | Teams | `advertising/teams-post.md` |
| 12:00 PM | Instagram | `advertising/instagram-post.md` |
| 12:15 PM | Facebook | `advertising/facebook-post.md` |
| 12:30 PM | Threads | `advertising/threads-post.md` |
| 5:00 PM | Reddit | `advertising/reddit-post.md` |
| 5:30 PM | X/Twitter | `advertising/x-post.md` (thread) |

---

## Platform Limits

| Platform | Character Limit | Hashtag Limit |
|----------|----------------|---------------|
| LinkedIn | 3,000 | 0 | Provocative hook + professional summary, 700-1,000 chars, no hashtags, link at bottom |
| X/Twitter | 280 | 5-10 |
| Instagram | 2,200 | 30 |
| Facebook | No limit | 20-30 |
| Threads | 500 | 15-20 |
| Reddit | No limit | 0 |
| Teams | No limit | 0 | Internal (Jabil Dev Network — Architecture Community), 30-60s read, featured image, catchy subject |

---

## Backfilling Existing Articles

**Priority Order**:
1. Most Recent (last 30 days)
2. High-Performing (most views)
3. Series Starters (first in series)
4. Remaining (chronological)

**Timeline**: Complete within 2 weeks

**Process**: See Appendix A in ARTICLE-WRITING-PROCESS.md

---

## Article Template - Front Matter and Back Matter

**CRITICAL**: Front matter and back matter are MANDATORY and consistent. Middle content is variable.

### FRONT MATTER (MANDATORY)

```markdown
# [Article Title - 60-70 characters, include primary keyword]

[Feature Image - uploaded directly to Medium, 1400x788px]

---

## Opening Blurb (For Series Articles Only)

Part {N} of my series on {Series Name}. Last time, we explored {previous topic} — {brief description of previous article in 1-2 sentences}. This time: {current topic and what readers will learn}. Follow along for more {series theme}.

---

## Hook / Introduction (3-4 paragraphs)

[Attention-grabbing opening - surprising fact, relatable scenario, or compelling question]

[Establish relevance - why this matters to the reader]

[Set expectations - what the article will cover]

[Include primary keyword within first 100 words]

---
```

**Front Matter Rules**:
- Title: 60-70 characters, primary keyword near beginning
- Opening blurb: ONLY for series articles (2-3 sentences)
- Hook: 3-4 paragraphs, conversational tone, grab attention immediately
- Primary keyword: Must appear in first 100 words

---

### MIDDLE CONTENT (VARIABLE)

```markdown
## [Main Content - 8-12 major sections with H2 headings]

[Content varies by article type and topic]
[Use whatever structure fits the content]
[Mix technical examples, strategies, case studies, frameworks as needed]

---
```

**Middle Content Guidelines**:
- 8-12 major sections (H2 headings)
- Short paragraphs (2-4 sentences)
- Concrete examples with real numbers
- Quantify impact where possible
- Use code blocks for technical articles
- Use Wrong/Right examples for communication articles
- Include case studies when you have experience
- Add tradeoffs section for balanced perspective

---

### BACK MATTER (MANDATORY)

```markdown
---

**Key Takeaways**:
- Takeaway 1
- Takeaway 2
- Takeaway 3
- Takeaway 4
- Takeaway 5

**Action Items**:
1. Action 1
2. Action 2
3. Action 3
4. Action 4
5. Action 5

---

## Tools and Resources

**[Category 1]**:
- [Tool Name](URL): Brief description
- [Tool Name](URL): Brief description

**[Category 2]**:
- [Tool Name](URL): Brief description
- [Tool Name](URL): Brief description

**[Category 3]** (if applicable):
- [Tool Name](URL): Brief description

---

## What's Next (For Series Articles Only)

In Part {N+1}, we'll explore {next topic}: {brief description of what's coming}.

**Coming up**:
- Topic 1
- Topic 2
- Topic 3
- Topic 4

---

## Series Navigation (For Series Articles Only)

**Previous Article**: [Title](link)
**Next Article**: [Title](link) *(Coming soon!)*

---

*{Your name} is an {title} specializing in {specialties}. {One sentence about passion or focus}.*

#{Tag1} #{Tag2} #{Tag3} #{Tag4} #{Tag5}
```

**Back Matter Rules**:
- Key Takeaways: MANDATORY, 5-6 bullet points summarizing main points
- Action Items: MANDATORY, 5-6 numbered steps readers can take
- Tools and Resources: MANDATORY, categorized by type, 2-4 categories
- What's Next: ONLY for series articles, brief preview of next article
- Series Navigation: ONLY for series articles, links to previous/next
- About the Author: 1-2 sentences in italics, no social links
- Hashtags: Exactly 5 tags, at very end, primary tag first

---

## Template Usage - What Matters

### FRONT MATTER (Consistent, MANDATORY)

**Title**:
- 60-70 characters
- Primary keyword near beginning
- Format: "How to {Action}" or "Why {Topic} Matters" or "{Provocative Statement}"

**Feature Image**:
- 1400x788px
- Upload directly to Medium

**Opening Blurb** (series only):
- 2-3 sentences
- "Part {N} of my series on {Series}. Last time... This time... Follow along..."

**Hook**:
- 3-4 paragraphs
- First sentence grabs attention (surprising fact, relatable scenario, provocative statement)
- Primary keyword in first 100 words
- Conversational, direct tone

### MIDDLE CONTENT (Variable, Your Choice)

**Guidelines**:
- 8-12 major sections (H2 headings)
- Short paragraphs (2-4 sentences)
- Concrete examples with real numbers
- Quantify impact where possible
- Let content dictate structure

**Common Patterns** (use what fits):
- Problem → Solution → Example → Impact
- Numbered strategies with Wrong/Right examples
- Real-world case studies with metrics
- Tradeoffs section ("Let's Be Honest")
- Measurement tools and code
- Stakeholder frameworks or tables

### BACK MATTER (Consistent, MANDATORY)

**Tools and Resources**:
- MANDATORY section
- 2-4 categories
- Tool name + link + brief description
- Categorize by type (Optimization, Monitoring, etc.)

**What's Next** (series only):
- Preview next article
- List 3-4 coming topics

**Series Navigation** (series only):
- Previous Article link
- Next Article link

**About the Author**:
- 1-2 sentences in italics
- Format: "*{Name} is an {title} specializing in {areas}. {Passion statement}.*"
- No social links

**Hashtags**:
- Exactly 5 tags
- At very end
- Format: #{Tag1} #{Tag2} #{Tag3} #{Tag4} #{Tag5}
- Primary tag first

---

## What's Consistent vs What's Variable

### CONSISTENT (Front Matter + Back Matter)

**Every Article Has**:
1. Title (60-70 chars, keyword-optimized)
2. Feature image (1400x788px)
3. Hook (3-4 paragraphs, attention-grabbing)
4. Key Takeaways (5-6 bullet points)
5. Action Items (5-6 numbered steps)
6. Tools and Resources section (categorized)
7. About the Author (1-2 sentences, italics)
8. Hashtags (exactly 5, at very end)

**Series Articles Also Have**:
7. Opening blurb (2-3 sentences)
8. What's Next section
9. Series Navigation links

### VARIABLE (Middle Content)

**Content Structure Varies By**:
- Article topic and type
- Technical vs communication focus
- Depth of coverage needed
- Available examples and case studies
- Your experience with the topic

**Let Content Dictate Structure**:
- Technical articles: Heavy on code, examples, metrics
- Communication articles: Strategies, frameworks, scenarios
- Mixed articles: Whatever combination fits

**Don't Force Sections That Don't Fit**:
- Not every article needs a case study
- Not every article needs a tradeoffs section
- Not every article needs measurement tools
- Not every article needs numbered strategies

**The Rule**: Front matter and back matter are sacred. Middle content is flexible.

---

## Platform-Specific Post Guidelines

### LinkedIn Posts (MANDATORY STRUCTURE)

LinkedIn posts are not mini-articles. They are professional summaries that drive clicks to the full piece. The article link at the bottom does the heavy lifting.

**Structure**:
1. **Provocative hook** (1-2 sentences): Open with a surprising fact, uncomfortable truth, or counterintuitive claim that stops the scroll. This is the only part most people will read.
2. **Context** (2-3 sentences): Ground the hook with a credible source, stat, or industry reference. Establish that this is real, not clickbait.
3. **What the article covers** (3-5 sentences): Professional summary of the key points. Not a retelling — a reason to click. Frame it as "I wrote about X covering Y, Z, and W" rather than restating the article's arguments.
4. **Series callout** (1 sentence, if applicable): Position within the series.
5. **Article link**: Clean URL, no CTA fluff like "drop your thoughts below 👇"

**Rules**:
- Target 700-1,000 characters (not 2,000+)
- No hashtags (LinkedIn's algorithm deprioritizes posts with hashtags)
- No emoji-heavy formatting
- No engagement-bait questions at the end
- Professional tone — you're sharing expertise, not performing
- First-person where natural ("I wrote", "most teams I talk to")
- The post should make someone want to read the article, not feel like they already did

**Anti-patterns to avoid**:
- ❌ Restating the entire article's argument with all the data points
- ❌ Bullet-point lists of everything the article covers (use prose)
- ❌ "What do you think? 👇" or "Agree or disagree?"
- ❌ Hashtag blocks at the bottom
- ❌ Posts over 1,500 characters — if it's that long, you're rewriting the article

**Reference**: `articles/quantum-computing/0-why-architects-quantum-now/advertising/linkedin-post.md`

---

## Reference Templates (Advertising)

**Location**: `for-approval/medium/green-coding/1- intro/advertising/`

Use these as examples when creating advertising infrastructure:
- linkedin-post.md - Provocative hook + professional summary (see LinkedIn guidelines above)
- x-post.md - Concise + thread version
- instagram-post.md - Visual, link in bio
- facebook-post.md - Detailed, direct link
- threads-post.md - Conversational
- reddit-post.md - Authentic, discussion-focused
- hashtag-strategy.md - Platform-specific research

---

## Anti-AI-Voice Final Pass (MANDATORY)

**When**: Applied to the final version before publication
**Why**: Readers increasingly detect and discount AI-sounding writing. This pass ensures the article sounds like a real person wrote it, not a model.
**Reference**: [Florian Roth — "I'm Sick of Reading AI-Written Posts"](https://medium.com/@cyb3rops/im-sick-of-reading-ai-written-posts-107767481fbf), [Jejomar Contawe — "The Single Most Prevalent AI Writing Tell"](https://medium.com/ai-ai-oh/the-single-most-prevalent-ai-writing-tell-spoiler-alert-its-not-em-dashes-c56dea4150f4)

### The Five AI Tells to Eliminate

**1. Fake Contrast**
Search for and remove the "Not X. Y." pattern used to sound clever.

❌ Kill these patterns:
- "This is not opinion. This is math."
- "It's not a feature. It's a paradigm shift."
- "Not hype. Reality."
- Any sentence that sets up a false binary just to slam one side down

✅ Replace with: Honest framing that acknowledges nuance. If there's a real contrast, earn it with evidence, don't just assert it.

**2. Absurd Certainty**
Flag and soften absolute language that no honest human would use.

❌ Ban these words/phrases (unless backed by hard data):
- "always", "never", "everyone", "no one"
- "proven", "solved", "permanent"
- "This changes everything"
- "The old way is dead"
- "We now know, with certainty, that…"
- "What happens next will redefine the industry"

✅ Replace with: Qualified, honest language. "In most cases…", "From what I've seen…", "The data suggests…", "There's a strong case that…". Real people hedge. Real people know the topic is bigger than one neat sentence.

**3. Too-Perfect Rhythm**
Break up the formulaic AI cadence: hook → big claim → three neat points → dramatic conclusion.

❌ Kill these patterns:
- Triplet sentence groups: "No vendor. No black box. No negotiation."
- "They don't pause. They don't reflect. They guess."
- Perfectly parallel sentence structures repeated more than twice
- Every section following the exact same internal structure

✅ Replace with: Vary sentence length. Let some paragraphs be one sentence. Let others run long. Mix up section structures. Let the writing breathe unevenly, like a real person thinking out loud.

**4. Desperate Importance**
Strip out language that frames everything as a historic moment.

❌ Kill these patterns:
- "This is the moment everything changed"
- "We are witnessing a fundamental shift in how humans create"
- Treating a benchmark result like a civilizational warning
- Treating a side project like the industrial revolution
- Any sentence designed to make the reader "stop breathing for a second"

✅ Replace with: Let the content speak for itself. If the thing is actually important, the reader will figure that out. State what happened, show the impact with numbers, and move on.

**5. Negation Framing and LLM Parallelism**
The single most prevalent AI writing tell according to [Jejomar Contawe](https://medium.com/ai-ai-oh/the-single-most-prevalent-ai-writing-tell-spoiler-alert-its-not-em-dashes-c56dea4150f4). LLMs compulsively define things by first stating what they're NOT "just about," then pivoting to a supposedly deeper meaning. They also overuse two parallel structures that real humans rarely lean on this heavily.

❌ Kill these patterns:

*Negation-pivot (the #1 tell):*
- "[Topic] isn't just about [basic thing]; it's about [deeper thing]."
- "[Topic] is more than just [X]; it's [Y]."
- "It's not just a [simple framing] — it's a [grander framing]."
- Any sentence that gives meaning to a subject by first stating what it isn't "just about"

*"From… to…" scope parallelism:*
- "From daily budgeting apps to sophisticated investment portfolios…"
- "From startups to Fortune 500 companies…"
- "From design to deployment…"
- LLMs use this to convey topic coverage; humans mostly use it for distance or time range

*"Whether… or…" false inclusivity:*
- "Whether you're a beginner or an expert…"
- "Whether you're an author, entrepreneur, or business owner…"
- LLMs abuse this structure to appear balanced and inclusive; it almost always signals unedited AI output

✅ Replace with: Just say the thing directly. If platform engineering matters to both startups and enterprises, say so in a way that doesn't sound like a brochure. If you need to define something, define it — don't perform the act of redefining it from a shallow version to a deep one. Drop the "whether you're X or Y" opener entirely; your reader knows who they are.

### The Authenticity Checklist (Final Version Only)

Run this checklist on the final version before publication:

- [ ] **Voice check**: Read the article out loud. Does it sound like YOU talking to a colleague, or like a LinkedIn thought leader performing for an audience?
- [ ] **Imperfection check (wabi-sabi)**: Is there at least some roughness? A slightly informal aside, a personal admission, a sentence that's a bit clumsy but clearly yours? Perfection is now a red flag.
- [ ] **Effort signal**: Does the article contain something that clearly required real effort — a personal experience, original data, a specific example from your work, an opinion you'd actually defend in a room full of experts?
- [ ] **Contrast audit**: Search for "not X, Y" and "not X. Y." patterns. Remove or rewrite any that are just rhetorical tricks rather than genuine distinctions.
- [ ] **Certainty audit**: Search for "always", "never", "every", "no one", "proven", "everything", "redefine", "fundamental shift". Soften or remove unless you have receipts.
- [ ] **Rhythm audit**: Read three consecutive paragraphs. If they all follow the same structure (same length, same cadence, same pattern), rewrite at least one to break the pattern.
- [ ] **Importance audit**: Find the most dramatic sentence in the article. Ask: "Would I actually say this to someone's face?" If not, tone it down.
- [ ] **Negation-pivot audit**: Search for "isn't just", "is more than just", "not just about", "it's about". If you're defining something by what it isn't before saying what it is, rewrite to just say what it is.
- [ ] **LLM parallelism audit**: Search for "From [X] to [Y]" and "Whether you're [X] or [Y]" openers. These are the most common unedited-AI-output signals after negation framing. Rewrite or cut.
- [ ] **Synthetic fatigue check**: If you removed the author name, would a reader be able to tell a specific human wrote this? If it could be anyone (or anything), it needs more of you in it.

### Acceptable AI Usage

Using AI for spelling, grammar, and cleaning up drafts is fine. The line is crossed when the text no longer sounds like a person who had something to say. The goal: use AI as a tool to help you write better, not to make you sound like everyone else.

---

## Common Mistakes to Avoid

❌ Creating advertising before v1 is complete
❌ Not updating advertising after major revisions
❌ Modifying existing version files
❌ Skipping SEO optimization
❌ Not including series navigation for series articles
❌ Using same hashtags across all platforms
❌ Posting to Reddit with hashtags
❌ Not documenting changes in TODO.md

---

## Checklist Before Starting

- [ ] Read ARTICLE-WRITING-PROCESS.md completely
- [ ] Understand version control rules
- [ ] Know when to create advertising infrastructure (after v1)
- [ ] Know when to update advertising (after major revisions)
- [ ] Understand SEO requirements
- [ ] Know series article requirements (if applicable)
- [ ] Have reference templates available

---

## Checklist After v1 Complete

- [ ] v1 article written and reviewed
- [ ] TODO.md created
- [ ] advertising/ directory created
- [ ] All 7 advertising files created with article-specific content
- [ ] Character counts verified
- [ ] Hashtags researched
- [ ] TODO.md updated with "Advertising infrastructure created for v1"

---

## Checklist After Each Revision

- [ ] New version file created (v2, v3, etc.)
- [ ] Changes documented in TODO.md
- [ ] Advertising materials reviewed
- [ ] Advertising materials updated (if needed)
- [ ] Update decision documented in TODO.md
- [ ] Character counts still within limits

---

## Checklist Before Publication

- [ ] Final version selected
- [ ] **Series navigation links populated from `articles/published.md`** (no placeholder `(link)` values)
- [ ] All advertising files updated with final article URL
- [ ] SEO checklist complete
- [ ] Series navigation added (if series article)
- [ ] Cover image ready
- [ ] All platform posts ready
- [ ] Posting schedule planned

---

**Status**: Active
**Last Updated**: 2026-03-31
**Version**: 1.1
**Owner**: Content Team
**Full Process**: `for-approval/medium/ARTICLE-WRITING-PROCESS.md`
