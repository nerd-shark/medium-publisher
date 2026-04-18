---
inclusion: manual
applies_to_tools: ["fsWrite", "strReplace", "readFile"]
priority: high
description: "Steering document precedence framework and conflict resolution procedures"
---

# Steering Document Precedence Framework

## Overview

This document establishes the hierarchy rules, conflict detection mechanisms, and resolution procedures for steering documents across the Nagara platform workspace. It ensures consistent AI guidance while allowing repository-specific customization when needed.

## Precedence Hierarchy

### 1. Repository-Local Steering (Highest Precedence)
**Location**: `{Repository}/.kiro/steering-local/`
**Scope**: Repository-specific guidance that overrides workspace-level steering
**Authority**: Repository development teams
**Examples**:
- `Nagara_Backend/.kiro/steering-local/categories/standards/rust-coding-standards.md`
- `Nagara_Frontend/.kiro/steering-local/categories/standards/react-development-patterns.md`
- `Nagara_PMO/.kiro/steering-local/categories/processes/ado-sync-procedures.md`

### 2. Workspace-Level Steering (Medium Precedence)
**Location**: `.kiro/steering/`
**Scope**: Cross-repository coordination and platform-wide standards
**Authority**: Platform architects and cross-functional teams
**Examples**:
- `.kiro/steering/architectural-standards.md`
- `.kiro/steering/cross-repository-coordination.md`
- `.kiro/steering/categories/integration/api-contracts.md`

### 3. ALM-SSDLC Library (Lowest Precedence)
**Location**: `ALM-SSDLC/` (read-only reference)
**Scope**: Enterprise-wide templates and compliance standards
**Authority**: Enterprise architecture and compliance teams
**Examples**:
- `ALM-SSDLC/templates/security-requirements.md`
- `ALM-SSDLC/processes/change-management.md`
- `ALM-SSDLC/standards/documentation-standards.md`

## Conflict Resolution Rules

### Rule 1: Repository-Specific Override Authority
When repository-local steering conflicts with workspace-level steering:
- **Repository-local steering takes precedence**
- **Justification must be documented** in the repository-local document
- **Notification required** to platform architects for awareness

**Example Override Pattern**:
```markdown
---
inclusion: fileMatch
fileMatchPattern: "*.rs"
overrides: ".kiro/steering/categories/standards/code-quality-standards.md"
justification: "Rust-specific memory safety patterns require stricter linting rules than general cross-repository standards"
notification_sent: "2025-01-21"
approved_by: "backend-team-lead"
---

# Rust-Specific Code Quality Standards

## Override Notice
This document overrides workspace-level code quality standards for Rust development.
**Justification**: Rust's ownership system requires specialized linting and testing patterns.
```

### Rule 2: Workspace Coordination Requirements
Repository overrides that affect cross-repository integration must:
- **Document integration impact** in the override justification
- **Coordinate with affected repositories** before implementation
- **Update workspace-level documentation** to reflect the exception

### Rule 3: Enterprise Compliance Preservation
Repository and workspace steering must not override:
- **Security compliance requirements** from ALM-SSDLC Library
- **Audit and governance standards** mandated by enterprise policies
- **Legal and regulatory requirements** specified in enterprise templates

## Validation and Enforcement Tools

### Automated Validation Scripts

#### 1. Precedence Validator
**Location**: `scripts/steering/validate-steering-precedence.sh`
**Purpose**: Detect conflicts and validate override documentation
**Usage**:
```bash
bash scripts/steering/validate-steering-precedence.sh
```

**Checks**:
- Conflicting guidance patterns between workspace and repository levels
- Missing override documentation (justification, notifications)
- Repository structure compliance
- Enterprise compliance alignment

#### 2. Cross-Repository Impact Checker
**Location**: `scripts/steering/check-cross-repo-impact.sh`
**Purpose**: Identify coordination requirements between repositories
**Usage**:
```bash
bash scripts/steering/check-cross-repo-impact.sh
```

**Checks**:
- API contract consistency between backend and frontend
- Deployment coordination across repositories
- Integration pattern alignment
- Security standard consistency
- Cross-reference completeness

### Manual Review Processes

#### Monthly Steering Review
1. **Conflict Resolution Log Review**: Assess resolved and pending conflicts
2. **Override Effectiveness Assessment**: Evaluate if overrides are still necessary
3. **Cross-Repository Coordination Health**: Check alignment between repositories
4. **Enterprise Compliance Verification**: Ensure ALM-SSDLC requirements are met

#### Quarterly Architecture Review
1. **Precedence Framework Effectiveness**: Assess if hierarchy is working
2. **Conflict Pattern Analysis**: Identify recurring conflict types
3. **Process Improvement Recommendations**: Suggest framework enhancements
4. **Training and Documentation Updates**: Update guidance based on learnings

