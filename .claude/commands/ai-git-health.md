Check repository health and identify git hygiene issues: $ARGUMENTS

Use to audit repository state and find issues that need attention. Provides comprehensive health check with actionable recommendations.

1. **Check for uncommitted changes**:
   ```bash
   # Check working directory status
   git status --porcelain

   # If changes exist, categorize them:
   git status --porcelain | grep "^??" | wc -l  # Untracked files
   git status --porcelain | grep "^ M" | wc -l  # Modified files
   git status --porcelain | grep "^M " | wc -l  # Staged files
   ```

2. **Find unpushed commits**:
   ```bash
   # Check all branches for unpushed commits
   git for-each-ref --format="%(refname:short) %(upstream:track)" refs/heads | grep "\["

   # Show unpushed commits on current branch
   git log @{u}..HEAD --oneline

   # Count unpushed commits per branch
   for branch in $(git branch -r | grep -v HEAD); do
     git log origin/$(basename $branch)..$(basename $branch) --oneline 2>/dev/null | wc -l
   done
   ```

3. **Identify unmerged feature branches**:
   ```bash
   # List all local branches
   git branch --no-merged main

   # Check if branches have open PRs
   for branch in $(git branch --no-merged main | grep -v "^\*"); do
     echo "Branch: $branch"
     gh pr list --head $branch --state all
   done

   # Find abandoned branches (no commits in 30+ days)
   git for-each-ref --format='%(refname:short) %(committerdate:relative)' refs/heads | \
     grep -E "(months|years) ago"
   ```

4. **Check branch divergence**:
   ```bash
   # Compare with main/dev
   git fetch origin

   # For each branch, check divergence
   for branch in $(git branch | grep -v "^\*"); do
     echo "=== Branch: $branch ==="
     git rev-list --left-right --count origin/main...$branch
   done

   # Check if current branch needs rebasing
   git merge-base --is-ancestor origin/main HEAD || echo "Branch needs rebase!"
   ```

5. **Scan for large files**:
   ```bash
   # Find files over 10MB
   find . -type f -size +10M -not -path "./.git/*" | while read file; do
     echo "Large file: $file ($(du -h "$file" | cut -f1))"
   done

   # Check git history for large blobs
   git rev-list --objects --all | \
     git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
     awk '/^blob/ {if ($3 > 10485760) print $4 " " $3/1048576 " MB"}' | \
     sort -k2 -n -r | head -10
   ```

6. **Security and secrets scan**:
   ```bash
   # Check for potential secrets
   grep -r -E "(password|secret|key|token|api_key)" --include="*.env*" .
   grep -r -E "ghp_|ghs_|github_pat_" .
   grep -r -E "AKIA[0-9A-Z]{16}" .  # AWS keys

   # Check .gitignore effectiveness
   git ls-files -i --exclude-standard
   ```

7. **Check merge conflicts**:
   ```bash
   # Find conflict markers
   grep -r "<<<<<<< HEAD" . --exclude-dir=.git
   grep -r "=======" . --exclude-dir=.git  
   grep -r ">>>>>>> " . --exclude-dir=.git

   # Check for .orig files from merges
   find . -name "*.orig" -type f
   ```

8. **Repository statistics**:
   ```bash
   # Branch count
   echo "Total branches: $(git branch -a | wc -l)"
   echo "Local branches: $(git branch | wc -l)"
   echo "Remote branches: $(git branch -r | wc -l)"

   # Stash count
   echo "Stashes: $(git stash list | wc -l)"

   # Tag count
   echo "Tags: $(git tag | wc -l)"
   ```

9. **Check CI/CD status**:
   ```bash
   # Recent workflow runs
   gh run list --limit 5

   # Failed workflows
   gh run list --status failure --limit 5

   # PR checks
   gh pr checks
   ```

10. **Generate health report**:
    ```bash
    echo "=== Git Repository Health Report ==="
    echo "Repository: $(basename $(git rev-parse --show-toplevel))"
    echo "Current branch: $(git branch --show-current)"
    echo "Last commit: $(git log -1 --format='%h %s (%cr)')"
    echo ""
    echo "=== Issues Found ==="
    # Summarize all findings
    ```

## Action Items

### Critical (Fix immediately)
- Uncommitted changes containing secrets
- Unmerged branches with no PRs
- Large files in repository
- Merge conflicts present

### High Priority
- Unpushed commits on main/dev
- Branches diverged significantly from main
- Stale branches (>30 days old)
- Failed CI/CD runs

### Medium Priority  
- Multiple stashes pending
- Untracked files in working directory
- Branches without upstream tracking

### Low Priority
- Old tags to clean up
- Documentation updates needed
- Branch naming inconsistencies

## Remediation Commands

### Clean up stale branches
```bash
# Delete merged branches
git branch --merged main | grep -v "main\|dev" | xargs -r git branch -d

# Delete remote tracking branches
git remote prune origin
```

### Fix unpushed commits
```bash
# Push all branches with upstream
git push --all

# Set upstream for branches without
git branch --no-contains origin/main | xargs -I {} git push -u origin {}
```

### Handle large files
```bash
# Add to .gitignore
echo "path/to/large/file" >> .gitignore

# Remove from history (careful!)
git filter-branch --index-filter 'git rm --cached --ignore-unmatch path/to/large/file' HEAD
```

## Preventive Measures
1. Set up pre-commit hooks for large files
2. Enable branch protection rules
3. Configure auto-delete merged branches
4. Set up secret scanning alerts
5. Regular hygiene checks (weekly)

## Summary Output Format
```
Repository Health: [Good|Warning|Critical]
- Uncommitted changes: [count]
- Unpushed commits: [count]
- Unmerged branches: [count]
- Branches without PRs: [count]
- Large files: [count]
- Stale branches: [count]
- Security issues: [count]

Top 3 Actions Required:
1. [Most critical issue]
2. [Second priority]
3. [Third priority]
```
