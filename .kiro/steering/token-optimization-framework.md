---
inclusion: manual
---

# Steering Document Token Optimization Framework

## Overview

This framework establishes token-efficient standards for all steering documents while maintaining full context and functionality. Optimizations focus on eliminating redundancy, improving structure, and creating cross-document references.

## Optimization Principles

### 1. Hierarchical Information Architecture
- **Overview** → **Core Rules** → **Examples** → **References**
- Front-load critical information
- Use progressive disclosure for details

### 2. Token-Efficient Formatting
- **Headers**: Use concise, descriptive titles
- **Lists**: Prefer bullet points over verbose paragraphs
- **Examples**: Show patterns, not exhaustive cases
- **Cross-References**: Link instead of duplicate

### 3. Content Consolidation Patterns
- **Common Sections**: Extract to shared references
- **Repeated Examples**: Create reusable templates
- **Verbose Explanations**: Convert to concise rules

## Optimized Document Structure

### Standard Template (Token-Efficient)
```markdown
# [Document Title]

## Core Rules
- [Primary rule with rationale]
- [Secondary rules as bullets]

## Quick Reference
| Pattern | Example | Notes |
|---------|---------|-------|
| [Pattern] | [Example] | [Key point] |

## Implementation
### [Scenario 1]
- **Do**: [Concise action]
- **Don't**: [What to avoid]

### [Scenario 2]
- **Pattern**: [Template]
- **Example**: [Brief case]

## Cross-References
- Related: [#document-name]
- See also: [#other-document]

---
**Owner**: [Team] | **Updated**: [Date] | **Version**: [X.Y]
```

## Content Optimization Strategies

### 1. Replace Verbose Sections
**Before** (High Token):
```markdown
## Purpose

This document establishes mandatory standards for organizing specification files and their associated deliverables across the Nagara Platform workspace. These standards ensure consistency, maintainability, and proper cross-repository coordination while following the principle that "created files should go in the same repository that the spec is in."

## Core Principle

**Primary Rule**: All files created as part of implementing a specification MUST be placed in the same repository where the specification itself resides.

**Rationale**: This ensures that specifications and their implementations remain co-located, making it easier to:
- Track deliverables and progress
- Maintain version consistency
- Enable proper code review workflows
- Facilitate knowledge transfer
- Support repository-specific CI/CD processes
```

**After** (Token-Optimized):
```markdown
## Core Rule
**Spec-Implementation Co-location**: All implementation files MUST be in the same repository as their spec.

**Benefits**: Unified tracking, version consistency, streamlined reviews, knowledge transfer, CI/CD alignment.
```

### 2. Consolidate Repetitive Examples
**Before**: Multiple verbose examples per document
**After**: Reference shared example library

### 3. Create Cross-Document Links
**Before**: Duplicate information across documents
**After**: Link to authoritative source

## Shared Reference Library

### Common Patterns
- **Repository Structure**: See [#repo-structure-ref]
- **Naming Conventions**: See [#naming-conventions-ref]
- **Error Handling**: See [#error-handling-ref]
- **Cross-Repo Coordination**: See [#cross-repo-ref]

### Quick Reference Cards
- **ADO Work Item Patterns**: [#ado-patterns-card]
- **File Organization Rules**: [#file-org-card]
- **Code Quality Standards**: [#quality-standards-card]

## Implementation Plan

### Phase 1: Document Audit
1. **Token Analysis**: Measure current usage per document
2. **Redundancy Mapping**: Identify duplicate content
3. **Priority Ranking**: Focus on highest-impact optimizations

### Phase 2: Content Consolidation
1. **Extract Common Sections**: Create shared reference library
2. **Optimize High-Token Documents**: Apply token-efficient patterns
3. **Create Cross-Links**: Replace duplication with references

### Phase 3: Validation
1. **Context Preservation**: Ensure no information loss
2. **Usability Testing**: Validate with real development scenarios
3. **Performance Measurement**: Confirm token reduction

## Optimization Targets

### High-Priority Documents (>2000 tokens)
- `spec-file-organization.md` → Target: 60% reduction
- `error-logging-standards.md` → Target: 50% reduction
- `ado-structure-governance.md` → Target: 55% reduction

### Medium-Priority Documents (1000-2000 tokens)
- `cross-repository-coordination.md` → Target: 40% reduction
- `troubleshooting-documentation-requirements.md` → Target: 45% reduction

### Shared Reference Creation
- **Common Examples Library**: Consolidate repetitive examples
- **Quick Reference Cards**: Create scannable summaries
- **Cross-Document Index**: Enable efficient navigation

## Success Metrics

### Quantitative
- **Token Reduction**: 40-60% across high-priority documents
- **Cross-References**: 80% reduction in duplicate content
- **Load Time**: Faster context loading for AI systems

### Qualitative
- **Context Preservation**: 100% functional information retained
- **Usability**: Improved developer experience
- **Maintainability**: Easier document updates and consistency

---

**Implementation Status**: Framework Complete | **Next**: Document Optimization | **Owner**: Platform Team