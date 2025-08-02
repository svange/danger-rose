Start working - simple and flexible: $ARGUMENTS

Begin working on your selected task with minimal friction. Works on any branch, including main.

## Usage

```bash
/sv-start-work
```

Uses the selection from `/sv-choose-what-to-work-on` or accepts direct input.

## 1. Load or Determine Work Context

```bash
# Check if we have a previous selection
if [ -f ".sv-work-selection" ]; then
    WORK_DESC=$(head -1 .sv-work-selection)
    ISSUE_INFO=$(grep "^ISSUE:" .sv-work-selection 2>/dev/null || echo "")
    echo "📋 Starting work on: $WORK_DESC"
else
    # No previous selection, check arguments or ask
    if [ -n "$ARGUMENTS" ]; then
        WORK_DESC="$ARGUMENTS"
    else
        echo "What are you working on? (or run /sv-choose-what-to-work-on first)"
        exit 1
    fi
fi
```

## 2. Handle Current Changes (Simply)

```bash
# Check for uncommitted changes
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    echo "📝 You have uncommitted changes:"
    git status -s
    echo ""
    echo "Options:"
    echo "1) Save them with a WIP commit"
    echo "2) Stash them"
    echo "3) Keep working with these changes"

    # Example for option 1:
    # git add -A && git commit -m "WIP: $WORK_DESC"

    # Example for option 2:
    # git stash push -m "WIP: Before starting $WORK_DESC"

    # Option 3: Just continue
fi
```

## 3. Decide on Branching (Or Not)

```bash
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "none")

echo "🌿 Current branch: $CURRENT_BRANCH"

# For personal projects, working on main is fine!
if [[ "$CURRENT_BRANCH" == "main" ]] || [[ "$CURRENT_BRANCH" == "master" ]]; then
    echo "📍 Working on $CURRENT_BRANCH branch (that's OK!)"
    echo ""
    echo "Options:"
    echo "1) Continue on $CURRENT_BRANCH"
    echo "2) Create a feature branch"

    # If creating branch, keep it simple
    if create_branch; then
        # Simple branch name - no conventions required
        BRANCH_NAME=$(echo "$WORK_DESC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | cut -c1-30)
        git checkout -b "$BRANCH_NAME"
        echo "Created branch: $BRANCH_NAME"
    fi
fi

# Pull latest to avoid conflicts (if on main)
if [[ "$CURRENT_BRANCH" == "main" ]] || [[ "$CURRENT_BRANCH" == "master" ]]; then
    echo "📥 Getting latest changes..."
    git pull --rebase 2>/dev/null || echo "No remote to pull from"
fi
```

## 4. Create Simple Work Context

```bash
# Just a simple note about what we're doing
cat > .current-work << EOF
Working on: $WORK_DESC
Started: $(date)
Branch: $CURRENT_BRANCH
$ISSUE_INFO
EOF

echo "📝 Created .current-work file"
```

## 5. Optional Development Setup

```bash
# Only run setup if it exists and user wants it
if [ -f "Makefile" ]; then
    echo "🔧 Found Makefile. Run 'make' if you need to set up."
fi

if [ -f "package.json" ] && [ ! -d "node_modules" ]; then
    echo "📦 Tip: Run 'npm install' if you need dependencies"
fi

if [ -f "requirements.txt" ]; then
    echo "🐍 Tip: Run 'pip install -r requirements.txt' if needed"
fi
```

## 6. Ready to Work!

```
✅ Ready to work on: $WORK_DESC

💡 Tips:
- Make your changes
- Test as you go
- Commit whenever you want
- When done: /sv-ship

No pressure, just have fun coding! 🎮
```

## Key Differences from Enterprise Version

### What This Command Does
- Works on any branch (including main)
- Creates simple branch names (or none at all)
- Doesn't enforce any structure
- Gives helpful tips instead of requirements
- Prevents basic merge conflicts

### What This Command Doesn't Do
- Doesn't require feature branches
- Doesn't enforce naming conventions
- Doesn't run automatic setup
- Doesn't validate branch state
- Doesn't require clean working directory

## Flexibility Examples

### Working on Main
```
Current branch: main
→ Working on main branch (that's OK!)
→ Getting latest changes...
→ Ready to work!
```

### Simple Branch Names
```
Working on: "add new boss character"
→ Created branch: add-new-boss-character
```

### Keep Current Changes
```
You have uncommitted changes:
M src/game.py
→ Options: save, stash, or keep working
→ Keeping current changes and continuing...
```

## Conflict Prevention

Even in simple mode, we help prevent problems:
- Pull latest when on main
- Offer to stash changes
- Create branches when it makes sense
- But never force anything

## Integration with Workflow

Part of the simple workflow:
1. `/sv-choose-what-to-work-on` - Pick work
2. `/sv-start-work` - This command
3. Make changes freely
4. `/sv-ship` - Share your work

## Perfect For

- Quick fixes
- Experiments
- Learning projects
- Game jams
- Personal projects
- Having fun with code

Remember: The goal is to reduce friction and let you focus on coding!
