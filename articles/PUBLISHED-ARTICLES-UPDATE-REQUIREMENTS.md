---
document-title: Published Articles Update Requirements
document-subtitle: Series Navigation Updates for Already-Published Articles
document-type: Update Specification
document-date: 2025-02-13
document-revision: 1.0
document-author: Kiro AI Assistant
review-cycle: One-time
---

# Published Articles Update Requirements

## Overview

This document specifies the updates required for already-published Medium articles to add series navigation sections. These updates improve reader experience by enabling easy navigation between articles in a series.

**Reference Document**: `for-approval/medium/ARTICLE-WRITING-PROCESS.md`
**Affected Articles**: All articles with "Published" status in `MEDIUM-ARTICLE-RELEASE-SCHEDULE.md`

**Important**: These are LIVE articles on Medium. Updates require editing the published article directly on Medium.com.

---

## Update Strategy

### What to Add

**Series Navigation Section** - Add at the end of each published article, before the author bio.

### What NOT to Change

- **Do NOT add series opening blurb** - These articles are already published and have their own openings
- **Do NOT change existing content** - Only add the navigation section
- **Do NOT modify title, subtitle, or tags** - Keep SEO intact

### Implementation Method

1. Create new version file (e.g., v6 if v5 is latest)
2. Copy latest version content
3. Add series navigation section at end (before author bio)
4. Edit published article on Medium.com
5. Paste series navigation section at end
6. Publish update

---

## Published Articles Requiring Updates

### Green Coding Series

#### Part 1: Why Your Code's Carbon Footprint Matters (PUBLISHED)

**Current Version**: v5
**New Version**: v6
**Medium URL**: [Insert URL]
**Last Updated**: [Check Medium]

**Series Navigation to Add**:

```markdown
---

## Series Navigation

**Next Article**: [Energy-Efficient Algorithm Patterns](link-to-part-2)

**Coming Up**: Database optimization, carbon-aware apps, microservices architecture, DevOps practices, AI/ML sustainability
```

**Implementation Steps**:
1. Create `v6-intro-article.md` in `for-approval/medium/green-coding/1- intro/versions/`
2. Copy v5 content to v6
3. Add series navigation section at end (before author bio)
4. Log into Medium.com
5. Open published article for editing
6. Scroll to end (before author bio)
7. Add horizontal rule (---)
8. Paste series navigation section
9. Update and republish

---

#### Part 2: Energy-Efficient Algorithm Patterns (PUBLISHED)

**Current Version**: v3
**New Version**: v4
**Medium URL**: [Insert URL]
**Last Updated**: [Check Medium]

**Series Navigation to Add**:

```markdown
---

## Series Navigation

**Previous Article**: [Why Your Code's Carbon Footprint Matters (And How to Measure It)](link-to-part-1)

**Next Article**: [Database Optimization Strategies That Cut Energy Costs](link-to-part-3)

**Coming Up**: Carbon-aware apps, microservices architecture, DevOps practices, AI/ML sustainability, language efficiency
```

**Implementation Steps**:
1. Create `v4-ee-algo-patterns.md` in `for-approval/medium/green-coding/2- ee-algo-patterns/versions/`
2. Copy v3 content to v4
3. Add series navigation section at end (before author bio)
4. Edit published article on Medium.com
5. Add series navigation section
6. Update and republish

---

#### Part 3: Database Optimization Strategies (PUBLISHED)

**Current Version**: v5
**New Version**: v6
**Medium URL**: [Insert URL]
**Last Updated**: [Check Medium]

**Series Navigation to Add**:

```markdown
---

## Series Navigation

**Previous Article**: [Energy-Efficient Algorithm Patterns](link-to-part-2)

**Next Article**: [Building Carbon-Aware Applications](link-to-part-4)

**Coming Up**: Microservices architecture, DevOps practices, AI/ML sustainability, language efficiency, workload placement
```

