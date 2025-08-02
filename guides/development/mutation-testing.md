# Mutation Testing Guide

## What is Mutation Testing?

Mutation testing is a method of software testing that involves modifying your code in small ways (mutations) and checking if your test suite detects these changes. It's a way to test your tests!

Unlike code coverage which only shows which lines are executed, mutation testing verifies that your tests actually detect bugs when they're introduced.

## How Mutation Testing Works

1. **Mutate**: The tool makes small changes to your code (mutations)
2. **Test**: Run your test suite against the mutated code
3. **Analyze**: If tests fail, the mutation is "killed" (good!). If tests pass, the mutation "survived" (bad!)

Common mutations include:
- Changing `>` to `>=` or `<`
- Replacing `+` with `-`
- Changing `True` to `False`
- Removing function calls
- Changing return values

## Using mutmut in augint-library

### Installation

mutmut is already included in the dev dependencies:
```bash
poetry install --with dev
```

### Basic Usage

Run mutation tests on the entire codebase:
```bash
make mutmut-run
```

**Warning**: This can take a long time! Press Ctrl+C to stop and save progress.

### Viewing Results

After running mutation tests:
```bash
make mutmut-results
```

This shows a summary like:
```
Killed 245 out of 267 mutants
Survived 22 mutants
```

### Detailed Investigation

To see a specific mutation that survived:
```bash
make mutmut-show ID=42
```

This shows exactly what change was made and where.

### HTML Reports

Generate a detailed HTML report:
```bash
make mutmut-report
```

Open `html/index.html` to browse mutations by file.

### Testing Changed Files Only

For faster feedback during development:
```bash
make mutmut-diff
```

This only tests files changed since branching from main.

## Understanding Results

### Mutation States

- **Killed**: Your tests detected the mutation ✅
- **Survived**: Your tests didn't detect the mutation ❌
- **Timeout**: Tests took too long (possible infinite loop)
- **Suspicious**: Tests were inconsistent

### Mutation Score

```
Mutation Score = (Killed Mutations / Total Mutations) × 100%
```

Aim for 80%+ mutation score for critical code paths.

## Fixing Survived Mutations

When a mutation survives, it usually means:

1. **Missing test case**: Add a test for that specific scenario
2. **Weak assertion**: Make your test assertions more specific
3. **Dead code**: The mutated code path is never used
4. **Equivalent mutation**: The mutation doesn't actually change behavior

### Example: Fixing a Survived Mutation

If this mutation survives:
```python
# Original
if x >= 10:
    return "high"

# Mutation (survived)
if x > 10:
    return "high"
```

Add a test case:
```python
def test_boundary_value():
    assert process_value(10) == "high"  # Tests the boundary
```

## Best Practices

### 1. Focus on High-Value Code

Don't aim for 100% mutation coverage everywhere. Focus on:
- Core business logic
- Security-critical code
- Complex algorithms
- Public APIs

### 2. Use Fast Tests

Configure mutmut to run only fast unit tests:
```toml
[tool.mutmut]
runner = "pytest -x -m 'not slow and not integration' -q"
```

### 3. Incremental Approach

Start with critical modules:
```bash
mutmut run --paths-to-mutate=src/augint_library/core.py
```

### 4. Handle Equivalent Mutations

Some mutations don't change behavior:
```python
# These are equivalent for the last iteration
for i in range(10):
    x = i

# vs
for i in range(10):
    x = i + 1  # On last iteration, x isn't used
```

Don't waste time on these.

## CI Integration

Mutation testing is scheduled weekly in CI due to its computational cost. See `.github/workflows/mutation-testing.yml` for configuration.

Manual trigger:
```bash
gh workflow run mutation-testing.yml
```

## Common Patterns

### Boundary Testing
Mutations often reveal missing boundary tests:
```python
# Mutation changes >= to >
# Add tests for the exact boundary value
```

### Exception Testing
Ensure exceptions are properly tested:
```python
# Mutation removes raise statement
# Add test that expects the specific exception
```

### Return Value Testing
Test all possible return values:
```python
# Mutation changes return True to return False
# Add tests for both true and false cases
```

## Performance Tips

1. **Parallel execution**: mutmut uses multiprocessing by default
2. **Cache results**: Results are cached in `.mutmut-cache`
3. **Exclude files**: Add to configuration if needed
4. **Quick mode**: Use `--paths-to-mutate` for specific files

## Troubleshooting

### Tests Pass Locally but Fail in Mutation

- Check for test order dependencies
- Look for shared state between tests
- Ensure proper test isolation

### Mutation Testing is Too Slow

- Reduce test scope in configuration
- Focus on specific modules
- Use `make mutmut-diff` during development

### Too Many Surviving Mutations

- Start with one module at a time
- Prioritize based on code criticality
- Some mutations may be false positives

## Further Reading

- [mutmut Documentation](https://mutmut.readthedocs.io/)
- [Mutation Testing Theory](https://en.wikipedia.org/wiki/Mutation_testing)
- [Test Quality Metrics](https://martinfowler.com/articles/testing-metrics.html)
