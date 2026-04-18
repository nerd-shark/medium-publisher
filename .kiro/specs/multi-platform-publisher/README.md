# Multi-Platform Article Publisher Spec

## Overview

This spec extends the Medium Article Publisher to support multiple publishing platforms (Medium and Substack) through a unified interface using the Strategy Pattern.

## Status

**Phase**: Planning  
**Created**: 2025-02-28  
**Estimated Effort**: 18 days (3.5-4 weeks)

## Goals

1. **Multi-Platform Support**: Enable publishing to both Medium and Substack
2. **Platform Abstraction**: Create extensible architecture for future platforms
3. **Zero Regression**: Maintain all existing Medium functionality
4. **Consistent UX**: Unified interface across platforms
5. **Easy Extension**: Simple process to add new platforms

## Architecture Approach

### Strategy Pattern Implementation

```
PlatformInterface (Abstract)
    ↓
    ├── MediumPlatform (Concrete)
    └── SubstackPlatform (Concrete)
```

### Key Components

1. **PlatformInterface**: Abstract base class defining platform contract
2. **PlatformFactory**: Factory for creating platform instances
3. **MediumPlatform**: Refactored Medium implementation
4. **SubstackPlatform**: New Substack implementation
5. **Multi-Platform UI**: Platform selector and platform-specific settings

## Implementation Phases

### Phase 1: Platform Abstraction Layer (2 days)
- Create platform directory structure
- Implement PlatformInterface abstract class
- Implement PlatformFactory
- Update configuration structure

### Phase 2: Medium Refactor (3 days)
- Refactor MediumEditor → MediumPlatform
- Refactor AuthHandler → MediumAuth
- Refactor ContentTyper → MediumTyper
- Update imports throughout codebase
- Regression testing

### Phase 3: Substack Implementation (5 days)
- Research Substack editor structure
- Implement SubstackAuth
- Implement SubstackTyper
- Implement SubstackPlatform
- Register in PlatformFactory

### Phase 4: UI Updates (2 days)
- Add platform selector to main window
- Update draft URL validation per platform
- Add platform-specific UI elements
- Create platform settings dialog

### Phase 5: Workflow Updates (2 days)
- Update PublishingWorkflow for multi-platform
- Update SessionManager for multi-platform
- Update error handling for multi-platform

### Phase 6: Testing (3 days)
- Unit tests for platform abstraction
- Unit tests for Medium platform (regression)
- Unit tests for Substack platform
- Integration tests for multi-platform
- UI tests for platform selector

### Phase 7: Documentation (1 day)
- Update user documentation
- Update developer documentation
- Create platform addition guide

## Key Features

### User Features
- Platform selector dropdown (Medium/Substack)
- Platform-specific authentication
- Platform-specific publishing options
- Platform-specific draft URL validation
- Seamless platform switching
- Independent platform sessions

### Developer Features
- Clean platform abstraction
- Easy platform addition (implement interface + register)
- Platform-specific configuration
- Platform-specific error handling
- Extensible architecture

## Files Structure

```
medium_publisher/
├── platforms/
│   ├── platform_interface.py      # Abstract base class
│   ├── platform_factory.py        # Factory
│   ├── medium/
│   │   ├── medium_platform.py     # Medium implementation
│   │   ├── medium_auth.py         # Medium auth
│   │   ├── medium_typer.py        # Medium typing
│   │   └── medium_selectors.yaml  # Medium selectors
│   └── substack/
│       ├── substack_platform.py   # Substack implementation
│       ├── substack_auth.py       # Substack auth
│       ├── substack_typer.py      # Substack typing
│       └── substack_selectors.yaml # Substack selectors
├── ui/
│   ├── main_window.py             # Updated: platform selector
│   ├── platform_settings.py       # New: platform settings
│   └── ...
├── core/
│   ├── publishing_workflow.py     # Updated: use PlatformInterface
│   ├── session_manager.py         # Updated: multi-platform
│   └── ...
└── ...
```

## Configuration Structure

```yaml
# Global settings
typing: {...}
browser: {...}
paths: {...}

# Platform selection
platform:
  selected: "medium"

# Platform-specific configs
platforms:
  medium:
    publishing: {...}
    credentials: {...}
    paths: {...}
  
  substack:
    publishing: {...}
    credentials: {...}
    paths: {...}
```

## Platform Differences

| Feature | Medium | Substack |
|---------|--------|----------|
| **Editor** | Rich text WYSIWYG | Markdown-native |
| **Auth** | Email/Password + OAuth | Email/Password only |
| **Metadata** | Tags (max 5), subtitle | Categories |
| **Publish Modes** | Draft, Public | Draft, Send |
| **URL Format** | medium.com/@user/story | name.substack.com/p/post |

## Success Criteria

- [ ] User can select between Medium and Substack
- [ ] User can authenticate with both platforms
- [ ] User can publish to Medium (no regression)
- [ ] User can publish to Substack
- [ ] User can switch platforms without restart
- [ ] Platform-specific features work correctly
- [ ] Draft URLs validated per platform
- [ ] All tests pass
- [ ] Documentation complete

## Migration Strategy

### Backward Compatibility
- Existing Medium configs migrated automatically
- Old session cookies moved to platform-specific locations
- Default platform set to "Medium"
- No user action required

### Breaking Changes
- Import paths changed (documented in migration guide)
- Configuration structure changed (auto-migrated)
- Session file locations changed (auto-migrated)

## Future Platforms

The architecture supports easy addition of:
- Dev.to
- Hashnode
- Ghost
- WordPress
- Any platform with web editor or API

## Getting Started

1. Review requirements.md for detailed user stories
2. Review design.md for architecture details
3. Review tasks.md for implementation breakdown
4. Start with Phase 1 (Platform Abstraction Layer)

## Questions?

- **Why refactor instead of separate apps?** Unified UX, shared code, easier maintenance
- **Why browser automation for Substack?** Consistent approach, no API key management
- **Can we add more platforms?** Yes! Implement PlatformInterface and register in factory
- **Will Medium functionality break?** No, comprehensive regression testing ensures zero regression
- **How long to add a new platform?** ~3-5 days (research + implementation + testing)

## Related Documents

- [Requirements](requirements.md) - Detailed user stories and acceptance criteria
- [Design](design.md) - Architecture and component design
- [Tasks](tasks.md) - Implementation task breakdown
- [Deliverables](deliverables.md) - Tracking document for outputs

## Contact

For questions or clarifications about this spec, please refer to the detailed documents above.
