Choose what to work on - flexible and simple: $ARGUMENTS

Find or describe what you want to work on, without rigid conventions.

## Usage Examples
- `/sv-choose-what-to-work-on 24` - Work on issue #24
- `/sv-choose-what-to-work-on fix the login bug` - Search for matching issues
- `/sv-choose-what-to-work-on add a new boss character` - Freeform work (no issue needed)
- `/sv-choose-what-to-work-on` - See what's available to work on

## 1. Understand the Request

```bash
# Check if we're in a git repo (optional for personal projects)
if git rev-parse --git-dir > /dev/null 2>&1; then
    IN_GIT_REPO=true
    REPO_URL=$(git remote get-url origin 2>/dev/null || echo "")
else
    IN_GIT_REPO=false
    echo "📝 Note: Not in a git repository. That's OK!"
fi
```

Analyze $ARGUMENTS:
- **Numeric** (e.g., "24") → Look for issue #24
- **Issue reference** (e.g., "#24") → Direct issue lookup
- **Keywords** → Search for matching work
- **Freeform text** → Just describe what you want to do
- **Empty** → Show options

## 2. If Issue Number Provided

```bash
# Simple issue lookup if number provided
if [[ "$ARGUMENTS" =~ ^#?[0-9]+$ ]]; then
    ISSUE_NUM=${ARGUMENTS#\#}

    if [ "$IN_GIT_REPO" = true ] && [ -n "$REPO_URL" ]; then
        echo "📋 Looking up issue #$ISSUE_NUM..."
        # Use mcp__github__get_issue if available
        # Show issue details
    else
        echo "📝 Planning to work on: Issue #$ISSUE_NUM"
    fi
fi
```

## 3. If Keywords/Search Terms

```bash
# Search for related work
if contains_keywords "$ARGUMENTS"; then
    echo "🔍 Searching for: $ARGUMENTS"

    if [ "$IN_GIT_REPO" = true ] && github_available; then
        # Search GitHub issues
        # Show matching results
        echo "Found these related items:"
        echo "1. #123 - Fix login timeout issue"
        echo "2. #456 - Add login rate limiting"
        echo "3. Or just work on: '$ARGUMENTS' without an issue"
    else
        echo "📝 Planning to work on: $ARGUMENTS"
    fi
fi
```

## 4. If No Arguments (Browse Mode)

```bash
if [ -z "$ARGUMENTS" ]; then
    echo "🤔 What would you like to work on?"

    if [ "$IN_GIT_REPO" = true ] && github_available; then
        echo ""
        echo "=== Recent Issues ==="
        # Show recent issues
        echo "1. #789 - Add save game feature"
        echo "2. #790 - Fix collision detection"
        echo "3. #791 - New background music"

        echo ""
        echo "=== Recent Files Modified ==="
        # Show recently modified files
        git log --name-only --pretty=format: -10 | sort | uniq -c | sort -rn | head -5

        echo ""
        echo "=== Or Work On Something New ==="
        echo "Just run: /sv-choose-what-to-work-on describe what you want"
    else
        echo "Some ideas:"
        echo "- Fix a bug you noticed"
        echo "- Add a new feature"
        echo "- Improve documentation"
        echo "- Refactor messy code"
        echo ""
        echo "Just run: /sv-choose-what-to-work-on describe what you want"
    fi
fi
```

## 5. Confirm Selection

```bash
# Simple confirmation of what we're working on
echo ""
echo "✅ Ready to work on: $WORK_DESCRIPTION"
echo ""
echo "Next step: /sv-start-work"
echo ""

# Save selection for next command
echo "$WORK_DESCRIPTION" > .sv-work-selection

# If it's an issue, save that info too
if [ -n "$ISSUE_NUM" ]; then
    echo "ISSUE:$ISSUE_NUM" >> .sv-work-selection
fi
```

## Key Differences from Enterprise Version

### What This Command Does
- Accepts any work description (no issue required)
- Doesn't enforce any naming conventions
- Works without GitHub if needed
- Keeps things simple and flexible

### What This Command Doesn't Do
- Doesn't require issues to exist
- Doesn't enforce project structure
- Doesn't validate against labels/priorities
- Doesn't score or rank issues

## Examples of Flexibility

### Working Without Issues
```
/sv-choose-what-to-work-on add particle effects to the victory screen
→ ✅ Ready to work on: add particle effects to the victory screen
```

### Casual Issue Reference
```
/sv-choose-what-to-work-on that bug with the jumping
→ Found: #234 - Player can double-jump infinitely
→ ✅ Ready to work on: #234 - Player can double-jump infinitely
```

### Quick Fixes
```
/sv-choose-what-to-work-on typo in readme
→ ✅ Ready to work on: typo in readme
```

## Integration with Workflow

This starts the simple personal workflow:
1. `/sv-choose-what-to-work-on` - Pick or describe work
2. `/sv-start-work` - Begin working (any branch, even main)
3. Make your changes
4. `/sv-ship` - Commit and push (simple process)

## No Enforcement

This command intentionally:
- Doesn't enforce issue tracking
- Doesn't require specific formats
- Doesn't validate selections
- Lets you work how you want

Perfect for:
- Personal projects
- Game development
- Quick experiments
- Learning projects
- Fun coding sessions
