Intelligently select a GitHub issue to work on: $ARGUMENTS

Follow these steps:

1. **Determine current repository**:
   - Check git remote: `git remote get-url origin`
   - Extract owner/repo from URL
   - If not a git repo, inform user and exit

2. **Parse selection criteria**:
   - Default: balanced (priority + ease)
   - Options: priority, ease, impact, learning
   - Custom: $ARGUMENTS (e.g., "security", "performance")

3. **Fetch candidate issues**:
   Use `mcp__github__search_issues`:
   ```
   Queries by criteria:
   - Priority: `label:P0,P1,critical state:open repo:owner/name`
   - Ease: `label:good-first-issue,easy state:open repo:owner/name`
   - Impact: `label:enhancement reactions:>5 repo:owner/name`
   - Bug fixes: `label:bug state:open repo:owner/name`
   ```
   Note: Replace owner/name with actual repo from step 1

4. **Score each issue**:
   ```
   Scoring factors:
   - Age: Older = higher priority
   - Labels: P0=10, P1=7, P2=4, bug=5
   - Reactions: Community interest
   - Comments: Complexity indicator
   - Assignee: Unassigned preferred
   ```

5. **Filter by constraints**:
   - My expertise areas
   - Available time estimate
   - Dependencies/blockers
   - Related to recent work

6. **Present top 3 candidates**:
   ```
   === Recommended Issues ===

   1. #123 [Score: 85] Fix authentication timeout
      - High priority bug affecting users
      - Clear reproduction steps
      - Estimated: 2-4 hours

   2. #456 [Score: 72] Add metrics dashboard
      - High impact feature
      - Good first issue for monitoring
      - Estimated: 1 day
   ```

## Selection Algorithm
- Weight factors based on criteria
- Consider issue interconnections
- Prefer issues with clear scope
- Avoid blocked/waiting issues

## Recommendation Output
- Why this issue was selected
- What skills it will develop
- Potential challenges
- Related issues to consider
