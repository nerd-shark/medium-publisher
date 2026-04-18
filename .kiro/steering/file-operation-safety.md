---
inclusion: manual
applies_to_tools: ["fsWrite", "deleteFile", "executePwsh", "controlPwshProcess"]
priority: critical
description: "Critical safety procedures for file operations, backups, and destructive actions"
---

# File Operation Safety Procedures

## Critical Rule: NEVER Delete Without Backup

**ABSOLUTE RULE**: Any operation that deletes, moves, or modifies files MUST follow this sequence:

1. **Create Backup** - Copy entire directory/files before any operations
2. **Get Explicit Approval** - Show user the plan and get written approval
3. **Execute with Verification** - Perform operations with step-by-step verification
4. **Verify Success** - Confirm all files are in correct locations
5. **Only Then Delete** - Delete old files/directories ONLY after verification

---

## File Operation Categories

### Category 1: Safe Operations (No Backup Required)
- Creating new files
- Reading files
- Appending to files
- Creating new directories

**Approval Required**: No (unless modifying user's code)

### Category 2: Moderate Risk (Backup Recommended)
- Modifying existing files (strReplace)
- Renaming files
- Moving files within same directory

**Approval Required**: Yes (show changes, get approval)  
**Backup Required**: Recommended for important files

### Category 3: High Risk (Backup MANDATORY)
- Deleting files or directories
- Moving files between directories
- Bulk file operations
- Reorganizing directory structures
- Running scripts that modify multiple files

**Approval Required**: YES - Explicit written approval  
**Backup Required**: MANDATORY - Create backup before any operations  
**Verification Required**: YES - Verify each step

### Category 4: Critical Risk (Extra Caution)
- Deleting multiple directories
- Bulk deletion operations
- Reorganizing entire project structures
- Running automated scripts with deletion phases

**Approval Required**: YES - Explicit written approval with full plan review  
**Backup Required**: MANDATORY - Full backup with verification  
**Verification Required**: YES - Verify at each phase before proceeding  
**Dry-Run Required**: YES - Show what will happen before executing  
**Rollback Plan**: YES - Document how to recover if something goes wrong

---

## Backup Procedures

### Before Any Destructive Operation

**Step 1: Create Backup**
```bash
# For directories
cp -r /path/to/directory /path/to/directory.backup.YYYYMMDD

# For files
cp /path/to/file /path/to/file.backup.YYYYMMDD
```

**Step 2: Verify Backup**
- Confirm backup directory/file exists
- Verify backup contains all expected files
- Check file sizes match originals
- Spot-check file contents

**Step 3: Document Backup Location**
- Note backup path in operation log
- Include timestamp
- Include reason for backup

### Backup Retention

**Retention Period**: Minimum 7 days after operation  
**Storage**: Same location as original (or documented alternate location)  
**Verification**: Periodically verify backup integrity

---

## Approval Process

### For Moderate Risk Operations

**Required Information**:
1. What files/directories will be modified
2. What changes will be made
3. Why the changes are necessary
4. Impact assessment

**Approval Format**:
```
User: "Go ahead with [operation description]"
OR
User: "Approved - [operation description]"
```

### For High Risk Operations

**Required Information**:
1. Complete list of files/directories affected
2. Detailed operation plan (step-by-step)
3. Backup location and verification plan
4. Verification steps after operation
5. Rollback procedure if needed
6. Impact assessment

**Approval Format**:
```
User: "Approved - proceed with [operation name]"
OR
User: "Yes, execute [operation name]"
```

**Explicit Approval Required**: User must explicitly approve, not just acknowledge

### For Critical Risk Operations

**Required Information**:
1. Full operation plan with all steps
2. Dry-run output showing what will happen
3. Backup strategy and verification
4. Phase-by-phase verification plan
5. Complete rollback procedure
6. Risk assessment and mitigation
7. Recovery procedures if something fails

**Approval Format**:
```
User: "Approved - execute [operation name]"
OR
User: "Yes, proceed with [operation name]"
```

**Explicit Approval Required**: User must explicitly approve the complete plan

---

## Execution Procedures

### Phase 1: Pre-Execution Verification

- [ ] Backup created and verified
- [ ] User approval obtained and documented
- [ ] All source files exist and are accessible
- [ ] Destination directories exist or will be created
- [ ] Sufficient disk space available
- [ ] No conflicting operations in progress

### Phase 2: Execution with Verification

**For Each Operation**:
1. Execute operation
2. Verify success (file exists, content correct, etc.)
3. Report result to user
4. Check for errors or warnings
5. Do NOT proceed to next step if verification fails

**Stop Immediately If**:
- Any file is missing or corrupted
- Operation produces errors
- Verification fails
- Unexpected results occur

### Phase 3: Post-Execution Verification

- [ ] All files in correct locations
- [ ] File contents verified (spot-check)
- [ ] No files lost or corrupted
- [ ] Directory structure correct
- [ ] Links and references updated
- [ ] Backup still available

### Phase 4: Cleanup

- [ ] Only delete old files/directories AFTER verification
- [ ] Verify deletion was successful
- [ ] Document what was deleted and when
- [ ] Keep backup for minimum 7 days

---

## Dry-Run Procedures

### For Complex Operations

**Before Executing**:
1. Show user exactly what will happen
2. List all files that will be moved/deleted
3. Show directory structure changes
4. Identify any potential issues
5. Get approval before proceeding

**Dry-Run Output Should Include**:
- Files to be moved (source → destination)
- Files to be deleted
- Directories to be created
- Directories to be deleted
- Any potential conflicts or issues

---

## Error Recovery

### If Operation Fails

**Immediate Actions**:
1. Stop all operations
2. Report error to user
3. Do NOT attempt to continue
4. Do NOT delete anything
5. Preserve backup

**Recovery Steps**:
1. Restore from backup if needed
2. Investigate root cause
3. Plan corrected approach
4. Get new approval
5. Execute corrected operation

### If Files Are Lost

**Immediate Actions**:
1. Stop all operations
2. Restore from backup immediately
3. Verify restoration successful
4. Report incident to user
5. Document what happened

---

## Documentation Requirements

### Operation Log Entry

For every high-risk or critical-risk operation:

```
Operation: [Name]
Date: [YYYY-MM-DD HH:MM:SS]
User Approval: [Yes/No] - [Approval text]
Backup Location: [Path]
Backup Verified: [Yes/No]
Files Affected: [Count and list]
Status: [In Progress/Completed/Failed]
Verification: [Results]
Notes: [Any issues or observations]
```

---

## Specific Scenarios

### Scenario: Directory Reorganization

**Risk Level**: Critical

**Procedure**:
1. Create full backup of directory
2. Verify backup completely
3. Show user reorganization plan with dry-run
4. Get explicit approval
5. Create new directory structure
6. Move files one category at a time
7. Verify each move
8. Update internal links/references
9. Verify all files in new locations
10. Only then delete old directories
11. Final verification
12. Keep backup for 7 days

### Scenario: Bulk File Deletion

**Risk Level**: Critical

**Procedure**:
1. Create backup of all files to be deleted
2. Verify backup
3. List all files to be deleted
4. Get explicit approval
5. Delete files one at a time
6. Verify each deletion
7. Confirm all deletions successful
8. Keep backup for 7 days

### Scenario: Script Execution with Deletion Phase

**Risk Level**: Critical

**Procedure**:
1. Create backup of all affected directories
2. Verify backup
3. Show user script code
4. Show dry-run output
5. Get explicit approval
6. Execute script with deletion phase disabled first
7. Verify results
8. Get approval to enable deletion phase
9. Execute deletion phase
10. Verify deletions
11. Keep backup for 7 days

---

## Checklist for Destructive Operations

**Before Starting**:
- [ ] Backup created
- [ ] Backup verified
- [ ] User approval obtained
- [ ] Operation plan documented
- [ ] Verification steps planned
- [ ] Rollback procedure documented

**During Operation**:
- [ ] Each step verified before proceeding
- [ ] Errors reported immediately
- [ ] No assumptions made
- [ ] User kept informed

**After Operation**:
- [ ] All files verified in correct locations
- [ ] No files lost or corrupted
- [ ] Links/references updated
- [ ] Backup retained for 7 days
- [ ] Operation documented

---

## When in Doubt

**If uncertain about safety**:
1. Create a backup
2. Ask the user for approval
3. Show the plan before executing
4. Verify each step
5. Never assume it's safe

**Better to be overly cautious than to lose data.**

---

**Document Owner**: Platform Engineering Team  
**Priority**: CRITICAL  
**Review Frequency**: Quarterly  
**Last Updated**: 2025-01-21  
**Version**: 1.0

**CRITICAL REMINDER**: This document exists because of a near-data-loss incident. Follow these procedures religiously.
