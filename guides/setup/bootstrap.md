# Bootstrap Setup Guide

**📋 This file contains detailed setup instructions. Delete it after your project is fully configured.**

This guide will walk you through setting up your new Python library project with enterprise-grade CI/CD using the augint-library template.

## 🎯 Overview

The bootstrap process uses a **two-stage approach** that eliminates common setup friction:

- **Stage 1**: Template customization (no dependencies required)
- **Stage 2**: AWS integration (after manual SAM setup)

This approach prevents dependency conflicts and handles the interactive SAM pipeline setup gracefully.

### Stage 1: Initial Setup (No Dependencies)
```bash
# Run BEFORE poetry install
python bootstrap-stage1.py
```

This will:
- ✅ Detect your GitHub repository from git remote
- ✅ Create initial .env file with placeholders
- ✅ Replace template strings with your project name
- ✅ Reset version to 0.0.0 for new projects
- ✅ Show clear next steps

### Manual Steps
After Stage 1, you need to:

1. **Add GitHub Token** to `.env` file
   - Generate at: https://github.com/settings/tokens
   - Required permissions: `repo`, `workflow`

2. **Install Dependencies**
   ```bash
   poetry install
   ```

3. **Create AWS Pipeline** (interactive process)
   ```bash
   sam pipeline bootstrap --stage <project-name>-testing
   ```

   **When prompted:**
   - CI/CD provider: Choose **"GitHub Actions"**
   - Repository: Enter your full repo name (e.g., `svange/augint-api`)
   - Branch: Use **"main"** (or your default branch)
   - Stage name: Use **`<project-name>-testing`** convention
   - Region: Accept default or choose your preferred region

   **✅ Success indicators:**
   - Creates `.aws-sam/pipeline/pipelineconfig.toml`
   - Shows ARNs for execution roles and S3 bucket
   - Configures IAM roles for your repository

### Stage 2: Complete Setup (With Dependencies)
```bash
# Run AFTER sam pipeline bootstrap
python bootstrap-stage2.py
```

**What Stage 2 does:**
- ✅ **Extracts AWS resources** from SAM config files
- ✅ **Updates .env** with pipeline ARNs, bucket name, and account ID
- ✅ **Configures IAM trust policy** for GitHub Actions OIDC authentication
- ✅ **Verifies OIDC provider** exists (creates if needed with your permission)

**Interactive prompts:**
- Trust policy update confirmation
- OIDC provider creation (if needed)

**✅ Success indicators:**
- `.env` file populated with AWS resource ARNs
- Trust policy updated for GitHub Actions
- All environment variables ready for CI/CD

## 🎯 Why Two-Stage Bootstrap?

The two-stage approach solves several problems:
- **No dependency conflicts** - Stage 1 runs before `poetry install`
- **Manual AWS setup** - No hanging on interactive SAM commands
- **Clear separation** - Template setup vs. AWS infrastructure
- **Better error handling** - Each stage has focused responsibilities

## ✅ Complete Setup Checklist

**Stage 1 - Template Setup:**
- [ ] Run `python bootstrap-stage1.py`
- [ ] Add GitHub token to `.env` file
- [ ] Run `poetry install`

**Manual AWS Setup:**
- [ ] Run `sam pipeline bootstrap --stage <project-name>-testing`
- [ ] Verify `.aws-sam/pipeline/pipelineconfig.toml` was created

**Stage 2 - AWS Integration:**
- [ ] Run `python bootstrap-stage2.py`
- [ ] Confirm trust policy update when prompted
- [ ] Verify `.env` file has all AWS resource ARNs

**Development Environment:**
- [ ] Secure `.env` with chezmoi: `chezmoi add .env`
- [ ] Run `poetry run pre-commit install`
- [ ] Run `poetry run pytest` to verify setup

**Repository Configuration:**
- [ ] Configure branch protection rules
- [ ] Set up PyPI trusted publishing
- [ ] Make initial commit and push

**Cleanup:**
- [ ] Delete this `BOOTSTRAP.md` file
- [ ] Review and customize `README.md` for your project

## 🔧 Troubleshooting

### Stage 1 Issues

**Repository name truncation (e.g., `augint-api` → `augint-ap`)**
- **Fixed**: Latest version handles this correctly
- **If still occurring**: Re-run `bootstrap-stage1.py`

**Missing dependencies errors**
- **Stage 1 requires no dependencies** - run before `poetry install`

### Stage 2 Issues

**"No pipelineconfig.toml files found"**
- **Cause**: SAM pipeline bootstrap wasn't run or failed
- **Solution**: Run `sam pipeline bootstrap --stage <project-name>-testing` first
- **Verify**: Check `.aws-sam/pipeline/pipelineconfig.toml` exists

**AWS credentials not configured**
- **Problem**: Shows `AWS_ACCOUNT_ID: Account` instead of actual ID
- **Solution**: Configure AWS CLI: `aws configure`
- **Verify**: Run `aws sts get-caller-identity`

**OIDC provider permission errors**
- **Problem**: `AccessDenied` when creating OIDC provider
- **Solution**: You need IAM admin permissions or ask an admin
- **Alternative**: Skip creation - pipeline will show clear error if needed

**Trust policy update fails**
- **Problem**: `AccessDenied` when updating IAM role
- **Solution**: Ensure you have permissions for the pipeline execution role
- **Note**: Role should have been created by SAM pipeline bootstrap

### General Issues

**SAM pipeline bootstrap hangs**
- **Expected**: This is an interactive command
- **Action**: Respond to prompts about CI/CD provider, repository, etc.
- **Cancel**: Use Ctrl+C if needed

**Path issues on Windows**
- **Solution**: Use Git Bash or PowerShell
- **Quote paths**: `poetry run pytest "tests/test with spaces.py"`

## 🏗️ What Gets Created

### AWS Resources (via SAM)
- Pipeline execution IAM role
- CloudFormation execution IAM role
- S3 artifacts bucket
- GitHub OIDC provider (if not exists)

### Local Files
- `.env` - Environment configuration
- `.aws-sam/` - SAM pipeline configuration
- Customized project files with your names

## 🧹 Cleanup

To remove AWS resources:
```bash
python bootstrap.py cleanup
```

This will delete:
- IAM roles created by SAM
- S3 artifacts bucket
- Related AWS resources

## 💡 Tips

- The two-stage approach is recommended for new users
- Stage 1 can be run immediately after cloning
- Stage 2 requires dependencies but automates AWS setup
- All bootstrap scripts are idempotent (safe to run multiple times)
- Check your `.env` file after each stage to ensure values are populated

## 📚 Next Steps

After bootstrap completes:
1. Review generated `README.md` and `CLAUDE.md`
2. Configure branch protection rules
3. Set up PyPI trusted publishing
4. Start developing your library!

For more details, see the main README.md file.

---

## 🎯 Final Step: Cleanup

After your project is fully set up and working:

1. **Delete bootstrap files** (no longer needed):
   ```bash
   rm bootstrap-stage1.py bootstrap-stage2.py BOOTSTRAP.md
   ```

2. **Commit the cleanup**:
   ```bash
   git add -A
   git commit -m "chore: remove bootstrap files after setup"
   git push
   ```

3. **Customize your README.md** with project-specific information

Your project is now ready for development! 🎉
