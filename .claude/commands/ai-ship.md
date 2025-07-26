Preserve and integrate user changes into proper workflow: $ARGUMENTS

Use when user has made changes outside Claude. This discovers all modifications and creates a clean git workflow on a new feature branch.

1. **Discover all changes**:
   ```bash
   # Full status check
   git status --porcelain

   # Categorize changes:
   # ?? = untracked (new files)
   # M  = modified staged
   #  M = modified unstaged  
   # D  = deleted
   # A  = added
   ```

2. **Analyze change patterns**:
   ```bash
   # Group by type
   git status --porcelain | grep "^??"  # New files
   git status --porcelain | grep "^ M"  # Modified
   git status --porcelain | grep "^D"   # Deleted

   # Check file types and purposes
   find . -name "*.new" -o -name "*.tmp"
   ```

3. **Preserve ALL work**:
   ```bash
   # Note current branch for reference
   ORIGINAL_BRANCH=$(git branch --show-current)

   # Stash everything including untracked files
   git stash push -u -m "WIP: preserving changes for $ARGUMENTS"

   # Verify stash created
   git stash list | head -1
   ```

4. **Determine issue context**:
   ```bash
   # Parse $ARGUMENTS for issue number or description
   # If numeric: use as issue number
   # If text: use as branch description
   # If empty: prompt for issue context
   ```

5. **Update base and create new branch**:
   ```bash
   # Determine base branch (check CLAUDE.md)
   # Libraries: main
   # APIs: dev (if exists) else main

   git checkout main  # or dev
   git pull origin main --ff-only

   # Create new feature branch
   git checkout -b feat/issue-$ARGUMENTS
   ```

6. **Apply preserved work**:
   ```bash
   # Pop the stashed changes
   git stash pop

   # If conflicts occur:
   # 1. Resolve conflicts carefully
   # 2. git add <resolved-files>
   # 3. Remove .orig files
   ```

7. **Handle special files**:
   ```bash
   # Check for sensitive files
   grep -r "SECRET\|PASSWORD\|KEY" --include="*.env*"

   # Large files
   find . -size +10M -type f

   # Temporary files
   find . -name "*.tmp" -o -name "*.bak"
   ```

8. **Create smart commits**:
   ```bash
   # Stage related changes together

   # Example: Group by feature
   git add src/auth/*
   git commit -m "feat: add authentication module"

   git add tests/auth/*
   git commit -m "test: add auth module tests"

   git add docs/*
   git commit -m "docs: update auth documentation"
   ```

9. **Update base and prepare PR**:
   ```bash
   # Fetch latest
   git fetch origin

   # Rebase on base branch
   git rebase origin/main --autostash

   # Push to remote
   git push -u origin HEAD
   ```

## Smart Commit Strategies

### By Component
```bash
# Backend changes
git add api/* lib/*
git commit -m "feat: implement API endpoints"

# Frontend changes  
git add web/* public/*
git commit -m "feat: add UI components"

# Config changes
git add *.config.* *.json *.yaml
git commit -m "chore: update configuration"
```

### By File Type
```bash
# Source code
git add "*.py" "*.js" "*.ts"
git commit -m "feat: core implementation"

# Tests
git add "*test*" "*spec*"
git commit -m "test: add test coverage"

# Documentation
git add "*.md" "docs/*"
git commit -m "docs: update documentation"
```

## Interactive Mode
When changes are complex:
```bash
# Review each change
git add -p  # Patch mode

# Or use interactive
git add -i
```

## Safety Checks
- Never commit secrets (.env files)
- Exclude generated files
- Verify .gitignore is working
- Check file permissions preserved
- Review large file additions

## Final Verification
```bash
# Review all commits
git log --oneline --graph -10

# Check nothing left behind
git status

# Verify builds still work
make test  # or npm test
```
