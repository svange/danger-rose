Create new git branch: $ARGUMENTS

## Quick Branch Creation

```bash
# Create feature branch (hooks handle safety checks)
git checkout -b $ARGUMENTS
```

**Git hooks automatically**:
- ✅ Warn about uncommitted changes
- ✅ Detect workflow type (dev→main vs direct-to-main)
- ✅ Check if branch is behind origin
- ✅ Suggest appropriate next steps

## Branch Naming Convention
- `feat/issue-{number}-{description}` - New features
- `fix/issue-{number}-{description}` - Bug fixes
- `perf/issue-{number}-{description}` - Performance improvements
- `docs/issue-{number}-{description}` - Documentation updates

## If You Need Manual Control

```bash
# 1. Stash changes if needed
git stash push -u -m "WIP: before $ARGUMENTS"

# 2. Create branch
git checkout -b $ARGUMENTS

# 3. Restore stashed work
git stash pop
```
