# Update and Test Dependency Changes

Safely update dependencies and test compatibility across the library and its consumers.

## Usage

```bash
# Check for outdated dependencies
poetry show --outdated

# Update all dependencies (within version constraints)
poetry update

# Update specific dependency
poetry update requests

# Update to latest (may break constraints)
poetry add requests@latest

# Update and test
poetry update && poetry run pytest

# Lock dependencies after update
poetry lock
```

## Dependency Update Workflow

### 1. Check Security Vulnerabilities First
```bash
# Run security checks
poetry run safety check
poetry run pip-audit

# If vulnerabilities found, update immediately
poetry add package-with-vulnerability@latest
```

### 2. Test Compatibility
```bash
# Create test environment
python -m venv update-test
source update-test/bin/activate

# Install updated dependencies
poetry install

# Run full test suite
poetry run pytest -m ""

# Test downstream compatibility
pip install -e .
python -c "import augint_library; augint_library.test_function()"
```

### 3. Update Lock File
```bash
# Regenerate lock file
poetry lock --no-update

# Verify lock file
poetry check
```

## Semantic Versioning Impact

### Patch Updates (1.0.0 → 1.0.1)
- Security fixes
- Bug fixes in dependencies
- No API changes

### Minor Updates (1.0.0 → 1.1.0)
- New features in dependencies
- Backward compatible changes
- May require code updates to use new features

### Major Updates (1.0.0 → 2.0.0)
- Breaking changes in dependencies
- Requires code migration
- Update with caution

## Testing Downstream Impact

```bash
# Test with augint-api
cd ../augint-api
poetry remove augint-library
poetry add ../augint-library
poetry run pytest

# Test with other consumers
for project in ../*/pyproject.toml; do
    if grep -q "augint-library" "$project"; then
        echo "Testing $(dirname $project)..."
        cd $(dirname $project)
        poetry update augint-library
        poetry run pytest
    fi
done
```

## Dependabot Integration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    assignees:
      - "your-username"
    labels:
      - "dependencies"
    open-pull-requests-limit: 10
    allow:
      - dependency-type: "all"
```

## Rollback Procedures

```bash
# If update causes issues, rollback
git checkout poetry.lock
poetry install

# Or revert to specific version
poetry add problematic-package@1.2.3
```

## Best Practices

1. **Update regularly**: Weekly for patch/minor updates
2. **Test thoroughly**: Run full test suite including slow tests
3. **Update in dev first**: Test in development before production
4. **Document breaking changes**: Update CHANGELOG.md
5. **Coordinate major updates**: Notify downstream consumers
