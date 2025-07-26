# Test Claude Mods - Comprehensive Testing Suite

Run a complete test suite for all custom Claude Code modifications, including hooks, git workflow automations, permission rules, and environment configurations.

## Overview

This command serves as a comprehensive testing suite to verify that all custom Claude Code modifications are working correctly. It tests:
- Permission rules (new file protection)
- Git workflow hooks (merge conflict prevention)
- Poetry integration hooks
- Branch protection mechanisms
- Environment configurations
- Custom command behaviors
- Extended timeout settings

## Test Suite Components

### 1. Test permission rules (NEW)
These operations should be BLOCKED by permission rules:

#### Lock file protection
```bash
# Try to edit poetry.lock
echo "Testing poetry.lock protection..."
```
Expected: Edit/Write operations on poetry.lock should be denied

```bash
# Try to edit package-lock.json
echo "Testing package-lock.json protection..."
```
Expected: Edit/Write operations on package-lock.json should be denied

#### Dependency management enforcement
```bash
# Try to edit pyproject.toml dependencies section
echo "Testing pyproject.toml dependency protection..."
```
Expected: Edits to [tool.poetry.dependencies] section should be denied

```bash
# Try direct pip install
pip install requests
```
Expected: Should be denied (except pip install -e)

```bash
# Try to push to main
git push origin main
```
Expected: Should be denied

### 2. Test hook configuration
Check if hooks and permissions are configured:
```bash
echo "=== Configuration Status ==="
echo "Hooks configured: $(grep -c '"command"' ~/.claude/settings.json 2>/dev/null || echo 0)"
echo "Permission rules: $(grep -c '"action"' ~/.claude/settings.json 2>/dev/null || echo 0)"
echo "Timeout setting: $(grep 'BASH_MAX_TIMEOUT_MS' ~/.claude/settings.json 2>/dev/null || echo 'Not set')"
```

### 3. Test blocked commands
These commands should be BLOCKED by the hook:

#### Poetry run commands (unnecessary in Claude Code)
```bash
poetry run pytest
```
Expected: Hook blocks with message "poetry run is not necessary in Claude Code - commands run directly in the virtual environment. Try the command without the poetry run prefix."

```bash
poetry run python -m pytest
```
Expected: Same blocking message

```bash
poetry run python --version
```
Expected: Same blocking message

#### Other blocked commands
```bash
pip install requests
```
Expected: "BLOCKED: Use poetry add instead of pip install"

```bash
rm -rf /
```
Expected: "DANGEROUS: Refusing to delete root directory!"

### 3. Test allowed commands (without poetry run)
These commands should work directly:

```bash
pytest
```
Expected: Runs pytest normally (shows version or runs tests)

```bash
python --version
```
Expected: Shows Python version

```bash
python -m pytest --version
```
Expected: Shows pytest version

```bash
make test
```
Expected: Runs the make command normally

### 4. Test Git hooks
#### Warning hooks (non-blocking):
```bash
# First create a test file
echo "test" > test.txt
git add test.txt

# Then try to checkout
git checkout -b test-branch
```
Expected: Warning about uncommitted changes but command proceeds

#### Blocking hooks:
```bash
# If on main branch
git push --force origin main
```
Expected: "🚨 BLOCKED: Cannot force push to main branch!"

### 5. Test Git Workflow Automation Hooks

#### Branch Sync Detection:
```bash
# Create a feature branch
git checkout -b feat/test-sync
```
Expected: Shows repo workflow type (dev→main or direct-to-main)

#### Poetry Lock Sync:
```bash
# Test poetry command hook
poetry add --group dev pytest-mock
```
Expected: "🔒 Updating poetry.lock..." followed by reminder to commit both files

#### Branch Behind Detection:
```bash
# Simulate outdated branch (if possible)
git checkout main && git pull && git checkout -b feat/behind-test
# Make a commit on main, then switch back
```
Expected: Warning about branch being behind with rebase commands

#### Mixed Commit Detection:
```bash
# Stage multiple file types
touch test.py README.md
git add test.py README.md
git commit -m "test: mixed commit"
```
Expected: Warning about mixed commit with suggestions to split

### 6. Test Merge Conflict Prevention

#### Push Protection:
```bash
# Try to push an outdated branch (simulation)
git push origin feat/test-branch
```
Expected: If branch is behind, BLOCKS with "🚫 BLOCKED: Branch is X commits behind"

