# Debug Click CLI Interface Issues

Troubleshoot and debug Click CLI commands in the augint-library.

## Usage

```bash
# Test CLI entry point
poetry run augint-library --help

# Debug specific command
poetry run augint-library --debug greet --name World

# Test with environment variables
DEBUG=true poetry run augint-library greet

# Run with Python debugger
poetry run python -m pdb -m augint_library.cli greet

# Test installed CLI
pip install -e .
augint-library --version
```

## Common CLI Issues

### 1. Entry Point Not Found
```bash
# Check pyproject.toml
[tool.poetry.scripts]
augint-library = "augint_library.cli:main"

# Reinstall in development mode
poetry install
```

### 2. Click Context Issues
```python
# Debug context in CLI
import click

@click.command()
@click.pass_context
def debug_context(ctx):
    """Debug Click context."""
    click.echo(f"Context: {ctx}")
    click.echo(f"Parent: {ctx.parent}")
    click.echo(f"Info: {ctx.info_name}")

    # Add breakpoint for debugging
    breakpoint()
```

### 3. Testing CLI Commands
```python
# tests/test_cli.py
from click.testing import CliRunner
from augint_library.cli import main

def test_greet_command():
    runner = CliRunner()
    result = runner.invoke(main, ['greet', '--name', 'World'])
    assert result.exit_code == 0
    assert 'Hello, World!' in result.output

def test_debug_mode():
    runner = CliRunner()
    result = runner.invoke(main, ['--debug', 'greet'],
                          catch_exceptions=False)
    # Debug output should be visible
```

### 4. CLI Configuration
```python
# Add debug logging to CLI
import logging
import click

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    """Augint Library CLI."""
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug

    if debug:
        logging.basicConfig(level=logging.DEBUG)
        click.echo('Debug mode enabled')
```

## Advanced Debugging

### Trace CLI Execution
```bash
# Use Python trace module
poetry run python -m trace -t -m augint_library.cli greet

# Profile CLI performance
poetry run python -m cProfile -m augint_library.cli greet
```

### Environment Debugging
```python
# Add environment info to CLI
@click.command()
def env_info():
    """Show environment information."""
    import sys
    import os

    click.echo(f"Python: {sys.version}")
    click.echo(f"Platform: {sys.platform}")
    click.echo(f"CWD: {os.getcwd()}")
    click.echo(f"PATH: {os.environ.get('PATH', 'Not set')}")
```

### Mock External Dependencies
```python
# Test CLI without AWS calls
from unittest.mock import patch

def test_cli_with_mock():
    runner = CliRunner()

    with patch('boto3.client') as mock_client:
        mock_client.return_value.get_secret_value.return_value = {
            'SecretString': '{"key": "value"}'
        }

        result = runner.invoke(main, ['process'])
        assert result.exit_code == 0
```

## CLI Best Practices

1. **Always provide --help text**
2. **Use click.echo() not print()**
3. **Handle exceptions gracefully**
4. **Provide --debug flag**
5. **Return proper exit codes**
6. **Test with CliRunner**
