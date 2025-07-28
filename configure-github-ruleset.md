# GitHub Ruleset Configuration for Danger Rose

## Current Status
- ✅ CI workflow has auto-merge job configured
- ✅ Repository auto-merge is enabled
- ✅ Ruleset "main-branch-protection" is active
- ✅ Delete branch on merge is enabled
- ✅ Recent CI fix has been pushed (Path.home() issue)

## Configuration Complete!
The repository is now configured with:
- Auto-merge enabled for the repository
- Automatic branch deletion after merge
- Main branch protection via ruleset
- Required status check: "Code Quality & Tests"
- No approval required (0 approvals)
- PR conversations must be resolved

## Step 1: Enable Repository Settings

First, enable auto-merge and automatic branch deletion:

```bash
# Enable auto-merge for the repository
gh api repos/svange/danger-rose --method PATCH \
  --field allow_auto_merge=true \
  --field delete_branch_on_merge=true
```

## Step 2: Create Ruleset for Main Branch

Since GitHub Rulesets are the modern approach (replacing branch protection rules), we'll create a ruleset:

```bash
# Create ruleset for main branch protection
gh api repos/svange/danger-rose/rulesets \
  --method POST \
  --field name="main-branch-protection" \
  --field enforcement="active" \
  --field target="branch" \
  --field-json conditions='{"ref_name":{"include":["~DEFAULT_BRANCH"],"exclude":[]}}' \
  --field-json rules='[
    {
      "type": "required_status_checks",
      "parameters": {
        "required_status_checks": [
          {
            "context": "Code Quality & Tests",
            "integration_id": null
          }
        ],
        "strict_required_status_checks_policy": false
      }
    },
    {
      "type": "pull_request",
      "parameters": {
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_approving_review_count": 0,
        "required_review_thread_resolution": true
      }
    }
  ]' \
  --field-json bypass_actors='[]'
```

## Step 3: Test Configuration

After applying these settings:

1. Create a test branch and PR
2. Verify status checks appear
3. Confirm auto-merge enables after checks pass
4. Ensure branch is deleted after merge

## Notes

- The CI already has an auto-merge job that triggers on feature branches
- Required status check: "Code Quality & Tests"
- No approval required (set to 0) since auto-merge from CI
- Conversations must be resolved before merge
- Stale reviews are dismissed on new pushes

## Manual Configuration (Alternative)

If you prefer to configure via GitHub UI:

1. Go to Settings → General
   - ✅ Allow auto-merge
   - ✅ Automatically delete head branches

2. Go to Settings → Rules → Rulesets → New ruleset
   - Name: `main-branch-protection`
   - Enforcement: Active
   - Target: Include default branch
   - Rules:
     - ✅ Require status checks to pass
       - Add: "Code Quality & Tests"
     - ✅ Require a pull request before merging
       - Required approvals: 0
       - ✅ Dismiss stale reviews
       - ✅ Require conversation resolution

## Current CI Workflow Status

The `game-ci.yaml` already includes:
- Quality checks job
- Test game job
- Build executables job
- Auto-merge job (lines 316-407)

The auto-merge job:
- Triggers on PRs to main from feat/* or fix/* branches
- Waits for quality checks to pass
- Enables auto-merge with squash strategy
- Adds a comment confirming auto-merge

## Issue to Fix

The Windows CI is still disabled due to Poetry installation issues (#54). This should be addressed separately.
