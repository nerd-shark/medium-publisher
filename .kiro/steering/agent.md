---
inclusion: always
---

# Kiro AI Agent Instructions

## ⚠️ CRITICAL: Windows CMD Shell Only

**MANDATORY**: This workspace uses Windows CMD exclusively!
- **Shell**: cmd.exe (NOT PowerShell, NOT Bash)
- **Command Separator**: `&` (NOT `&&`)
- **Paths**: Backslashes `\` (NOT forward slashes `/`)
- **Variables**: `%VAR%` (NOT `$env:VAR` or `$VAR`)
- **Line Continuation**: `^` (NOT `\` or backtick)

**See "Shell Commands (MANDATORY)" section below for complete reference.**

## Token Budget Monitoring

**Check before acting**: If >50% chance of exceeding 200K tokens, notify user.
**Threshold**: Notify when `(current + estimated) > 180,000` (90% of limit)

## Core File Writing Principles

### Incremental File Creation (MANDATORY)
1. **Write + Append**: Create core structure (40-45 lines), use fsAppend for sections
2. **String Replace**: Create template, use strReplace to expand progressively
3. **Multi-File**: Split large implementations into logical modules

| Scenario | Tool | Notes |
|----------|------|-------|
| New file | `fsWrite` | Initial creation |
| Add content | `fsAppend` | Append sections |
| Targeted edits | `strReplace` | Replace specific parts |
| Multiple edits | Multiple `strReplace` | Parallel when independent |

## Nagara Platform Guidelines

### Spec-Driven Development (MANDATORY)
- **Requirements first**: requirements.md with EARS patterns
- **Design before code**: design.md with architecture
- **Task breakdown**: tasks.md for implementation
- **Track deliverables**: deliverables.md updated continuously
- **User approval required**: Each phase (requirements → design → tasks)
- **One task at a time**: Execute single task, stop for review
- **Test verification required**: MANDATORY - All tests must pass before marking task complete

### Test Verification Before Task Completion (MANDATORY)

**CRITICAL RULE**: A task CANNOT be marked complete unless ALL tests created in that task pass without errors.

**Verification Process**:
1. **After writing tests**: Run tests immediately to verify they can import modules
2. **After implementation**: Run all tests for that task to verify they pass
3. **Before marking complete**: Run full test suite one final time
4. **Document results**: Include test run output in task implementation report

**Test Execution**:
```cmd
REM Run specific test file
python -m pytest path\to\test_file.py -v

REM Run specific test class
python -m pytest path\to\test_file.py::TestClassName -v

REM Run with detailed output
python -m pytest path\to\test_file.py -v --tb=short
```

**Failure Handling**:
- If tests fail, fix implementation until they pass
- Maximum 2 attempts to fix failing tests
- After 2 attempts, document issue and ask user for guidance
- NEVER mark task complete with failing tests

**Task Report Requirements**:
- Include test execution command used
- Include test results (passed/failed counts)
- Document any test failures and fixes applied
- Confirm all tests passing before finalizing report

### EARS Requirements Pattern (MANDATORY)
- **Ubiquitous**: THE {system} SHALL {response}
- **Event-driven**: WHEN {trigger}, THE {system} SHALL {response}
- **State-driven**: WHILE {condition}, THE {system} SHALL {response}
- **Unwanted event**: IF {condition}, THEN THE {system} SHALL {response}
- **Optional feature**: WHERE {option}, THE {system} SHALL {response}
- **Complex**: [WHERE] [WHILE] [WHEN/IF] THE {system} SHALL {response}

### Repository Organization

**Core Directories**:
- **Nagara_PMO**: Specs, docs, ADO sync, project coordination (workspace root)
- **products/**: Individual Nagara product implementations
- **shared/**: Cross-product code (libraries, infrastructure)
- **ALM-SSDLC-Library**: SDLC reference (read-only, access via Nagara-Kensaku)
- **scripts/**: Automation (Python, PowerShell)
- **logs/**: Centralized logging (errors, access, performance, debug)

**Nagara Products** (in products/):
- **nagara-kozo**: Infrastructure platform (K8s orchestration, Promise/Work controllers)
- **nagara-kanri**: Automated audit and requirements analysis
- **nagara-hoshin**: Project documentation generation
- **nagara-kensaku**: Web scraper, search indexing, ALM-SSDLC retrieval
- **nagara-rekishi**: Documentation backfill and analysis
- **nagara-seisa**: Document evaluation and quality assessment
- **nagara-shinzui**: Core essence extraction
- **nagara-kigyo**: Enterprise integration
- **nagara-mado**: Window/interface management

**File Placement (Co-Location)**:

**CRITICAL**: Spec directories contain ONLY documentation. Implementation files go in the target repository root!

**Spec Documentation Location**:
- **Workspace specs**: `.kiro/specs/{spec-name}/` for cross-product features
- **Product specs**: `products/{product}/.kiro/specs/{spec-name}/`
- **PMO specs**: `Nagara_PMO/.kiro/specs/{spec-name}/`
- **Repository specs**: `{repository}/.kiro/specs/{spec-name}/` for repository-specific features

**Spec Directory Contents (ONLY)**:
- `requirements.md` - EARS requirements
- `design.md` - Architecture and design
- `tasks.md` - Implementation task breakdown
- `deliverables.md` - Tracking document (updated continuously)
- `task-N-implementation-report.md` - Per-task reports
- `troubleshooting-log.md` - Debug documentation (if needed)

**Implementation Files Location (MANDATORY)**:
- **Workspace specs** → Implementation in target repository root (e.g., `ALM-SSDLC-Library/terraform/`, `scripts/python/`)
- **Product specs** → Implementation in product root (e.g., `products/nagara-kozo/src/`, `products/nagara-kanri/lambda/`)
- **PMO specs** → Implementation in PMO root (e.g., `Nagara_PMO/scripts/`, `Nagara_PMO/documents/`)
- **Repository specs** → Implementation in repository root (e.g., `ALM-SSDLC-Library/src/`, `Nagara_Backend/api/`)

**Examples**:
```
# CORRECT - Workspace spec for ALM-SSDLC infrastructure
.kiro/specs/alm-ssdlc-storage-execution/
├── requirements.md
├── design.md
├── tasks.md
├── deliverables.md
└── task-N-implementation-report.md

