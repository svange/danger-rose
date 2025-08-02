# Docker Development Guide

This guide covers using Docker for development of the augint-library project, including special support for Claude Code on Windows.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Workflows](#workflows)
- [Claude Code Integration](#claude-code-integration)
- [PyCharm Integration](#pycharm-integration)
- [Service Dependencies](#service-dependencies)
- [Troubleshooting](#troubleshooting)

## Overview

The Docker setup provides:
- **Consistent development environment** across all platforms
- **Isolated testing** with service dependencies
- **Claude Code support** on Windows without WSL
- **Zero-setup onboarding** for new developers
- **CI/CD compatibility** for reliable builds

## Quick Start

### Windows Users

1. **Using PowerShell:**
   ```powershell
   # First time setup
   .\scripts\docker-dev.ps1 -Build

   # Daily use
   .\scripts\docker-dev.ps1
   ```

2. **Using Make:**
   ```bash
   # Build and start
   make docker-build
   make docker-dev
   ```

### macOS/Linux Users

```bash
# Build images
make docker-build

# Start development environment
make docker-dev
```

### Claude Code Users

With the Docker integration, Claude Code commands automatically run inside the container:

```bash
# These commands run in the container automatically
poetry install
make test
python -m augint_library.cli
```

## Architecture

### Multi-Stage Dockerfile

```
base          → Python 3.9 slim base image
  ↓
builder       → Adds build tools, installs Poetry
  ↓
development   → Adds dev tools, creates user, full environment
  ↓
test-runner   → Optimized for running tests
  ↓
production    → Minimal runtime image
```

### Container Services

1. **dev** - Main development container
2. **test** - Test runner (read-only source)
3. **security** - Security scanning
4. **docs** - Documentation server
5. **jupyter** - Jupyter notebook server

### Volume Strategy

- **Source code**: Bind mounted for live editing
- **Poetry cache**: Named volume for performance
- **Virtual environment**: Named volume for isolation

## Workflows

### Daily Development

```bash
# Start environment
make docker-dev

# Inside container
poetry install          # Install dependencies
make test              # Run tests
make lint              # Run linting
make format            # Format code

# From another terminal
make docker-shell      # Open another shell
```

### Running Tests

```bash
# Fast unit tests
make docker-test

# Integration tests with services
make docker-test-integration

# Security scans
make docker-security
```

### Documentation

```bash
# Start documentation server
make docker-docs
# Visit http://localhost:8000
```

### Jupyter Notebooks

```bash
# Start Jupyter
docker-compose up -d jupyter
# Visit http://localhost:8888
```

## Claude Code Integration

### How It Works

1. **Automatic Container Start**: The `.claude/settings.json` hooks ensure the container is running
2. **Command Routing**: Non-Docker commands are automatically executed inside the container
3. **File Synchronization**: Files edited locally are immediately available in the container

### Configuration

The integration is configured in `.claude/settings.json`:
- PreCommand hook starts the container
- PreToolUse hook routes commands through docker-exec
- Permissions allow Docker commands

### Usage

Simply use Claude Code normally - all Python/Poetry commands run in Docker:

```bash
# These automatically run in Docker
poetry add requests
pytest tests/
make test
```

## PyCharm Integration

### Option 1: Docker Interpreter

1. **Settings → Project → Python Interpreter**
2. **Add Interpreter → Docker Compose**
3. **Service**: `dev`
4. **Python path**: `/usr/local/bin/python`

### Option 2: Traditional Setup

Continue using Windows `.venv` - both approaches work:

```powershell
# Windows native development
poetry install
poetry run pytest
```

## Service Dependencies

### PostgreSQL
- **Container**: `postgres`
- **Connection**: `postgresql://testuser:testpass@postgres:5432/testdb`
- **Health check**: Waits for database readiness

### Redis
- **Container**: `redis`
- **Connection**: `redis://redis:6379/0`
- **Persistence**: Append-only file enabled

### LocalStack (AWS)
- **Container**: `localstack`
- **Endpoint**: `http://localstack:4566`
- **Services**: S3, DynamoDB, Lambda, SQS, SNS

### Using Services in Tests

```python
import os
import pytest

@pytest.mark.integration
def test_with_postgres():
    db_url = os.environ.get('DATABASE_URL')
    # Your test code here

@pytest.mark.integration  
def test_with_redis():
    redis_url = os.environ.get('REDIS_URL')
    # Your test code here
```

## Troubleshooting

### Docker Desktop Not Starting (Windows)

```powershell
# Check if virtualization is enabled
Get-ComputerInfo -property "HyperV*"

# Start Docker manually
& "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

### Container Won't Start

```bash
# Check logs
docker-compose logs dev

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d dev
```

### Permission Errors

```bash
# Fix ownership issues
docker-compose exec dev chown -R developer:developer /workspace
```

### Slow Performance (Windows)

1. **Use named volumes** instead of bind mounts for better I/O
2. **Enable WSL2 backend** in Docker Desktop settings
3. **Allocate more resources** in Docker Desktop settings

### Port Conflicts

```bash
# Check what's using a port
netstat -an | findstr :8000

# Use different ports
DOCS_PORT=8080 docker-compose up docs
```

### Out of Space

```bash
# Clean up Docker resources
make docker-clean

# More aggressive cleanup
docker system prune -a --volumes
```

### Poetry Lock Issues

```bash
# Inside container
rm poetry.lock
poetry lock
poetry install
```

## Advanced Usage

### Custom Environment Variables

Create `.env` file (git-ignored):
```env
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
CUSTOM_VAR=value
```

### Running Specific Python Version

Modify `Dockerfile`:
```dockerfile
FROM python:3.10-slim as base
```

### Adding System Dependencies

Edit the development stage in `Dockerfile`:
```dockerfile
RUN apt-get update && apt-get install -y \
    postgresql-client \
    redis-tools \
    your-package-here
```

### Debugging in Container

```bash
# Install debugger
docker-compose exec dev pip install ipdb

# Use in code
import ipdb; ipdb.set_trace()
```

## Best Practices

1. **Commit Dockerfile changes** - Keep the environment reproducible
2. **Use named volumes** - Better performance than bind mounts
3. **Clean regularly** - Run `make docker-clean` weekly
4. **Update base images** - Pull latest security updates monthly
5. **Document dependencies** - Add comments for unusual packages

## Platform-Specific Notes

### Windows
- Docker Desktop required (WSL2 backend recommended)
- Use PowerShell scripts for best experience
- File watchers may need polling mode

### macOS
- Docker Desktop required
- File sharing permissions may need configuration
- Consider increasing Docker resources

### Linux
- Native Docker gives best performance
- Add user to docker group: `sudo usermod -aG docker $USER`
- No Desktop application needed

## Conclusion

The Docker setup provides a robust, consistent development environment that works seamlessly with Claude Code, PyCharm, and CI/CD pipelines. It eliminates "works on my machine" issues and makes onboarding new developers trivial.
