Comprehensive repository health check and maintenance: $ARGUMENTS

Perform deep analysis of repository health, update issues, find problems, and suggest improvements. Run periodically for repository hygiene.

## Phase 1: Issue Analysis & Updates

1. **Scan all open issues**:
   Use `mcp__github__list_issues` with state:open:
   ```
   For each issue:
   - Check last activity date
   - Verify referenced code still exists
   - Check if already implemented
   - Look for duplicate issues
   - Verify labels are appropriate
   ```

2. **Update issue status**:
   Use `mcp__github__update_issue`:
   - Mark stale issues (>60 days no activity)
   - Close completed issues (work already done)
   - Add missing labels (bug, enhancement, etc.)
   - Link related issues

3. **Issue quality check**:
   - Missing acceptance criteria
   - No assignee but has activity
   - High priority but no recent updates
   - Blocked issues without blocker resolution

## Phase 2: Code & Documentation Analysis

4. **Documentation consistency**:
   ```bash
   # Check README completeness
   grep -E "(Installation|Usage|Testing|Contributing)" README.md

   # Find outdated examples
   grep -r "version\|v[0-9]" docs/ --include="*.md"

   # Broken internal links
   find . -name "*.md" -exec grep -l "\[.*\](\..*)" {} \;
   ```

5. **Code hygiene scan**:
   ```bash
   # TODO/FIXME comments
   grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.py" --include="*.js"

   # Large files that shouldn't be committed
   find . -size +5M -type f | grep -v ".git"

   # Generated files in repo
   find . -name "*.pyc" -o -name "__pycache__" -o -name "*.log"
   ```

6. **Dependency analysis**:
   ```bash
   # Python: Check for unused
   pip list --outdated
   safety check

   # JavaScript: Check vulnerabilities
   npm audit
   npm outdated
   ```

## Phase 3: Git Repository Health

7. **Branch cleanup**:
   ```bash
   # List merged branches
   git branch -r --merged main | grep -v main

   # Stale branches (no commits in 30 days)
   git for-each-ref --format='%(refname:short) %(committerdate)' refs/remotes
   ```

8. **Repository sync status**:
   ```bash
   # Check remote status
   git fetch --all --prune
   git branch -vv | grep -E "ahead|behind"

   # Uncommitted changes check
   git status --porcelain
   ```

## Phase 4: Performance & Quality Metrics

9. **Test coverage analysis**:
   ```bash
   # Python coverage gaps
   coverage report --show-missing

   # Find untested modules
   find . -name "*.py" | while read f; do
     test_file="${f/src/tests}"
     test_file="${test_file/.py/_test.py}"
     [[ ! -f "$test_file" ]] && echo "Missing test: $f"
   done
   ```

10. **Build performance**:
    ```bash
    # Measure test execution time
    time make test

    # Check for slow tests
    pytest --durations=10
    ```

## Phase 5: Technology Recommendations

11. **Analyze code patterns** for library suggestions:
    - Authentication → suggest `python-jose`, `authlib`
    - API development → suggest `fastapi`, `pydantic`
    - Data processing → suggest `polars`, `dask`
    - Testing → suggest `hypothesis`, `pytest-benchmark`

12. **Architecture improvements**:
    - Identify tightly coupled modules
    - Suggest microservice boundaries
    - Recommend caching strategies
    - Propose async opportunities

## Phase 6: Generate Report & Actions

13. **Create health report**:
    ```markdown
    # Repository Health Report - [DATE]

    ## Executive Summary
    - Issues needing attention: X
    - Code quality score: X/100
    - Documentation completeness: X%
    - Test coverage: X%

    ## Critical Findings
    1. [Security vulnerabilities found]
    2. [Performance bottlenecks]
    3. [Maintainability concerns]

    ## Completed Actions
    - Closed X obsolete issues
    - Updated Y issue labels
    - Identified Z improvement opportunities

    ## Recommended Actions
    ### Immediate (This Week)
    - Fix security vulnerabilities
    - Clean up X stale branches
    - Update outdated dependencies

    ### Short Term (This Month)
    - Implement missing tests
    - Refactor module X
    - Add documentation for Y

    ### Long Term (This Quarter)
    - Migrate to technology X
    - Restructure for better modularity
    - Implement performance monitoring

    ## New Issue Suggestions
    1. "Add integration tests for API endpoints"
    2. "Implement caching for expensive operations"
    3. "Create architecture decision records"

    ## Technology Recommendations
    1. **structlog** - Better structured logging
    2. **ruff** - Faster Python linting
    3. **hypothesis** - Property-based testing
    ```

14. **Create fix branch if needed**:
    ```bash
    # If fixes are needed
    git checkout -b chore/repo-health-[DATE]

    # Apply automatic fixes
    - Remove generated files
    - Update .gitignore
    - Fix simple documentation issues
    - Update dependency versions

    # Commit categorized changes
    git add .gitignore
    git commit -m "chore: update gitignore for generated files"
    ```

15. **Create GitHub issues**:
    Use `mcp__github__create_issue` for:
    - Each major finding
    - Suggested improvements
    - Technology adoptions

## Advanced Checks

### Security Scan
```bash
# Secret detection
truffleHog --regex --entropy=False .

# Dependency vulnerabilities
bandit -r src/
pip-audit
```

### Performance Analysis
```bash
# Profile slow code paths
python -m cProfile -o profile.stats main.py

# Memory leaks
python -m tracemalloc
```

### Architecture Metrics
- Cyclomatic complexity
- Module coupling
- Code duplication
- Technical debt calculation

## Output Locations
- Full report: `reports/health-check-[DATE].md`
- Issue updates: GitHub Issues
- Fix branch: `chore/repo-health-[DATE]`
- Metrics: `metrics/health-[DATE].json`

This comprehensive check ensures repository health, identifies improvement opportunities, and maintains high code quality standards.
