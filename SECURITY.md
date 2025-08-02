# Security Policy

## 🛡️ Reporting Security Vulnerabilities

The Danger Rose team takes security seriously. We appreciate your efforts to responsibly disclose your findings.

### Where to Report

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: svange@github.com

### What to Include

Please include the following information:
- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Response Timeline

- We will acknowledge receipt of your report within 48 hours
- We will provide a more detailed response within 7 days
- We will work on fixes and coordinate disclosure with you

## 🎮 Security Considerations for a Game Project

While Danger Rose is a family-friendly game, we still maintain security best practices:

### Data Storage
- Game saves are stored locally only
- No personal data is collected or transmitted
- High scores are stored locally

### Dependencies
- We regularly update dependencies to patch known vulnerabilities
- Run `poetry update` to get the latest secure versions

### Code Security
- No hardcoded secrets or API keys
- All user input is validated
- File paths are sanitized

## 📋 Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.10.x  | :white_check_mark: |
| < 1.10  | :x:                |

## 🔒 Security Best Practices for Contributors

When contributing to Danger Rose, please:

1. **Never commit secrets**
   - API keys, tokens, passwords must use environment variables
   - Check your commits before pushing

2. **Validate input**
   - Always validate user input in minigames
   - Sanitize file paths

3. **Update dependencies**
   - Keep dependencies up to date
   - Check for security advisories

4. **Safe file operations**
   - Use pathlib for file operations
   - Validate file paths are within expected directories

## 🚨 Known Security Considerations

### Local File Access
The game reads and writes save files locally. These operations are restricted to the game's data directory.

### Asset Loading
The game loads images and sounds from the assets directory. All paths are validated before loading.

### Network
Currently, Danger Rose does not make any network requests. If this changes in the future, we will update our security policy accordingly.

## 👨‍👩‍👧‍👦 For Parents

Danger Rose is designed with child safety in mind:
- No online features or chat
- No data collection
- No in-app purchases
- No external links

Your children can safely play and even modify the game code without security concerns.

## 📝 Security Checklist for Releases

Before each release, we ensure:
- [ ] No secrets in code or commit history
- [ ] Dependencies are up to date
- [ ] Security scanning passes
- [ ] No vulnerable dependencies
- [ ] File operations are properly bounded

Thank you for helping keep Danger Rose secure for all our players!