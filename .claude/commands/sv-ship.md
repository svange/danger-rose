Ship your work - simple and friendly: $ARGUMENTS

Commit and share your changes with minimal friction. No conventions enforced.

## Usage

```bash
/sv-ship
```

Commits all changes and pushes them. Simple as that!

## 1. Check What We're Shipping

```bash
# Show what's changed
echo "📦 Changes to ship:"
git status -s

# Show a summary
git diff --stat

# If no changes
if [ -z "$(git status --porcelain)" ]; then
    echo "✨ Everything is already committed!"
    echo "Push to remote? (y/n)"
    # If yes: git push
    exit 0
fi
```

## 2. Prepare Changes

```bash
# Add all changes (simple approach)
echo "📝 Preparing changes..."
git add -A

# Show what we're about to commit
echo ""
echo "Files to commit:"
git diff --cached --name-only
```

## 3. Create Simple Commit

```bash
# Check if we have work context
if [ -f ".current-work" ]; then
    WORK_DESC=$(grep "Working on:" .current-work | cut -d: -f2- | xargs)
    echo "📋 Working on: $WORK_DESC"
else
    WORK_DESC=""
fi

# Generate a simple, friendly commit message
if [ -n "$WORK_DESC" ]; then
    DEFAULT_MESSAGE="$WORK_DESC"
else
    # Analyze changes for a simple message
    if mostly_added_files; then
        DEFAULT_MESSAGE="Add new features"
    elif mostly_modified_files; then
        DEFAULT_MESSAGE="Update code"
    elif mostly_deleted_files; then
        DEFAULT_MESSAGE="Clean up files"
    else
        DEFAULT_MESSAGE="Update project"
    fi
fi

# Offer to customize
echo ""
echo "💬 Commit message: $DEFAULT_MESSAGE"
echo "Press Enter to use this, or type a new message:"
# Read user input, use default if empty

# Make the commit
git commit -m "$COMMIT_MESSAGE"
```

## 4. Handle Pushing

```bash
CURRENT_BRANCH=$(git branch --show-current)

# Check if we need to push
if ! git diff HEAD origin/$CURRENT_BRANCH --quiet 2>/dev/null; then
    echo "📤 Pushing to remote..."
    
    # Try to push
    if ! git push 2>/dev/null; then
        # No upstream? Set it up
        echo "🔗 Setting up remote tracking..."
        git push -u origin $CURRENT_BRANCH
    fi
else
    echo "✅ Already up to date with remote!"
fi

# If on main and push fails due to divergence
if [[ "$CURRENT_BRANCH" == "main" ]] && push_failed_due_to_divergence; then
    echo "⚠️  Remote has new changes. Let's sync up:"
    echo ""
    echo "Options:"
    echo "1) Pull and merge changes"
    echo "2) Pull with rebase"
    echo "3) Create a branch for your changes"
    
    # Handle based on choice
    # Option 1: git pull
    # Option 2: git pull --rebase
    # Option 3: git checkout -b my-changes && git push -u origin my-changes
fi
```

## 5. Optional: Create Simple PR

```bash
# Only if not on main and user wants it
if [[ "$CURRENT_BRANCH" != "main" ]] && github_available; then
    echo ""
    echo "🔀 Create a pull request? (y/n)"
    
    if create_pr; then
        # Simple PR
        gh pr create \
          --title "$COMMIT_MESSAGE" \
          --body "## Changes
          
$WORK_DESC

Made with ❤️"
        
        echo "✅ Pull request created!"
    fi
fi
```

## 6. Success!

```
✅ Work shipped successfully!

Branch: $CURRENT_BRANCH
Commit: $COMMIT_MESSAGE

🎉 Great job! Your changes are saved and shared.

Next: 
- Take a break ☕
- Or start something new: /sv-choose-what-to-work-on
```

## Simple Commit Messages

This command creates friendly, simple commits:

### Examples
- "Add particle effects"
- "Fix jumping bug"
- "Update player sprite"
- "Add new level"
- "Fix typo in readme"

No conventions required! Just describe what you did.

## Conflict Handling (Simple)

If pushing fails due to conflicts:

```bash
echo "📝 Someone else made changes too!"
echo "Let's get their changes first:"

# Simple merge approach
git pull

# If merge conflicts
if merge_conflicts; then
    echo "🤝 Need to combine changes:"
    echo "1. Fix the conflicts in your editor"
    echo "2. Run: git add -A"
    echo "3. Run: git commit"
    echo "4. Run: /sv-ship again"
fi
```

## Key Differences from Enterprise Version

### What This Command Does
- Simple, descriptive commits (no format required)
- Works with any branch
- Helps with basic conflict resolution
- Optional PR creation
- Friendly success messages

### What This Command Doesn't Do
- No conventional commits required
- No pre-commit hooks
- No automated tests
- No complex PR templates
- No issue linking required

## Perfect For

### Quick Fixes
```
Working on: typo in readme
→ Commit: "Fix typo in readme"
→ Pushed to main ✅
```

### Feature Work
```
Working on: add new boss character
→ Commit: "Add new boss character"
→ Create PR? Yes
→ PR created ✅
```

### Experiments
```
Working on: trying new physics engine
→ Commit: "Experiment with new physics"
→ Pushed to branch: physics-experiment ✅
```

## Tips for Success

1. **Commit Often**: No need to wait for "perfect" code
2. **Simple Messages**: Just describe what you did
3. **Push Regularly**: Share your progress
4. **Have Fun**: This is your project!

## Integration with Workflow

Completes the simple workflow:
1. `/sv-choose-what-to-work-on` - Pick work
2. `/sv-start-work` - Begin coding
3. Make changes
4. `/sv-ship` - This command

Then repeat! Keep it simple, keep it fun.