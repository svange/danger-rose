Run tests across multiple Python versions: $ARGUMENTS

Steps:
1. Set up test matrix with tox
2. Run tests for Python 3.8, 3.9, 3.10, 3.11, 3.12
3. Generate combined coverage report
4. Check for version-specific issues

```bash
# Run all environments
tox

# Run specific version
tox -e py39

# Run with coverage
tox -e py39-coverage

# Recreate environments
tox -r
```

Report any version-specific failures or deprecation warnings.