#### Dev Branch Accumulation:
```bash
# If in a repo with dev branch
git checkout dev && git push
```
Expected: If dev is >10 commits ahead of main, warns about accumulation

### 7. Test post-command hooks
```bash
git status
```
Expected: Shows status, and if behind origin, suggests `git pull --rebase`

```bash
make test
```
Expected: If tests pass, shows "✅ All tests passing!" and suggests next steps

## Hook Configuration Details

The hooks are configured in `~/.claude/settings.json` with:
- **PreToolUse hooks**: Run before commands, can block execution
- **PostToolUse hooks**: Run after commands, provide helpful suggestions

## Why poetry run is unnecessary

Claude Code automatically activates the virtual environment, so:
- ❌ `poetry run pytest` → ✅ `pytest`
- ❌ `poetry run python script.py` → ✅ `python script.py`
- ❌ `poetry run mypy src/` → ✅ `mypy src/`

## Troubleshooting Steps

### If hooks are not working:
1. Check `~/.claude/settings.json` exists and is valid JSON
2. Restart Claude Code WITHOUT using --continue flag
3. Verify you're not in a subdirectory that overrides settings

### To manually check hook configuration:
```bash
cat ~/.claude/settings.json | grep -A5 "poetry run"
```

### Common issues:
- **Old message showing**: Restart Claude Code to reload settings
- **Hooks not triggering**: Check JSON syntax in settings.json
- **"Is a directory" errors**: Windows subprocess issues, check paths

## Full Test Suite

Run complete test suite for all Claude mods:

### Quick Test (Essential Checks)
```bash
echo "=== Claude Mods Quick Test Suite ==="

# 0. Configuration check (NEW)
echo "Permission rules: $(grep -c '"action"' ~/.claude/settings.json 2>/dev/null || echo 0)"
echo "Hook commands: $(grep -c '"command"' ~/.claude/settings.json 2>/dev/null || echo 0)"

# 1. Basic blocks (hooks)
poetry run pytest 2>&1 | grep -q "not necessary" && echo "✓ Poetry run block working" || echo "✗ Poetry run block FAILED"

# 2. Permission rule blocks (NEW)
pip install test 2>&1 | grep -q "denied\|blocked" && echo "✓ Pip install block working" || echo "✗ Pip install block FAILED"

# 3. Git workflow
git checkout -b test/quick-check 2>&1 | grep -q "workflow" && echo "✓ Branch detection working" || echo "✗ Branch detection FAILED"
git branch -D test/quick-check 2>/dev/null

# 4. Direct commands
python --version >/dev/null 2>&1 && echo "✓ Direct Python working" || echo "✗ Direct Python FAILED"
pytest --version >/dev/null 2>&1 && echo "✓ Direct pytest working" || echo "✗ Direct pytest FAILED"

echo "=== Quick Test Complete ==="
```

### Comprehensive Test (All Features)
```bash
echo "=== Claude Mods Comprehensive Test Suite ==="

# Test Categories:
# 1. Permission Rules (5 tests) - NEW
# 2. Command Blocks (5 tests)
# 3. Git Workflow Automation (6 tests)
# 4. Poetry Integration (3 tests)
# 5. Branch Protection (4 tests)
# 6. Developer Assistance (3 tests)

# Run each category...
echo "See detailed test sections above for comprehensive testing"
echo "Total permission rules: $(grep -c '"action"' ~/.claude/settings.json)"
echo "Total hook commands: $(grep -c '"command"' ~/.claude/settings.json)"
echo "=== Comprehensive Test Complete ==="
```

## Test Results Summary

After running tests, you should see:
- ✅ **Permission Rules**: Lock files protected, dependency edits blocked, main branch protected
- ✅ **Command Blocks**: Poetry run, dangerous commands blocked  
- ✅ **Git Automation**: Branch sync, behind detection, smart suggestions
- ✅ **Poetry Integration**: Auto lock updates, commit reminders
- ✅ **Branch Protection**: Push blocks when outdated, conflict prevention
- ✅ **Developer Assistance**: Helpful messages, exact fix commands

## Success Indicators

Your Claude mods are working correctly if:
1. No more merge conflicts due to outdated branches
2. Poetry.lock always stays in sync
3. Git operations provide helpful guidance
4. Dangerous operations are prevented
5. Development workflow feels smoother

## Customization

To add or modify tests, edit this file and the hooks in `~/.claude/settings.json`.