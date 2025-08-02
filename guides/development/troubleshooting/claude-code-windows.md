# Claude Code on Windows

## Windows-Specific Setup

### Required Environment Variables
```powershell
# Set these environment variables for optimal Claude Code experience on Windows
$env:CLAUDE_CODE_GIT_BASH_PATH = "C:\Program Files\Git\bin\bash.exe"
$env:CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR = 1
```

### Git Bash Integration
Claude Code works best with Git Bash on Windows. Make sure Git for Windows is installed and the path above points to your Git Bash installation.

### Common Issues

#### Poetry Commands Failing in Claude Code
**Symptom**: `poetry run` commands fail or timeout in Claude Code
**Solution**: Use the Makefile commands instead:
```bash
# Use these instead of poetry run commands
make test          # Instead of poetry run pytest
make lint          # Instead of poetry run ruff
make format        # Instead of poetry run black
```

#### Path Issues
**Symptom**: Commands can't find executables
**Solution**: Ensure Git Bash is in your system PATH and restart Claude Code

### Recommended Tools
- Git for Windows (includes Git Bash)
- Windows Terminal or PowerShell 7+
- WSL2 (optional, for Linux-like environment)

For more detailed Windows setup instructions, see the main [Bootstrap Guide](../../setup/bootstrap.md).