## Override Procedures

### Step 1: Justification Documentation
Repository teams must document:
- **Specific need** for override (technical, performance, security)
- **Impact analysis** on cross-repository coordination
- **Alternative solutions considered** and why they were rejected
- **Mitigation strategies** for any negative impacts

### Step 2: Stakeholder Notification
Required notifications based on override scope:
- **Platform Architect**: All architectural pattern overrides
- **Security Team**: Security standard modifications
- **Cross-Repository Teams**: Integration pattern changes
- **Enterprise Compliance**: ALM-SSDLC deviation requests

### Step 3: Implementation with Tracking
```markdown
# Override Implementation Template
---
override_id: "backend-rust-memory-safety-001"
created_date: "2025-01-21"
created_by: "backend-team-lead"
overrides_document: ".kiro/steering/categories/standards/code-quality-standards.md"
justification: "Rust memory safety requires forbidding unsafe code blocks"
impact_assessment: "No cross-repository impact - backend-specific implementation"
stakeholders_notified: ["platform-architect", "security-team"]
review_date: "2025-04-21"
status: "active"
---
```

## Conflict Resolution Procedures

### Level 1: Automated Resolution
**Scope**: Simple conflicts with clear precedence rules
**Process**: Automated tools apply precedence hierarchy
**Examples**: Repository-local overrides workspace-level for same topic

### Level 2: Team Coordination
**Scope**: Cross-repository impacts requiring alignment
**Process**: Affected teams coordinate resolution
**Timeline**: 5 business days for resolution
**Escalation**: Platform architect if no agreement

### Level 3: Architecture Review
**Scope**: Complex conflicts affecting platform architecture
**Process**: Platform architecture team review and decision
**Timeline**: 10 business days for resolution
**Documentation**: Architectural Decision Record (ADR) created

### Level 4: Enterprise Escalation
**Scope**: Conflicts with enterprise compliance requirements
**Process**: Enterprise architecture and compliance team involvement
**Timeline**: 15 business days for resolution
**Authority**: Enterprise compliance team has final authority

## Monitoring and Metrics

### Key Performance Indicators

#### Conflict Resolution Metrics
- **Mean Time to Resolution (MTTR)**: Average time to resolve steering conflicts
- **Conflict Recurrence Rate**: Percentage of conflicts that reoccur
- **Override Effectiveness**: Success rate of repository overrides
- **Cross-Repository Alignment**: Consistency score across repositories

#### Usage and Adoption Metrics
- **Steering Document Usage**: Frequency of access and reference
- **Override Utilization**: Rate of repository-local overrides
- **Compliance Score**: Adherence to enterprise requirements
- **Developer Satisfaction**: Feedback on steering effectiveness

## Best Practices

### For Repository Teams
1. **Document Overrides Clearly**: Always provide detailed justification
2. **Assess Cross-Repository Impact**: Consider effects on other repositories
3. **Communicate Early**: Notify affected teams before implementing overrides
4. **Regular Review**: Periodically assess if overrides are still needed
5. **Follow Templates**: Use standardized override documentation format

### For Platform Architects
1. **Monitor Conflict Patterns**: Identify systemic issues requiring framework updates
2. **Facilitate Coordination**: Help teams resolve cross-repository conflicts
3. **Maintain Framework**: Keep precedence rules current and effective
4. **Document Decisions**: Create ADRs for significant architectural conflicts
5. **Provide Training**: Ensure teams understand precedence framework

### For Enterprise Compliance
1. **Clear Requirements**: Specify non-negotiable compliance requirements
2. **Regular Updates**: Communicate changes to enterprise standards
3. **Support Teams**: Provide guidance on compliance implementation
4. **Monitor Adherence**: Track compliance across all repositories
5. **Escalation Paths**: Maintain clear escalation procedures for violations

## Framework Evolution

### Continuous Improvement Process
1. **Quarterly Framework Review**: Assess effectiveness and identify improvements
2. **Stakeholder Feedback**: Collect input from all repository teams
3. **Metrics Analysis**: Use KPIs to identify optimization opportunities
4. **Process Refinement**: Update procedures based on lessons learned
5. **Documentation Updates**: Keep framework documentation current

### Version Control and Change Management
- **Framework Versioning**: Track changes to precedence rules and procedures
- **Change Approval**: Require architecture team approval for framework changes
- **Migration Support**: Provide guidance for adapting to framework updates
- **Backward Compatibility**: Ensure existing overrides remain valid during updates

---

**Document Owner**: Platform Architecture Team
**Review Frequency**: Quarterly
**Last Updated**: 2025-01-21
**Next Review**: 2025-04-21
**Version**: 1.0

This framework ensures consistent AI guidance across the Nagara platform while enabling repository-specific customization when justified and properly coordinated.