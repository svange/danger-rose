Find GitHub issue by number or description: $ARGUMENTS

Follow these steps:

1. **Determine current repository**:
   - Check git remote: `git remote get-url origin`
   - Extract owner/repo from URL
   - If not a git repo, inform user and exit

2. **Parse the input**:
   - If numeric: treat as issue number
   - If text: treat as search query

3. **For issue number**:
   Use `mcp__github__get_issue` to fetch:
   - Title, state, labels, assignees
   - Issue body and comments
   - Related PR if linked

4. **For keyword search**:
   Use `mcp__github__search_issues` with:
   - Query: `$ARGUMENTS in:title,body repo:owner/name`
   - Sort by relevance or updated
   - Show top 5-10 results
   Note: Replace owner/name with actual repo from step 1

5. **Display format**:
   ```
   #123 [open] Title of issue
   Labels: bug, enhancement
   Assignee: @username

   Description preview...

   Last activity: 2 days ago
   ```

6. **Additional context**:
   - Check for linked PRs
   - Show related issues if mentioned
   - Display priority indicators

## Usage Examples
- `/ai-find-issue 123` - Get issue #123
- `/ai-find-issue authentication bug` - Search for auth issues
- `/ai-find-issue "AI SRE"` - Search exact phrase

## Best Practices
- Include repository context when searching
- Show actionable information upfront
- Highlight blockers or dependencies
