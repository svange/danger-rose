# Run Full Test Suite Including Slow Tests

Execute the complete test suite including slow AWS integration tests that are normally skipped.

## Usage

```bash
# Run all tests including slow/integration tests
poetry run pytest -m ""

# Run with coverage report
poetry run pytest -m "" --cov=src --cov-report=html

# Run specific test categories
poetry run pytest -m "slow"           # Only slow tests
poetry run pytest -m "not slow"       # Fast tests only (default)
poetry run pytest -m "integration"    # Integration tests
poetry run pytest -m "ci_only"        # CI-only tests

# Run with verbose output
poetry run pytest -m "" -vv

# Run tests in parallel
poetry run pytest -m "" -n auto
```

## Test Categories

### Default Tests (Fast)
- Unit tests
- Business logic tests
- No external dependencies
- Run in < 1 second each

### Slow Tests (@pytest.mark.slow)
- AWS integration tests
- Database operations
- External API calls
- Network operations

### CI Only Tests (@pytest.mark.ci_only)
- Tests requiring specific CI environment
- GitHub Actions integration
- Deployment verification

## Pre-test Setup

```bash
# Ensure AWS credentials are configured
aws sts get-caller-identity

# Set test environment variables
export AWS_DEFAULT_REGION=us-east-1
export TEST_S3_BUCKET=augint-library-test-bucket
export TEST_DYNAMODB_TABLE=augint-library-test-table

# Install all test dependencies
poetry install --with dev,test
```

## Troubleshooting Test Failures

### AWS Permission Issues
```bash
# Check IAM permissions
aws iam get-user
aws iam list-attached-user-policies --user-name $(aws iam get-user --query 'User.UserName' --output text)
```

### Flaky Tests
```bash
# Run flaky test multiple times
poetry run pytest -m "" --count=10 -x tests/test_flaky.py::test_function
```

### Debug Failing Tests
```bash
# Drop into debugger on failure
poetry run pytest -m "" --pdb

# Show local variables on failure
poetry run pytest -m "" -l

# Capture and show logs
poetry run pytest -m "" --log-cli-level=DEBUG
```

## Coverage Analysis

```bash
# Generate coverage report
poetry run pytest -m "" --cov=src --cov-report=term-missing

# Generate HTML coverage report
poetry run pytest -m "" --cov=src --cov-report=html
open htmlcov/index.html

# Check coverage requirements
poetry run pytest -m "" --cov=src --cov-fail-under=90
```
