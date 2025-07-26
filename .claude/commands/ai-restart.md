Restart git workflow preserving current work: $ARGUMENTS

Use when you've started work on the wrong branch. This safely moves work to a proper feature branch.

1. **Assess current situation**:
   ```bash
   git status
   git branch --show-current
   git log --oneline -5
   ```

2. **Preserve ALL work**:
   ```bash
   # Create descriptive stash
   git stash push -u -m "WIP: moving to proper branch for $ARGUMENTS"

   # Verify stash created
   git stash list
   git stash show -p stash@{0}
   ```

3. **Return to clean base**:
   ```bash
   # Identify proper base branch
   # Check CLAUDE.md for project type

   git checkout main  # or dev
   git pull origin main --ff-only
   ```

4. **Create proper feature branch**:
   ```bash
   # Parse issue from $ARGUMENTS
   # Format: feat/issue-N-description
   git checkout -b feat/issue-$ARGUMENTS
   ```

5. **Restore work on new branch**:
   ```bash
   # Apply stashed work
   git stash pop

   # If conflicts occur:
   # 1. Resolve conflicts
   # 2. git add <resolved-files>
   # 3. Remove .orig files
   ```

6. **Verify work transferred**:
   ```bash
   git status
   git diff
   # Ensure all work is present
   ```

7. **Clean up old branch** (optional):
   ```bash
   # If old branch has no unique commits
   git branch -D old-branch-name
   ```

## Common Scenarios

### Scenario: Started on main
```bash
# Work directly on main (oops!)
git stash -u
git checkout -b feat/issue-123
git stash pop
```

### Scenario: Old feature branch
```bash
# On outdated feat/old-issue
git stash -u
git checkout main && git pull
git checkout -b feat/issue-new
git stash pop
```

### Scenario: Detached HEAD
```bash
# In detached HEAD state
git stash -u
git checkout main
git checkout -b feat/issue-123
git stash pop
```

## Safety Notes
- Never lose work - always stash first
- Include untracked files with -u
- Name stashes descriptively
- Verify work after each step
