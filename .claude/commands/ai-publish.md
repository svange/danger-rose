# Verify Library Ready for PyPI Publishing

Check that the library meets all requirements for publishing to PyPI, including metadata, version, and package integrity.

## Usage

```bash
# Build the package
poetry build

# Check package contents
tar -tzf dist/*.tar.gz | head -20
unzip -l dist/*.whl | head -20

# Validate package metadata
twine check dist/*

# Test installation in clean environment
python -m venv test-env
source test-env/bin/activate  # or test-env\Scripts\activate on Windows
pip install dist/*.whl
python -c "import augint_library; print(augint_library.__version__)"
deactivate
rm -rf test-env

# Dry run upload to TestPyPI
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish -r testpypi --dry-run
```

## Pre-publish Checklist

### 1. Version Management
```bash
# Check current version
poetry version

# Bump version (automated by semantic-release in CI)
poetry version patch  # 1.0.0 -> 1.0.1
poetry version minor  # 1.0.0 -> 1.1.0
poetry version major  # 1.0.0 -> 2.0.0
```

### 2. Documentation
- [ ] README.md is complete and accurate
- [ ] CHANGELOG.md is up to date
- [ ] API documentation is generated
- [ ] Examples are working

### 3. Package Metadata
```toml
# pyproject.toml should include:
[tool.poetry]
name = "augint-library"
version = "1.0.0"
description = "Your description"
authors = ["Your Name <email@example.com>"]
license = "AGPL-3.0"
readme = "README.md"
homepage = "https://github.com/svange/augint-library"
repository = "https://github.com/svange/augint-library"
keywords = ["augint", "library", "aws"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Affero General Public License v3",
    "Programming Language :: Python :: 3.9",
]
```

### 4. Dependencies
```bash
# Check for security vulnerabilities
poetry run safety check

# Audit dependencies
poetry run pip-audit

# Check for outdated packages
poetry show --outdated
```

### 5. Test Coverage
```bash
# Ensure tests pass with coverage
poetry run pytest --cov=src --cov-fail-under=90
```

## Manual Publishing (if needed)

```bash
# Set PyPI token (get from https://pypi.org/manage/account/)
poetry config pypi-token.pypi <your-token>

# Publish to PyPI
poetry publish

# Or use twine directly
twine upload dist/*
```

## Post-publish Verification

```bash
# Wait a few minutes for PyPI to update, then:
pip install augint-library==$VERSION

# Test import
python -c "import augint_library; print(augint_library.__version__)"

# Check PyPI page
open https://pypi.org/project/augint-library/
```

## Troubleshooting

### Package Name Already Taken
- Ensure you've reserved the name on PyPI
- Check both pypi.org and test.pypi.org

### Authentication Issues
- Use API tokens, not username/password
- Ensure token has upload permissions

### Missing Files in Package
```bash
# Check MANIFEST.in or use poetry includes
[tool.poetry]
include = ["LICENSE", "README.md", "CHANGELOG.md"]
```