**Implementation Steps**:
1. Create `v6-database-optimization.md` in `for-approval/medium/green-coding/3- eff-database/versions/`
2. Copy v5 content to v6
3. Add series navigation section at end (before author bio)
4. Edit published article on Medium.com
5. Add series navigation section
6. Update and republish

---

#### Part 4: Building Carbon-Aware Applications (PUBLISHED)

**Current Version**: v2
**New Version**: v3
**Medium URL**: https://medium.com/@diverdan326/building-carbon-aware-applications-when-and-where-you-run-code-matters-as-much-as-how-you-write-it-ed312e9fbcdb
**Last Updated**: Feb 10, 2025

**Series Navigation to Add**:

```markdown
---

## Series Navigation

**Previous Article**: [Database Optimization Strategies That Cut Energy Costs](link-to-part-3)

**Next Article**: [Sustainable Microservices Architecture](link-to-part-5) *(Coming soon!)*

**Coming Up**: DevOps practices, AI/ML sustainability, language efficiency, workload placement
```

**Implementation Steps**:
1. Create `v3-carbon-aware-apps.md` in `for-approval/medium/green-coding/4-carbon-aware-apps/versions/`
2. Copy v2 content to v3
3. Add series navigation section at end (before author bio)
4. Edit published article on Medium.com
5. Add series navigation section
6. Update and republish

---

### Communication Series

#### Part 1: Speaking Executive - A Technical Guide to C-Suite Communication (PUBLISHED)

**Current Version**: v5
**New Version**: v6
**Medium URL**: [Insert URL]
**Last Updated**: [Check Medium]

**Series Navigation to Add**:

```markdown
---

## Series Navigation

**Next Article**: [Navigating Executive Disagreement: Stakeholder Dynamics](link-to-part-2) *(Coming soon!)*

**Coming Up**: Technical presentations, architecture reviews, design reviews, technical writing, technical debt
```

**Implementation Steps**:
1. Create `v6-speaking-executive.md` in `for-approval/medium/communication/1- executive-communication/speaking-executive/versions/`
2. Copy v5 content to v6
3. Add series navigation section at end (before author bio)
4. Edit published article on Medium.com
5. Add series navigation section
6. Update and republish

---

### Resilience Engineering Series

#### Part 1: Cell-Based Architecture & Circuit Breakers (PUBLISHED)

**Current Version**: v2
**New Version**: v3
**Medium URL**: [Insert URL]
**Last Updated**: [Check Medium]

**Series Navigation to Add**:

```markdown
---

## Series Navigation

**Next Article**: [Chaos Engineering in Production: Breaking Things on Purpose](link-to-part-2) *(Coming soon!)*

**Coming Up**: Monitoring blind spots, graceful failures, infrastructure apocalypse, rate limiting, bulkhead pattern
```

**Implementation Steps**:
1. Create `v3-cell-based-architecture-circuit-breakers.md` in `for-approval/medium/resliliency/1- cell-based-architecture/versions/`
2. Copy v2 content to v3
3. Add series navigation section at end (before author bio)
4. Edit published article on Medium.com
5. Add series navigation section
6. Update and republish

---

#### Part 2: Chaos Engineering in Production (PUBLISHED)

**Current Version**: Check versions directory
**New Version**: Next version number
**Medium URL**: https://medium.com/@diverdan326/chaos-engineering-breaking-things-on-purpose-so-they-dont-break-by-accident-f7b810eef514
**Last Updated**: Feb 12, 2025

**Series Navigation to Add**:

```markdown
---

## Series Navigation

**Previous Article**: [Cell-Based Architecture & Circuit Breakers](link-to-part-1)

**Next Article**: [The $10M Blind Spot: Why Your Monitoring is Lying to You](link-to-part-3) *(Coming soon!)*

**Coming Up**: Graceful failures, infrastructure apocalypse, rate limiting, bulkhead pattern, incident response
```

