# Context7 MCP Code Assistance

## Core Rule
**Use Context7 MCP for Library Documentation**: When writing code that uses external libraries or frameworks, use the Context7 MCP to fetch up-to-date documentation and code examples.

## Quick Reference

| Scenario | Action | Example |
|----------|--------|---------|
| Using new library | Resolve library ID, fetch docs | `resolve-library-id` → `get-library-docs` |
| Need code examples | Fetch docs with topic | `get-library-docs` with topic parameter |
| Multiple libraries | Resolve each separately | One `resolve-library-id` per library |
| Pagination needed | Use page parameter | `page=2`, `page=3` for more context |

## Implementation

### Step 1: Resolve Library ID
Before fetching documentation, resolve the library name to a Context7-compatible ID:

```python
# Use resolve-library-id tool
libraryName: "boto3"  # or "fastapi", "pytest", etc.
```

**Returns**: Context7-compatible library ID (e.g., `/boto/boto3`, `/tiangolo/fastapi`)

### Step 2: Fetch Documentation
Use the resolved library ID to get documentation:

```python
# Use get-library-docs tool
context7CompatibleLibraryID: "/boto/boto3"
topic: "s3 operations"  # Optional: focus on specific topic
page: 1  # Start with page 1, use 2, 3, 4 if more context needed
```

### Step 3: Apply Documentation
Use the fetched documentation to:
- Understand API patterns
- Find correct method signatures
- See working code examples
- Follow best practices

## When to Use Context7

### ✅ Use Context7 When:
- Starting work with a new library
- Unsure about API signatures or parameters
- Need code examples for specific functionality
- Want to follow library best practices
- Implementing complex library features

### ❌ Don't Use Context7 When:
- Working with internal/proprietary code
- Library not available in Context7
- Simple standard library usage (os, sys, json)
- Documentation already in context

## Common Libraries

### Python
- **boto3**: AWS SDK - `/boto/boto3`
- **fastapi**: Web framework - `/tiangolo/fastapi`
- **pytest**: Testing - `/pytest-dev/pytest`
- **pydantic**: Data validation - `/pydantic/pydantic`
- **sqlalchemy**: ORM - `/sqlalchemy/sqlalchemy`

### JavaScript/TypeScript
- **react**: UI library - `/facebook/react`
- **next.js**: React framework - `/vercel/next.js`
- **express**: Web framework - `/expressjs/express`
- **typescript**: Type system - `/microsoft/TypeScript`

### Workflow Example

```markdown
**Task**: Implement S3 file upload with boto3

**Step 1**: Resolve boto3 library
- Tool: resolve-library-id
- Input: "boto3"
- Output: "/boto/boto3"

**Step 2**: Get S3 documentation
- Tool: get-library-docs
- Input: context7CompatibleLibraryID="/boto/boto3", topic="s3 upload"
- Output: Documentation with upload examples

**Step 3**: Implement using examples
- Use put_object() method from docs
- Follow error handling patterns
- Apply best practices from examples
```

## Best Practices

1. **Resolve First**: Always resolve library ID before fetching docs
2. **Use Topics**: Narrow documentation with topic parameter
3. **Paginate**: If context insufficient, try page=2, page=3
4. **Multiple Libraries**: Resolve each library separately
5. **Cache Results**: Keep documentation in context for related tasks

## Error Handling

### Library Not Found
If `resolve-library-id` returns no matches:
- Check library name spelling
- Try alternative names (e.g., "aws-sdk" vs "boto3")
- Library may not be in Context7 catalog

### Insufficient Context
If documentation doesn't cover your use case:
- Try different topic keywords
- Use pagination (page=2, page=3)
- Combine with existing knowledge

## Integration with Development Workflow

### Before Writing Code
1. Identify external libraries needed
2. Resolve library IDs using Context7
3. Fetch relevant documentation
4. Review API patterns and examples

### During Implementation
1. Reference fetched documentation
2. Follow code examples from Context7
3. Apply best practices from docs
4. Use correct method signatures

### After Implementation
1. Verify code matches documentation patterns
2. Check for deprecated methods
3. Ensure error handling follows best practices

---

**Status**: Active | **Updated**: 2025-01-19 | **Owner**: Platform Team
**MCP**: context7 | **Tools**: resolve-library-id, get-library-docs
