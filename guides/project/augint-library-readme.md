# Auto-Merge Configuration for Downstream APIs

## Overview

This library is designed to trigger automatic dependency updates in downstream API repositories (like `augint-api`) through Dependabot. To enable seamless auto-merge of these updates, you need to configure GitHub repository settings.

## Quick Setup

### Option 1: Automated Setup (Recommended)

```bash
# Copy the bootstrap script to your augint-library directory
cp path/to/augint-api/bootstrap-github-auto-merge.sh .

# Make it executable and run it
chmod +x bootstrap-github-auto-merge.sh
./bootstrap-github-auto-merge.sh
```

### Option 2: Manual Setup

1. **Enable Auto-Merge via GitHub CLI:**
   ```bash
   gh repo edit --enable-auto-merge
   ```

2. **Or enable via GitHub Web Interface:**
   - Go to repository Settings → General
   - Scroll to "Pull Requests" section  
   - Check ☑️ "Allow auto-merge"
   - Save changes

## How It Works

When you publish a new version of this library:

1. **Library Release** → New version published to PyPI
2. **Dependabot Detection** → Detects new version in downstream APIs
3. **PR Creation** → Creates pull request with dependency update
4. **Auto-Merge** → Automatically merges if all checks pass

## Downstream Repository Requirements

For auto-merge to work, downstream repositories (like `augint-api`) need:

- ✅ Auto-merge enabled (this setup)
- ✅ Dependabot configured for Python dependencies
- ✅ Auto-merge workflow configured
- ✅ Required status checks passing

## Triggering Test Updates

To test the auto-merge pipeline:

```bash
# 1. Make a minor change to the library
echo "# Test update" >> README.md

# 2. Commit with semantic versioning
git add .
git commit -m "docs: test auto-merge pipeline"

# 3. Push to trigger release
git push origin main

# 4. Wait for semantic-release to create new version
# 5. Check downstream repositories for auto-merge PR
```

## Security Considerations

Auto-merge only applies to:
- ✅ **Minor and patch updates** (e.g., 1.2.3 → 1.2.4 or 1.2.3 → 1.3.0)
- ✅ **Dependabot-created PRs**
- ✅ **PRs that pass all required checks**

Major version updates (1.x.x → 2.x.x) always require manual review.

## Troubleshooting

### Auto-merge not working?

1. **Check repository settings:**
   ```bash
   # Verify auto-merge is enabled
   gh repo view --json autoMergeAllowed
   ```

2. **Check Dependabot configuration** in downstream repos
3. **Verify status checks** are passing
4. **Check workflow permissions** in downstream repos

### Common Issues

- **Permission errors:** Ensure GitHub token has `repo` scope
- **Status check failures:** Review CI/CD pipeline logs
- **Manual approval required:** Major version updates need manual merge

---

**Need help?** Check the [augint-api repository](https://github.com/svange/augint-api) for working auto-merge configuration examples.
