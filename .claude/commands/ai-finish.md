Complete work and create pull request: $ARGUMENTS

Follow these steps to safely finish and submit work:

1. **Run quality checks**:
   ```bash
   # Python projects
   make test
   make lint
   make security

   # Node projects
   npm test
   npm run lint
   npm audit --audit-level=high
   ```

2. **Review changes**:
   ```bash
   git status
   git diff --staged
   git diff
   ```

3. **Stage and commit**:
   ```bash
   git add -A
   # Or selective: git add -p

   # Conventional commit format
   git commit -m "type: description

   - Detail 1
   - Detail 2

   closes #issue-number"
   ```

4. **Sync with base branch**:
   ```bash
   # Fetch latest
   git fetch origin

   # Rebase on base branch
   git rebase origin/main  # or origin/dev

   # If conflicts:
   # 1. Fix conflicts
   # 2. git add <files>
   # 3. git rebase --continue
   ```

5. **Final quality check**:
   ```bash
   # Re-run tests after rebase
   make test
   ```

6. **Push branch**:
   ```bash
   # First push
   git push -u origin HEAD

   # After rebase (if needed)
   git push --force-with-lease
   ```

7. **Create pull request**:
   Use `mcp__github__create_pull_request`:
   - Title: Match commit message
   - Body: Include "closes #N"
   - Add test results
   - List key changes

## PR Description Template
```
## Summary
Brief description of changes

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated

closes #issue-number
```

## Edge Cases
- **Rebase conflicts**: Take time to resolve correctly
- **Test failures**: Fix before pushing
- **Large diffs**: Consider splitting PR
