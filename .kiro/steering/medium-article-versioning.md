---
inclusion: fileMatch
fileMatchPattern: 'for-approval/medium/**'
---

# Medium Article Version Management

## Core Rule
When writing or revising content in `for-approval/medium/`, NEVER modify the existing version. Always create a new version file.

## Version Naming Convention
- First version: `v1-{descriptive-name}.md`
- Subsequent versions: `v2-{descriptive-name}.md`, `v3-{descriptive-name}.md`, etc.
- Store versions in: `for-approval/medium/{article-topic}/versions/`

## Workflow
1. **Initial Draft**: Create `v1-article-name.md` in versions directory
2. **Revisions**: Create `v2-article-name.md`, `v3-article-name.md`, etc.
3. **Never**: Modify existing version files
4. **Final**: Copy approved version to parent directory as final article

## Example Structure
```
for-approval/medium/green-coding/
├── intro/
│   ├── versions/
│   │   ├── v1-intro-article.md
│   │   ├── v2-intro-article.md
│   │   └── v3-intro-article.md
│   └── intro-article-proposal.md
```

## Rationale
- Preserves revision history
- Allows comparison between versions
- Enables rollback to previous versions
- Documents evolution of content

---

**Status**: Active | **Updated**: 2025-01-28