ALM-SSDLC-Library/
├── terraform/          # ← Implementation files here
│   ├── modules/
│   └── examples/
└── lambda/             # ← Lambda code here

# CORRECT - Product spec for Nagara-Kanri
products/nagara-kanri/.kiro/specs/audit-agent/
├── requirements.md
├── design.md
└── tasks.md

products/nagara-kanri/
├── src/                # ← Implementation files here
│   ├── agents/
│   └── services/
└── tests/

# WRONG - Implementation in spec directory
.kiro/specs/alm-ssdlc-storage-execution/
└── terraform/          # ❌ NEVER put implementation here!
```

**Rule**: Spec directories are for planning and tracking. Implementation goes in the repository being modified.

### Python Development (MANDATORY)

**Version**: Python 3.11+, use venv/poetry

**Logging (MANDATORY)**:
```python
from nagara_logger import NagaraLogger
self.logger = NagaraLogger("component_name")
self.logger.info("Message", work_item_id=id, operation="op", context="details")
```
- **No print statements** (except CLI help)
- **Context-aware**: Include operation, work_item_id, context
- **Exceptions**: Use logger.exception() with full context

**Code Quality**:
- **Formatter**: Black (line length 100)
- **Linter**: Ruff
- **Type Checking**: mypy strict mode
- **Docstrings**: Google style
- **Naming**: snake_case (functions/vars), PascalCase (classes), UPPER_CASE (constants)

**Type Hints (MANDATORY)**:
```python
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

def process_item(item_id: str, config: Dict[str, Any]) -> Optional[ProcessResult]:
    """Process item with configuration."""
    pass

class ItemConfig(BaseModel):
    name: str
    timeout: int = 30
```

**Error Handling**:
```python
try:
    self.logger.info("Processing", work_item_id=id, operation="process")
    result = self._do_processing(id)
    self.logger.info("Complete", work_item_id=id, operation="process")
    return result
except ValidationError as e:
    self.logger.error("Validation failed", work_item_id=id, operation="process", context=str(e))
    raise
except Exception as e:
    self.logger.exception("Unexpected error", work_item_id=id, operation="process")
    raise ProcessingError(f"Failed {id}") from e