**Implementation Steps**:
1. Check current version in `for-approval/medium/resliliency/2-chaos-engineering/versions/`
2. Create next version file
3. Copy current version content
4. Add series navigation section at end (before author bio)
5. Edit published article on Medium.com
6. Add series navigation section
7. Update and republish

---

## Medium Editing Workflow

### Step-by-Step Process

1. **Prepare New Version Locally**
   - Create new version file (increment version number)
   - Copy previous version content
   - Add series navigation section at end
   - Save file

2. **Log into Medium**
   - Go to medium.com
   - Sign in with your account
   - Navigate to "Stories" dashboard

3. **Open Article for Editing**
   - Find the published article
   - Click "Edit" button
   - Article opens in Medium editor

4. **Locate Insertion Point**
   - Scroll to end of article
   - Find author bio section
   - Position cursor BEFORE author bio

5. **Add Series Navigation**
   - Add horizontal rule (type "---" on new line)
   - Copy series navigation section from new version file
   - Paste into Medium editor
   - Format as needed (Medium auto-formats markdown)

6. **Preview Changes**
   - Click "Preview" button
   - Verify navigation section displays correctly
   - Check all links work (if published)
   - Verify formatting is clean

7. **Publish Update**
   - Click "Publish" or "Update story"
   - Confirm publication
   - Verify changes are live

8. **Update Version History**
   - Update TODO.md with new version
   - Note what was changed (added series navigation)
   - Record date of Medium update

---

## Link Management

### Initial Publication (Links Not Yet Available)

When adding navigation to early articles in a series, some links won't exist yet:

**Use this format**:
```markdown
**Next Article**: [Title of Next Article](link) *(Coming soon!)*
```

**Example**:
```markdown
**Next Article**: [Sustainable Microservices Architecture](link-to-part-5) *(Coming soon!)*
```

### Updating Links After Publication

As new articles are published:

1. **Get Medium URL** of newly published article
2. **Update previous articles** with actual link
3. **Remove "Coming soon!" note**
4. **Create new version** documenting the link update

**Before**:
```markdown
**Next Article**: [Sustainable Microservices Architecture](link-to-part-5) *(Coming soon!)*
```

**After**:
```markdown
**Next Article**: [Sustainable Microservices Architecture](https://medium.com/@diverdan326/sustainable-microservices-architecture-abc123)
```

### Link Placeholder Convention

Until actual Medium URLs are available, use placeholder format:

```markdown
[Article Title](link-to-part-N)
```

This makes it easy to find and replace with actual URLs later.

---

## Version Control Best Practices

### Creating New Versions

**Always create a new version when updating published articles**:

1. **Increment version number** (v5 → v6)
2. **Copy previous version** as starting point
3. **Make changes** (add series navigation)
4. **Document changes** in TODO.md
5. **Never modify existing versions**

### Version Naming Convention

```
v{N}-{article-name}.md
```

**Examples**:
- `v6-intro-article.md`
- `v4-ee-algo-patterns.md`
- `v6-database-optimization.md`
- `v3-carbon-aware-apps.md`

### TODO.md Updates

After creating new version, update TODO.md:

```markdown
## Version History
- **v6** (2025-02-13): Added series navigation section for published article
- **v5** (2025-01-28): [Previous changes]
```

---

## Quality Assurance Checklist

Before updating published article on Medium:

- [ ] New version file created locally
- [ ] Previous version content copied to new version
- [ ] Series navigation section added at correct location (before author bio)
- [ ] Horizontal rule (---) added before navigation section
- [ ] Previous article link correct (if not first article)
- [ ] Next article link correct (or "Coming soon!" if not published)
- [ ] "Coming Up" topics listed (3-5 items)
- [ ] All markdown formatting correct
- [ ] TODO.md updated with version history
- [ ] Ready to edit on Medium.com

After updating on Medium:

- [ ] Changes published successfully
- [ ] Navigation section displays correctly
- [ ] Links work (for published articles)
- [ ] Formatting is clean
- [ ] No broken elements
- [ ] Author bio still displays correctly
- [ ] Article still reads well with new section

---

## Timeline and Priorities

### Immediate Priority (This Week)

1. **Green Coding Part 4** (most recent, easiest to update)
2. **Resilience Part 2** (just published Feb 12)
3. **Communication Part 1** (standalone, needs navigation)

### High Priority (Next Week)

1. **Green Coding Part 3** (v5 exists, add navigation)
2. **Green Coding Part 2** (v3 exists, add navigation)
3. **Resilience Part 1** (v2 exists, add navigation)

### Medium Priority (Following Week)

1. **Green Coding Part 1** (v5 exists, add navigation)

### Link Updates (Ongoing)

As new articles are published:
- Update previous articles with actual Medium URLs
- Remove "Coming soon!" notes
- Create new versions documenting link updates

---

## Benefits of These Updates

### For Readers

- **Easy navigation** between articles in series
- **Discovery** of related content
- **Context** about series structure
- **Anticipation** for upcoming topics

### For Author

- **Increased engagement** (readers explore more articles)
- **Better SEO** (internal linking structure)
- **Series cohesion** (articles feel connected)
- **Reader retention** (easier to follow series)

### For Metrics

- **Higher views per reader** (navigation encourages exploration)
- **Lower bounce rate** (readers stay in series)
- **More claps** (engaged readers clap more)
- **Better read ratio** (series readers more committed)

---

## Troubleshooting

### Issue: Can't Find Published Article on Medium

**Solution**:
1. Go to medium.com
2. Click your profile icon
3. Select "Stories"
4. Find article in list
5. Click "Edit"

### Issue: Series Navigation Formatting Looks Wrong

**Solution**:
1. Check horizontal rule (---) is on its own line
2. Verify blank line after horizontal rule
3. Ensure "## Series Navigation" has proper heading format
4. Check bold formatting (**Previous Article**:)
5. Preview before publishing

### Issue: Links Don't Work

**Solution**:
1. Verify Medium URL is correct
2. Check for typos in URL
3. Ensure URL is complete (starts with https://)
4. Test link in browser before adding to article

### Issue: Author Bio Disappeared

**Solution**:
1. Series navigation should be BEFORE author bio
2. Check that you didn't accidentally delete bio
3. Re-add bio if needed
4. Save and republish

---

## Notes

- **Backward Compatibility**: These updates are additive only (no content changes)
- **SEO Impact**: Minimal (only adding internal links, which helps SEO)
- **Reader Impact**: Positive (easier navigation, better experience)
- **Maintenance**: Update links as new articles publish
- **Consistency**: All series articles should have navigation sections

---

## Summary Table

| Series        | Part | Title                                  | Current Ver | New Ver | Priority  | Status  |
| ------------- | ---- | -------------------------------------- | ----------- | ------- | --------- | ------- |
| Green Coding  | 1    | Why Your Code's Carbon Footprint...   | v5          | v6      | Medium    | Pending |
| Green Coding  | 2    | Energy-Efficient Algorithm Patterns    | v3          | v4      | High      | Pending |
| Green Coding  | 3    | Database Optimization Strategies       | v5          | v6      | High      | Pending |
| Green Coding  | 4    | Building Carbon-Aware Applications     | v2          | v3      | Immediate | Pending |
| Communication | 1    | Speaking Executive                     | v5          | v6      | Immediate | Pending |
| Resilience    | 1    | Cell-Based Architecture & Circuit...   | v2          | v3      | High      | Pending |
| Resilience    | 2    | Chaos Engineering in Production        | TBD         | TBD     | Immediate | Pending |

---

**Status**: Active | **Created**: 2025-02-13 | **Owner**: Content Team
**Purpose**: Add series navigation to published Medium articles for better reader experience
**Next Review**: After all 7 articles updated

