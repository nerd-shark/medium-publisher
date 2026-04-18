---
inclusion: manual
---

# Steering Document Context Provider

## Proactive Document Suggestions

This context provider enables Kiro to automatically suggest relevant steering documents based on the current task context.

## How It Works

### Automatic Context Detection
Kiro analyzes:
- **Current files** being worked on (file extensions, names, directories)
- **Task description** from user input or conversation context
- **Repository context** (which repo you're working in)
- **Technology patterns** (Rust, React, Kubernetes, etc.)
- **Inferred role** (backend, frontend, PMO, architect)

### Suggestion Algorithm
The system scores documents based on:
1. **Role relevance** (30 points) - Documents for your inferred role
2. **Repository match** (20 points) - Documents from your current repository
3. **Technology overlap** (15 points per match) - Matching technology tags
4. **Task type alignment** (25 points) - Documents for your task type
5. **Keyword matching** (10 points per match) - Keywords in document content

### Integration Commands

#### Quick Check
```python
# Check if there are relevant unloaded documents
python scripts/steering/kiro-integration.py --quick --task "implementing promise controller" --files "promise-controller.rs" --repo "backend"
```

#### Full Analysis
```python
# Get detailed suggestions with reasons
python scripts/steering/kiro-integration.py --message --task "building react components" --files "Button.tsx" --repo "frontend"
```

#### Auto-Load Commands
```python
# Get load commands for automatic loading
python scripts/steering/kiro-integration.py --commands --task "api development" --repo "backend"
```

## Steering System Index

The complete steering system structure is defined in `steering-system-index.json` which provides:
- Document locations and categories
- Loading strategies for different document types  
- Precedence rules for conflict resolution
- Human vs AI tool separation

## Usage Patterns for Kiro

### 1. Proactive Suggestions
When a user starts working on a task, Kiro can automatically check:

```python
from scripts.steering.kiro_integration import KiroSteeringIntegration

integration = KiroSteeringIntegration()

# Check for suggestions based on context
suggestions = integration.check_for_suggestions(
    task_description="implementing kubernetes controllers",
    current_files=["promise-controller.rs", "work-controller.rs"],
    repository="backend"
)

if suggestions["has_suggestions"]:
    message = integration.get_contextual_message(suggestions)
    # Display message to user
    print(message)
    
    # Optionally auto-load top suggestions
    load_commands = integration.auto_load_suggestions(suggestions)
    for command in load_commands:
        # Execute load command (e.g., load document with #promise-work-patterns)
        pass
```

### 2. Context-Aware Responses
When responding to user questions, Kiro can check for additional relevant guidance:

```python
# Quick check during conversation
quick_message = integration.quick_check(
    task_description="user is asking about rust error handling",
    current_files=["error.rs"],
    repository="backend"
)

if quick_message:
    # Append to response: "💡 I found 2 relevant steering documents that could help: #rust-development, #backend-code-quality"
    pass
```

### 3. File-Based Triggers
When files are opened or modified, Kiro can suggest relevant documents:

```python
# Triggered when user opens files
def on_file_open(file_paths):
    suggestions = integration.check_for_suggestions(
        current_files=file_paths,
        repository=detect_repository(file_paths[0])
    )
    
    if suggestions["has_suggestions"]:
        # Show subtle notification with suggestions
        pass
```

## Example Scenarios

### Backend Development
**Context**: Working on `promise-controller.rs` in `Nagara_Backend`
**Suggestions**:
- `#promise-work-patterns` - Core platform patterns
- `#kubernetes-controller-patterns` - Controller development patterns  
- `#rust-development-standards` - Rust coding standards

### Frontend Development  
**Context**: Working on `Button.tsx` in `Nagara_Frontend`
**Suggestions**:
- `#react-development-standards` - React patterns
- `#ui-component-design-system` - Component guidelines
- `#frontend-security-standards` - Security implementation

### API Development
**Context**: Task description mentions "REST API" 
**Suggestions**:
- `#api-contract-standards` - API design standards
- `#backend-api-development` - Implementation patterns
- `#application-security-standards` - Security requirements

### Cross-Repository Work
**Context**: Task mentions "integration" or "cross-repo"
**Suggestions**:
- `#cross-repository-coordination` - Multi-repo workflows
- `#api-integration-patterns` - Integration patterns
- `#deployment-orchestration` - Deployment coordination

## Configuration

### Suggestion Limits
- **Default**: 3 suggestions per check (to avoid overwhelming)
- **Maximum**: 5 suggestions for detailed analysis
- **Minimum relevance**: 25 points (filters out low-relevance matches)

### Auto-Loading Behavior
- **Conservative**: Only suggest loading, don't auto-load
- **Proactive**: Auto-load top 1-2 suggestions for high-confidence matches
- **User preference**: Allow users to configure auto-loading behavior

### Context Detection
- **File patterns**: Analyze file extensions, names, and directory structure
- **Technology keywords**: 50+ recognized technology terms
- **Task classification**: 7 task types (development, testing, deployment, etc.)
- **Role inference**: Based on repository and file patterns

## Integration Points

### Kiro Chat Interface
```markdown
User: "I'm implementing a new Promise controller"

Kiro: "I'll help you implement the Promise controller. 

🦀 **Backend Development Context Detected**
I found 3 relevant steering documents that could help with this development task:

**1. Promise/Work Pattern Architectural Decisions**
   💡 Covers technologies: promise, work, kubernetes
   🔗 Load with: `#promise-work-patterns`

**2. Kubernetes Controller Design Patterns**  
   💡 Relevant for backend developers
   🔗 Load with: `#kubernetes-controller-patterns`

**3. Rust Development Standards**
   💡 Matches keywords: rust, controller
   🔗 Load with: `#rust-development-standards`

💡 **Tip**: I can load these documents automatically if you'd like. Just let me know!"
```

### Kiro File Explorer
When files are selected or opened, show subtle suggestions in the sidebar or status bar.

### Kiro Command Palette
Add commands for manual steering document discovery:
- "Find Relevant Steering Documents"
- "Load Suggested Documents"
- "Show Steering Context"

## Benefits

### For Users
- **Proactive guidance** - Get relevant help before asking
- **Context awareness** - Suggestions match current work
- **Reduced friction** - Easy loading with simple commands
- **Discovery** - Find documents you didn't know existed

### For Kiro
- **Better responses** - More context leads to better answers
- **User satisfaction** - Proactive help improves experience
- **Knowledge utilization** - Ensures steering documents are actually used
- **Adaptive behavior** - System learns what's relevant when

## Implementation Status

✅ **Completed**:
- Proactive suggestion algorithm
- Context analysis and scoring
- CLI integration tools
- Example usage patterns

🔄 **In Progress**:
- Kiro integration hooks
- Auto-loading behavior
- User preference configuration

📋 **Planned**:
- Machine learning for improved suggestions
- User feedback integration
- Performance optimization
- Advanced context detection

---

**Usage**: This context provider enables Kiro to automatically suggest relevant steering documents based on current task context, improving developer productivity and ensuring relevant guidance is always available.