Find related GitHub issues in the current repository: $ARGUMENTS

Follow these steps:

1. **Determine current repository**:
   - Check git remote: `git remote get-url origin`
   - Extract owner/repo from URL
   - If not a git repo, inform user and exit

2. **Extract key terms**:
   - Parse $ARGUMENTS for keywords
   - Identify technical terms, components
   - Build search variations

3. **Search within current repository only**:
   Use `mcp__github__search_issues` with:
   ```
   Query patterns:
   - `$ARGUMENTS repo:owner/name state:open`
   - `$ARGUMENTS repo:owner/name is:issue`
   - Related terms in:title,body,comments
   ```
   Note: Replace owner/name with actual repo from step 1

4. **Categorize results**:
   - **Direct matches**: Issues mentioning exact terms
   - **Component related**: Same subsystem/module
   - **Dependency chain**: Blocking/blocked by
   - **Similar problems**: Pattern matching

5. **Analyze relationships**:
   - Cross-references between issues (#123 mentions)
   - Shared labels or milestones
   - Common assignees or mentions
   - Timeline correlations

6. **Present findings**:
   ```
   === Repository: owner/repo ===

   Direct References (3):
   #123 - Authentication refactor
   #456 - Update auth UI components

   Same Component (5):
   #789 - Auth module unit tests

   May Block/Impact (2):
   #234 - API versioning changes
   ```

## Advanced Patterns
- Check issue bodies for `#\d+` references
- Search PR descriptions for issue links
- Look for "depends on", "blocked by" keywords
- Consider closed issues for context

## Output Options
- Sort by relevance/recency
- Show dependency graph if complex