```

**Testing**: pytest, 80% coverage minimum, mirror src/ structure

**Project Structure**:
```
product/
├── src/
│   ├── main.py
│   ├── api/
│   ├── models/
│   ├── services/
│   └── config.py
├── tests/
│   ├── unit/
│   └── integration/
├── requirements.txt
└── README.md
```

### ADO Work Item Management (MANDATORY)
- **Single Source**: ONLY Epic JSON in `Nagara_PMO/documents/project/work-item-documents/single-source-of-truth/epic-{N}.json`
- **Never delete**: Mark as "Removed" state
- **Sync first**: ALWAYS pull from ADO before modifying
- **Naming**:
  - Epic: `E.{N}: {Title}`
  - Feature: `F.{E}.{N}: {Title}`
  - Story: `S.{E}.{F}.{N}: {Title}`
  - Task: `T.{E}.{F}.{S}.{N}: {Title}`
- **Update discussions**: Use Python script with structured completion

### CI/CD and Automation (MANDATORY)

**CRITICAL**: This workspace uses **Azure DevOps** for CI/CD, NOT GitHub Actions!

- **Platform**: Azure DevOps (ADO)
- **Pipeline Location**: `azure-pipelines/` directory in repository root
- **Pipeline Format**: YAML (azure-pipelines.yml)
- **Triggers**: Branch policies, scheduled, manual
- **Agents**: Microsoft-hosted or self-hosted agents

**Pipeline Structure**:
```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - feature/*
  paths:
    include:
      - 'path/to/watch/**'

schedules:
  - cron: "0 2 * * 1"  # Weekly on Monday at 2 AM
    displayName: Weekly scheduled run
    branches:
      include:
        - main

pool:
  vmImage: 'ubuntu-latest'

stages:
  - stage: Build
    jobs:
      - job: BuildJob
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '3.11'
          - script: |
              python scripts/your-script.py
            displayName: 'Run automation'
```

**Common ADO Tasks**:
- `UsePythonVersion@0`: Set Python version
- `PublishBuildArtifacts@1`: Publish artifacts
- `PublishTestResults@2`: Publish test results
- `CreatePullRequest@1`: Create PR (custom task)

**When to Use ADO Pipelines**:
- Scheduled automation (weekly/monthly maintenance)
- PR validation (lint, test, validate)
- Deployment automation
- Document generation and processing
- Cross-reference updates

**Never Use**:
- ❌ GitHub Actions
- ❌ GitLab CI
- ❌ Jenkins (unless specifically required)

### Core Technology Stack

**Languages by Product**:
- **Infrastructure (Kozo, Mado)**: Rust (kube-rs, Tokio, K8s controllers)
- **Agents (Kanri, Hoshin, Kensaku, etc.)**: Python 3.11+ (async/await)
- **Frontend/UI**: React + TypeScript, Backstage
- **Shared**: Python (cross-product), Rust (performance-critical)

**Stack**:
- **Python**: FastAPI, asyncio, pydantic, pytest, black, ruff, mypy
- **Rust**: kube-rs, Tokio, serde, tracing, clippy
- **Infrastructure**: Kubernetes (EKS), Helm, CRDs
- **Integration**: Azure DevOps, ServiceNow, Okta, Vault
- **Observability**: OpenTelemetry, Jaeger, Prometheus, Grafana
- **Pattern**: Promise/Work for K8s orchestration
- **Logging**: Nagara-Logger (Python package)

### Security (MANDATORY)
- **No hardcoded credentials**: Use AWS Secrets Manager, Vault
- **Encryption**: TLS in transit, KMS at rest
- **Authentication**: AWS Organization SSO, Okta SAML/OIDC
- **RBAC**: Role-based access for all operations
- **Network**: Jabil internal only, VPC restrictions
- **Container**: CIS benchmark compliance
- **Audit**: CloudTrail, SIEM integration

## Development Workflows

### Creating New Specs (MANDATORY)
1. **Feature name**: kebab-case (e.g., "promise-controller")
2. **Create directory**: `.kiro/specs/{feature-name}/`
3. **Create spec-config.yaml** (MANDATORY FIRST STEP):
   - Define affected repositories (which repos will be modified)
   - Set branch strategy (feature, bugfix, hotfix, etc.)
   - Define PR delivery points (logical milestones for incremental PRs)
   - Configure branch naming patterns
   - Link to ADO work item if exists
4. **Research**: Use Nagara-Kensaku for ALM-SSDLC templates
5. **Write requirements.md**: Introduction, Glossary, User stories with EARS criteria
6. **Get approval**: userInput with reason='spec-requirements-review'
7. **Write design.md**: Overview, Architecture, Components, Data Models, Error Handling
8. **Get approval**: userInput with reason='spec-design-review'
9. **Write tasks.md**: Implementation breakdown (max 2-level hierarchy), reference requirements
   - **REMINDER**: Insert PR delivery tasks at logical milestones (see "PR Delivery Tasks" section)
   - **REMINDER**: Insert branch creation tasks after each PR delivery point
10. **Get approval**: userInput with reason='spec-tasks-review'
11. **Create deliverables.md**: Track outputs, files, progress

### Spec Configuration (MANDATORY)

**File**: `spec-config.yaml`
**Location**: `.kiro/specs/{spec-name}/spec-config.yaml`
**Purpose**: Define affected repositories and enable automated branch creation via agent hooks

**Format**:
```yaml
# Spec Configuration
spec:
  name: "feature-name"
  type: "feature" # feature, bugfix, infrastructure, documentation
  status: "planning" # planning, in-progress, completed, archived

# Affected Repositories
affected_repositories:
  - name: "Nagara-Chishiki"
    path: "Nagara-Chishiki"
    branch_strategy: "feature" # feature, hotfix, release
    create_branch: true
    branch_name: "feature/{spec-name}"
    
  - name: "Nagara_PMO"
    path: "Nagara_PMO"
    branch_strategy: "feature"
    create_branch: true
    branch_name: "feature/{spec-name}"

# Branch Configuration
branching:
  base_branch: "main" # or "master", "develop"
  auto_create: true # Enable automatic branch creation via agent hook
  naming_pattern: "feature/{spec-name}" # feature/, bugfix/, hotfix/, docs/
  
# Pull Request Delivery Points (MANDATORY for incremental PRs)
pr_delivery_points:
  - id: "pr-1"
    name: "Documentation Phase"
    after_task: 2  # Task number after which to submit PR
    status: "pending"  # pending, submitted, merged, abandoned
    pr_urls: {}  # Populated by submit-spec-pr hook
    pr_ids: {}  # Populated by submit-spec-pr hook
    submitted_at: null
    merged_at: null
    next_branch_name: "feature/{spec-name}-phase-2"  # Branch to create after merge
    title: "[{spec-name}] Phase 1 Documentation"
    body: |
      ## Overview
      Documentation phase complete
      
      ## Changes
      - Updated architecture docs
      - Updated design docs
      
      ## Next Steps
      - Review and approve before implementation
    reviewers:
      - "platform-engineering@jabil.com"
    labels:
      - "documentation"
      - "phase-1"

# Integration Points (optional)
integration:
  ado_work_item: "1234567" # Link to ADO work item
  related_specs: [] # Related spec names
  dependencies: [] # Dependency specs that must complete first
```

**IMPORTANT**: When creating spec-config.yaml:
1. **ALWAYS include pr_delivery_points** if spec will use incremental PRs
2. Define logical delivery points (e.g., after documentation, after config, after dev deployment)
3. Each delivery point needs: id, name, after_task, next_branch_name, title, body, reviewers
4. Set status to "pending" initially
5. Leave pr_urls, pr_ids, submitted_at, merged_at as null/empty (filled by hooks)

**Repository Path Examples**:
- **Workspace root repos**: `Nagara-Chishiki`, `Nagara_PMO`, `ALM-SSDLC-Library`
- **Product repos**: `products/nagara-kozo`, `products/nagara-kanri`
- **Shared repos**: `shared/libraries/nagara-logger`, `shared/infrastructure`

### PR Delivery Tasks in tasks.md (REMINDER)

**IMPORTANT**: When creating tasks.md, remember to insert PR delivery tasks at logical milestones.

**PR Delivery Task Template**:
```markdown
- [ ] X. Submit PR for [Phase Name]
  - Review all completed tasks
  - Verify deliverables.md is up to date
  - Click "📤 Submit PR" button in Agent Hooks panel
  - Wait for PR review and approval
  - _Requirements: All_

- [ ] X+1. Create Next Branch After PR Merge
  - Verify PR is merged in ADO
  - Click "🌿 Create Next Branch" button in Agent Hooks panel
  - Agent will verify merge and create branches automatically
  - Agent will switch to new branch locally
  - Continue with next phase tasks
  - _Requirements: All_
```

**Example Integration** (after Task 2 - Documentation Phase):
```markdown
- [x] 2. Update Design Documentation
  - Update Detailed Design Document
  - Document alarm thresholds
  - _Requirements: All_

- [ ] 3. Submit PR #1 - Documentation Phase
  - Review Tasks 0-2 completion
  - Verify deliverables.md updated
  - Click "📤 Submit PR" button
  - Wait for PR review and merge
  - _Requirements: All_

- [ ] 4. Create Branch for Configuration Phase
  - Verify PR #1 is merged
  - Click "🌿 Create Next Branch" button
  - Agent verifies merge and creates feature/{spec-name}-config branch
  - Agent switches to new branch locally
  - _Requirements: All_

- [ ] 5. Update Terraform Configuration
  - Update main.tf
  - Add variables
  - _Requirements: All_
```

**Benefits**:
- **Explicit milestones**: Clear PR submission points in task list
- **User reminder**: Tasks prompt user to use agent hooks
- **Workflow integration**: PR tasks are part of normal task execution
- **Tracking**: PR submission and branch creation tracked in tasks.md

**Branch Strategy Types**:
- **feature**: New features, enhancements (branch: `feature/{spec-name}`)
- **bugfix**: Bug fixes (branch: `bugfix/{spec-name}`)
- **hotfix**: Critical production fixes (branch: `hotfix/{spec-name}`)
- **release**: Release preparation (branch: `release/{version}`)
- **docs**: Documentation only (branch: `docs/{spec-name}`)
- **infrastructure**: Infrastructure changes (branch: `infra/{spec-name}`)

**Agent Hook Integration**:
When a new spec is created with `spec-config.yaml`, the AI agent automatically:
1. Reads the `affected_repositories` list from spec-config.yaml
2. For each repository with `create_branch: true`:
   - Uses ADO MCP `mcp_ado_repo_get_repo_by_name_or_id` to get repository details
   - Uses ADO MCP `mcp_ado_repo_get_branch_by_name` to check if branch exists
   - Uses ADO MCP `mcp_ado_repo_create_branch` to create branch from `base_branch`
   - Updates spec-config.yaml with branch creation status and timestamp
3. Logs branch creation results in deliverables.md

**Agent Hook Configuration**:
Create an agent hook that triggers when a new spec directory is created:
- **Trigger**: When `.kiro/specs/{spec-name}/spec-config.yaml` is created
- **Action**: Agent reads config and uses ADO MCP tools to create branches
- **No script needed**: Agent handles this directly using MCP tools

**ADO MCP Tools Used**:
- `mcp_ado_repo_get_repo_by_name_or_id`: Get repository details by name
- `mcp_ado_repo_get_branch_by_name`: Check if branch already exists
- `mcp_ado_repo_create_branch`: Create new branch from base branch
- `mcp_ado_repo_list_branches_by_repo`: List all branches (optional verification)

**Spec-Config.yaml Example (Multi-Repo)**:
```yaml
spec:
  name: "chishiki-infra-phase1"
  type: "infrastructure"
  status: "in-progress"

affected_repositories:
  - name: "Nagara-Chishiki"
    path: "Nagara-Chishiki"
    branch_strategy: "feature"
    create_branch: true
    branch_name: "feature/chishiki-infra-phase1"
    branch_created: true
    branch_created_at: "2025-01-22T10:30:00Z"
    
  - name: "Nagara_PMO"
    path: "Nagara_PMO"
    branch_strategy: "feature"
    create_branch: true
    branch_name: "feature/chishiki-infra-phase1-docs"
    branch_created: true
    branch_created_at: "2025-01-22T10:30:05Z"

branching:
  base_branch: "main"
  auto_create: true
  naming_pattern: "feature/{spec-name}"
  
integration:
  ado_work_item: "7654321"
  related_specs: []
  dependencies: []
```

**Benefits**:
- **Automated Branch Management**: Agent hooks create branches automatically
- **Multi-Repo Coordination**: Track which repos are affected by spec
- **Branch Naming Consistency**: Enforce naming conventions
- **Audit Trail**: Track when branches were created
- **Integration**: Link specs to ADO work items and dependencies

### Executing Spec Tasks (MANDATORY)

**FIRST TASK**: Create deliverables.md
**FIRST STEP**: Create task-{N}-implementation-report.md, review previous task report
**EVERY STEP**: Update deliverables.md when artifacts written/updated/removed
**LAST STEP OF SUBTASK**: Update task report with subtask completion
**SECOND TO LAST STEP OF TASK**: Commit and push changes using Task Completion Committer hook
**LAST STEP OF TASK**: Finalize task report

**Execution**:
1. **Create task report**: `task-{N}-implementation-report.md`
2. **Review previous**: Read previous task report for context
3. **Read context**: requirements.md, design.md, tasks.md
4. **One task**: Focus on single task, don't auto-proceed
5. **Skip optional**: Tasks marked `*` are optional
6. **Update deliverables**: Document all files, directories, changes
7. **Update task report**: Document subtask completion
8. **Update ADO**: Use Python script with structured format
9. **Commit changes**: Use Task Completion Committer hook to commit and push all changes
10. **Finalize report**: Complete task report before marking done
11. **Stop**: Let user review before next task

**Testing**: Implement first, limit verification to 2 attempts, prompt user after 2 attempts

### Token Bloat Prevention (CRITICAL)

**Problem**: Task reports and deliverables grow exponentially, causing token overflow
**Solution**: Enforce strict token limits and content discipline

**Mandatory Practices**:
1. **Review previous reports** - Check token count before creating new ones
2. **Consolidate when needed** - Merge similar subtasks into single entries
3. **Archive completed phases** - Move old task reports to `_archive/` after major milestones
4. **Use references** - Link to code files instead of describing implementation details
5. **Standardize language** - Use consistent, abbreviated terminology

**Token Monitoring**:
- **Task Report**: <500 tokens each (HARD LIMIT)
- **Deliverables**: <800 tokens total (HARD LIMIT)
- **Combined Reports**: <5000 tokens per spec (WARNING THRESHOLD)

**Enforcement Actions**:
- **>500 tokens**: Immediately refactor task report
- **>800 tokens**: Consolidate deliverables document
- **>5000 tokens**: Archive old reports, create fresh tracking documents

**Quality Gates**:
- [ ] Task report under 500 tokens
- [ ] Deliverables under 800 tokens  
- [ ] No duplicate information across documents
- [ ] Essential information only

### Writing Tests (MANDATORY PRE-TEST REVIEW)

**CRITICAL**: Before writing ANY test, you MUST review the code being tested!

**Pre-Test Review Checklist (MANDATORY)**:

Before writing a single line of test code, you MUST:

1. **Read the implementation file completely**:
   - [ ] Identify the actual class/function names
   - [ ] Check actual method signatures (names, parameters, return types)
   - [ ] Verify import paths for the code under test
   - [ ] Note any dependencies the code uses

2. **Review exception handling**:
   - [ ] Read the exceptions module to see what exceptions exist
   - [ ] Check which exceptions the code actually raises
   - [ ] Verify exception names (don't assume they exist)
   - [ ] Check exception hierarchy and inheritance

3. **Check dependencies and imports**:
   - [ ] Identify what modules/classes the code imports
   - [ ] Note the actual import paths used
   - [ ] Check if dependencies need mocking
   - [ ] Verify mock patch paths match where imports are used

4. **Understand the API contract**:
   - [ ] What are the actual method names?
   - [ ] What parameters do they accept?
   - [ ] What do they return?
   - [ ] What exceptions do they raise?

**Common Test Writing Mistakes to Avoid**:

❌ **WRONG - Assuming method names**:
```python
# Assumed method name without checking
generator.generate_document(...)  # Method doesn't exist!
```

✅ **CORRECT - Use actual method names**:
```python
# After reading adhoc_generator.py, found actual method
generator.generate_from_markdown(...)  # Actual method
```

❌ **WRONG - Assuming exception names**:
```python
# Assumed exception without checking exceptions.py
from exceptions import FootnoteGenerationError  # Doesn't exist!
```

✅ **CORRECT - Use actual exceptions**:
```python
# After reading exceptions.py, found actual exception
from exceptions import FootnoteInsertionError  # Actual exception
```

❌ **WRONG - Wrong mock patch paths**:
```python
# Patching where class is defined, not where it's used
with patch('module.submodule.ClassName'):  # Wrong!
```

✅ **CORRECT - Patch where imported**:
```python
# Patching where class is imported and used
with patch('code_under_test.ClassName'):  # Correct!
```

**Test Writing Workflow (MANDATORY)**:

1. **STOP - Read First**:
   - Open the file you're testing
   - Read the entire class/module
   - Take notes on actual names and signatures

2. **Verify Dependencies**:
   - Check what the code imports
   - Identify what needs mocking
   - Verify import paths

3. **Check Exceptions**:
   - Read the exceptions module
   - List actual exception names
   - Note exception hierarchy

4. **Write Test Skeleton**:
   - Use actual class/method names
   - Use actual exception types
   - Use correct import paths

5. **Implement Tests**:
   - Mock at correct import locations
   - Use actual method signatures
   - Test actual behavior

**Example: Proper Test Writing Process**:

```python
# STEP 1: Read adhoc_generator.py
# Found: class AdHocWordGenerator
# Found: method generate_from_markdown(markdown_path, template_path, output_path, metadata, require_footnotes)
# Found: imports FootnoteParser from content_processing.footnote_parser
# Found: imports S3DocumentUploader from infrastructure.s3_uploader

# STEP 2: Read exceptions.py
# Found: FootnoteInsertionError (not FootnoteGenerationError!)
# Found: S3UploadError
# Found: FootnoteParsingError

# STEP 3: Write test with actual names
def test_s3_error_propagates():
    # Mock where S3DocumentUploader is imported (in adhoc_generator)
    with patch('nagara_doc_generator.infrastructure.s3_uploader.S3DocumentUploader') as mock:
        mock.return_value.upload_standard.side_effect = S3UploadError("Bucket not found")
        
        generator = AdHocWordGenerator()  # Actual class name
        
        with pytest.raises(S3UploadError):  # Actual exception name
            generator.generate_from_markdown(  # Actual method name
                markdown_path=Path("test.md"),
                template_path=Path("template.docx"),
                output_path=Path("output.docx"),
                require_footnotes=True
            )
```

**Enforcement**:
- If you write tests without reading the implementation first, STOP
- If you use method/class names without verifying them, STOP
- If you import exceptions without checking they exist, STOP
- If you mock without verifying import paths, STOP

**This is not optional. This is MANDATORY for all test writing.**

### Task Implementation Reports (Token-Efficient)

**CRITICAL**: Maintain token efficiency to prevent bloat over time. Reports MUST be concise and focused.

**File**: `task-{N}-implementation-report.md`
**Location**: `.kiro/specs/{spec-name}/`
**Token Target**: <500 tokens per report

**Mandatory Format** (NO DEVIATIONS):
```markdown
# Task {N} Implementation Report

## Overview
**Task**: {Name}
**Requirements**: {IDs}
**Status**: {Status}
**Started**: {Date}

## Subtask Checklist
- [x] {N}.1 {Subtask}
- [ ] {N}.2 {Subtask}

## Implementation Details

### {N}.1 {Subtask}
**Status**: Complete
**Files Created**: core/template_analyzer.py
**Functions**: analyze_template(), get_slide_layouts()
**Technical Changes**: 
- PPTX loading with python-pptx
- Placeholder detection with PlaceholderType enum
- NagaraLogger integration
**Validation**: Code compiles, follows patterns

## Next Steps
Subtask {N}.2: {Next subtask name}

## Issues & Decisions
- {Key decision with rationale}
```

**Token Efficiency Rules** (MANDATORY):
1. **No verbose descriptions** - Use bullet points only
2. **No duplicate information** - Reference other docs instead of repeating
3. **Limit technical details** - Focus on key changes only
4. **Use abbreviations** - "Complete" not "Successfully completed"
5. **Single line per item** - No multi-paragraph explanations
6. **Essential info only** - Skip obvious or redundant details

**Anti-Bloat Enforcement**:
- **Max 15 lines** per subtask section
- **Max 5 bullets** per technical changes
- **Max 3 items** per issues & decisions
- **No screenshots** or large code blocks
- **No copy-paste** from other documents

### Deliverables Tracking (Token-Efficient)

**File**: `deliverables.md`
**Update**: EVERY STEP when artifacts change
**Token Target**: <800 tokens total

**Mandatory Format** (NO EXPANSIONS):
```markdown
# {Spec} - Deliverables

## Overview
**Project**: {Name}
**Location**: {Path}
**Start**: {Date}
**Status**: {Phase} ({Status})

## Current Phase
**Phase**: {Name}
**Progress**: {Tasks done/total}

## Completed Deliverables

### Documents
**Location**: {Path}
- **`file.md`** - Purpose

### Code Files
**Location**: {Path}
- **`file.py`** - Purpose, key functions

### Tests
**Location**: {Path}
- **`test_file.py`** - Coverage, purpose

## Metrics
- Files created: {count}
- Files modified: {count}
- Lines of code: {count}
- Test coverage: {%}

## Integration Points
[Bullets]
```

**Token Efficiency Rules** (MANDATORY):
1. **No verbose sections** - Skip "Lessons Learned", "Directory Structure" unless critical
2. **One line per file** - No multi-line descriptions
3. **Essential metrics only** - Skip redundant counts
4. **Bullet format** - No paragraph explanations
5. **Update incrementally** - Add items, don't rewrite sections

**Bloat Prevention**:
- **Max 50 lines** total document length
- **Max 10 items** per deliverable category
- **No duplicate information** from task reports
- **No detailed explanations** - keep descriptions under 10 words

### Cross-Product Coordination
1. **Identify primary**: Where main implementation lives
2. **Document dependencies**: API contracts, integration points
3. **Version compatibility**: Semantic versioning
4. **Integration testing**: Contract testing
5. **Communication**: Document APIs, 2-week notice for breaking changes
6. **Shared resources**: Use `shared/libraries/`, `shared/infrastructure/`
7. **Deployment**: Sequential (breaking) or Parallel (compatible)
8. **Product integration**: Nagara-Kozo platform, Nagara-Logger, AWS SSO, multi-access interfaces
9. **Knowledge retrieval**: Use Nagara-Kensaku for ALM-SSDLC content

### API Contract Standards

**URL Pattern**: `/api/v{major}/{resources}`

| Pattern | Method | Purpose |
|---------|--------|---------|
| `/api/v1/{resources}` | GET | List |
| `/api/v1/{resources}` | POST | Create |
| `/api/v1/{resources}/{id}` | GET | Get |
| `/api/v1/{resources}/{id}` | PUT | Update |
| `/api/v1/{resources}/{id}` | DELETE | Delete |

**Status Codes**: 200 (success), 201 (created), 204 (no content), 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 409 (conflict), 422 (validation), 500 (server error)

**Response Format**:
```json
{
  "data": {},
  "meta": {"request_id": "uuid", "timestamp": "ISO8601", "version": "v1"},
  "links": {"self": "/api/v1/resource/id"}
}
```

**Error Format**:
```json
{
  "error": {"code": "CODE", "message": "Message", "details": []},
  "meta": {"request_id": "uuid", "timestamp": "ISO8601"}
}
```

## Shell Commands (MANDATORY)

**CRITICAL**: This workspace uses Windows CMD exclusively. NEVER use PowerShell commands!

### Shell: Windows CMD Only
- **Platform**: Windows (win32)
- **Shell**: cmd.exe
- **Command Separator**: `&` (NOT `&&`)
- **Line Continuation**: `^` at end of line
- **Variables**: `%VARIABLE%` (NOT `$env:VARIABLE`)

### CMD Command Reference

**File Operations**:
```cmd
REM List files
dir

REM Remove file
del file.txt

REM Remove directory
rmdir /s /q dirname

REM Copy file
copy source.txt destination.txt

REM Create directory
mkdir dirname

REM View file content
type file.txt

REM Change directory (use 'cd' or provide path parameter to executePwsh)
cd path\to\directory
```

**Common Patterns**:
```cmd
REM Multiple commands (use & separator)
cd src & python script.py

REM Check if file exists
if exist file.txt echo File exists

REM Environment variables
echo %PATH%
set MY_VAR=value
echo %MY_VAR%
```

### Python Scripts (Windows CMD)
```cmd
REM ADO Sync
python scripts\python\ado_sync\sync_json_to_ado.py --dry-run
python scripts\python\ado_sync\sync_json_to_ado.py
python scripts\python\ado_sync\validate_ado_hierarchy.py

REM Work Item Updates (use ^ for line continuation)
python scripts\python\ado_sync\update_single_work_item.py ^
  --work-item-id 1234567 ^
  --completion-summary "Summary" ^
  --files-modified "file1.rs,file2.rs" ^
  --functions-implemented "func1(),func2()" ^
  --technical-changes "change1,change2" ^
  --tests-added "tests" ^
  --validation-notes "validation"

REM Parent Progress
python scripts\python\ado_sync\update_single_work_item.py ^
  --work-item-id 1234567 ^
  --add-comment "Progress update"
```

### Rust Development (CMD)
```cmd
cargo build --release
cargo test --all-features
cargo clippy -- -D warnings
kubectl apply -f config\crd\
helm install nagara-platform .\charts\
```

### Git Commands (CMD)
```cmd
REM Status
git status

REM Add files
git add .

REM Commit
git commit -m "Message"

REM Push
git push origin master

REM Pull
git pull origin master

REM Submodule operations
git submodule add https://url.git path
git submodule update --init --recursive
git submodule status
```

### AWS CLI (CMD)
```cmd
REM S3 operations
aws s3 ls s3://bucket-name/
aws s3 cp file.txt s3://bucket-name/
aws s3 sync . s3://bucket-name/ --exclude "*" --include "*.md"

REM Lambda operations
aws lambda list-functions
aws lambda invoke --function-name name output.json

REM Step Functions
aws stepfunctions list-state-machines
aws stepfunctions start-execution --state-machine-arn arn --input "{}"
```

### Terraform (CMD)
```cmd
REM Initialize
terraform init

REM Plan
terraform plan -var-file=environments\dev.tfvars

REM Apply
terraform apply -var-file=environments\dev.tfvars

REM Destroy
terraform destroy -var-file=environments\dev.tfvars
```

### Terraform Variable Audit (MANDATORY)

**CRITICAL**: Before running `terraform plan` on new or modified Terraform projects, ALWAYS perform a variable audit to avoid iteration cycles.

**Variable Audit Checklist**:

1. **Audit tfvars → variables.tf**:
   - Compare all variables in `*.tfvars` files with `variables.tf`
   - Ensure every variable used in tfvars is declared in variables.tf
   - Add missing variable declarations with proper types and defaults

2. **Audit module calls → module variables**:
   - For each module call in `main.tf`, check the module's `variables.tf`
   - Ensure all required module variables are passed
   - Ensure no unsupported arguments are passed
   - Check for renamed variables (e.g., `capacity` vs `capacity_min`/`capacity_max`)

3. **Audit module resources → module variables**:
   - Check if module resources reference variables not declared in module's `variables.tf`
   - Common missing variables: `environment`, `common_tags`, `aws_region`
   - Add missing variable declarations to module's `variables.tf`

4. **Audit circular dependencies**:
   - Check for module A needing output from module B, while module B needs output from module A
   - Solution: Use intermediate resources (e.g., VPC creates security groups, both modules use VPC outputs)
   - Separate security group creation from rules using `aws_security_group_rule` resources

5. **Audit variable validations**:
   - Check for validation conditions that fail with null/default values
   - Use `try()` function for validations that might fail: `try(length(var.x) > 0, false)`
   - Ensure default values pass validation rules

**Variable Audit Script** (optional):
```cmd
REM Run variable audit script
python scripts\terraform\fix-variables.py
```

**Common Variable Mismatches**:
- `tags` vs `common_tags` - modules may expect different names
- `min_capacity`/`max_capacity` vs `capacity` - check module expectations
- `environment` - often missing from module variables but used in resources
- `aws_region` - needed for VPC endpoints and regional resources
- `name_prefix` vs `project_name` - naming convention differences

**Before First `terraform plan`**:
- [ ] All tfvars variables declared in variables.tf
- [ ] All module calls pass required variables
- [ ] All module resources have needed variables declared
- [ ] No circular dependencies between modules
- [ ] Variable validations handle null/default values
- [ ] Module interfaces match (argument names, types)

### Common Mistakes to Avoid

❌ **WRONG** (PowerShell):
```powershell
Get-ChildItem
Remove-Item file.txt
$env:PATH
```

✅ **CORRECT** (CMD):
```cmd
dir
del file.txt
echo %PATH%
```

❌ **WRONG** (Bash/PowerShell separator):
```bash
cd src && python script.py
```

✅ **CORRECT** (CMD separator):
```cmd
cd src & python script.py
```

❌ **WRONG** (Forward slashes):
```bash
python scripts/python/script.py
```

✅ **CORRECT** (Backslashes):
```cmd
python scripts\python\script.py
```

## Backup and Recovery (MANDATORY)

**CRITICAL**: Never delete/overwrite files without backing up!

**Procedure**:
1. Create `_bak/` directory if needed
2. Copy to `_bak/{filename}.{YYYYMMDD}_{HHMMSS}.bak`
3. Verify backup exists
4. Then perform operation

**When MANDATORY**:
- Deleting any file
- Overwriting entire file (fsWrite on existing)
- Regenerating with automated tools
- Changes affecting >50% of content

**Recovery**: Check `{repository}/_bak/` for timestamped backups

## Troubleshooting Documentation (MANDATORY)

**When debugging**: Create `.kiro/specs/{spec-name}/troubleshooting-log.md`
**Document**: Search attempts, failed fixes, root causes, next steps
**Purpose**: Preserve knowledge across conversation limits

## Best Practices Summary

### File Operations
- ✅ fsWrite for initial (under 50 lines)
- ✅ fsAppend for incremental additions
- ✅ strReplace for targeted edits (parallel when independent)
- ✅ **MANDATORY backup** to `_bak/` before delete/overwrite
- ❌ Don't write massive files in one operation
- ❌ **NEVER delete/overwrite without backup**

### Development Process
- ✅ Spec-driven (requirements → design → tasks)
- ✅ Explicit user approval each phase (userInput tool)
- ✅ One task at a time, stop for review
- ✅ Update deliverables.md continuously
- ✅ Update ADO discussions with structured format
- ✅ Skip optional tasks (`*`) unless requested
- ❌ Don't skip ahead without approval
- ❌ Don't auto-proceed to next task

### Code Quality
- ✅ Nagara Logger for all Python (no exceptions)
- ✅ Python: Type hints, Black, Ruff, mypy, pydantic, async/await
- ✅ Proper error handling with context
- ✅ Self-documenting code, clear naming
- ✅ 80% test coverage minimum
- ❌ Don't use print in Python (use logger)
- ❌ Don't hardcode credentials
- ❌ Don't skip type hints

### Security
- ✅ AWS Secrets Manager/Vault for secrets
- ✅ TLS encryption, AWS SSO, RBAC
- ✅ CIS benchmarks, audit logging
- ❌ Don't hardcode credentials
- ❌ Don't expose sensitive data in logs

## Quick Reference

### Spec Workflow
- [ ] Create `.kiro/specs/{feature}/`
- [ ] **Create spec-config.yaml** (MANDATORY - defines affected repos, PR delivery points, branch strategy)
- [ ] Write requirements.md (EARS)
- [ ] Get approval (userInput reason='spec-requirements-review')
- [ ] Write design.md
- [ ] Get approval (userInput reason='spec-design-review')
- [ ] Write tasks.md
- [ ] **Add PR delivery tasks to tasks.md** (REMINDER - insert tasks for submitting PRs at logical milestones)
- [ ] **Add branch creation tasks to tasks.md** (REMINDER - insert tasks for creating next branch after PR merge)
- [ ] Get approval (userInput reason='spec-tasks-review')
- [ ] Create deliverables.md
- [ ] Execute tasks one at a time
- [ ] Update deliverables.md after each task
- [ ] Update ADO discussions
- [ ] Stop for review before next

### Task Execution
- [ ] Read requirements.md, design.md, tasks.md
- [ ] Create task-{N}-implementation-report.md (<500 tokens)
- [ ] Review previous task report
- [ ] Check if optional (`*`)
- [ ] Implement changes
- [ ] Update deliverables.md (<800 tokens total)
- [ ] Update task report after subtasks
- [ ] Update ADO discussion
- [ ] Finalize task report
- [ ] Stop for user review

### Token Efficiency (CRITICAL)
- [ ] Task report <500 tokens (HARD LIMIT)
- [ ] Deliverables <800 tokens (HARD LIMIT)
- [ ] Use bullet points only
- [ ] No verbose descriptions
- [ ] Essential info only
- [ ] Archive old reports when >5000 tokens combined

### Python Development
- [ ] Python 3.11+, type hints
- [ ] Import Nagara Logger
- [ ] Initialize logger
- [ ] Use logger methods (no print)
- [ ] Include work_item_id, operation, context
- [ ] Black formatting (100 chars)
- [ ] Ruff linting, mypy type checking
- [ ] Google docstrings
- [ ] Async/await for I/O
- [ ] Custom exceptions
- [ ] pytest 80% coverage
- [ ] requirements.txt updated

### File Backup
- [ ] Create `_bak/` if needed
- [ ] Copy to `_bak/{file}.{YYYYMMDD}_{HHMMSS}.bak`
- [ ] Verify backup exists
- [ ] Proceed with operation
- [ ] Document in deliverables.md

### Security
- [ ] No hardcoded credentials
- [ ] AWS Secrets Manager/Vault
- [ ] TLS encryption
- [ ] AWS Organization SSO
- [ ] RBAC controls
- [ ] Audit logging
- [ ] CIS benchmarks
- [ ] Sanitize logs

## Common Errors & Solutions

| Error | Solution |
|-------|----------|
| "text exceeded 50 line limit" | Use fsWrite + fsAppend or strReplace |
| "'scripts' not recognized" | Prefix with `python`: `python scripts/...` |
| "ADO sync validation failed" | Run validate_ado_hierarchy.py |
| "Nagara Logger import failed" | Check sys.path.append to logger directory |
| "Backup file not found" | Check `{repo}/_bak/` structure, verify timestamp |
| "File deleted without backup" | Check `_bak/`, git history, restore if available |

---

**Purpose**: Consolidated guidance for Kiro AI in Nagara Platform
**Scope**: All repositories in workspace
**Maintained By**: Platform Architecture Team
**Last Updated**: 2025-01-22
**Version**: 2.0.0 (Token-Optimized)
**Token Savings**: ~60% reduction (from ~30K to ~12K tokens)
