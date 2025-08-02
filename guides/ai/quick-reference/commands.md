# Game Development Commands - Quick Reference

## Essential Make Commands

```bash
# Core Development
make run                  # Run game normally
make debug               # Run with debug info (FPS, collision boxes)
make test                # Run all tests
make test-fast           # Quick unit tests only
make coverage            # Generate coverage report

# Code Quality
make lint                # Check code style
make format              # Auto-format code
make check               # Run all quality checks
make fix                 # Fix common issues

# Building
make build               # Build executable for current platform
make build-all           # Build for all platforms
make clean               # Clean build artifacts
```

## Scene-Specific Commands

```bash
# Direct scene access
make run-ski             # Start at ski minigame
make run-pool            # Start at pool minigame  
make run-vegas           # Start at Vegas minigame
make run-hub             # Start at hub world

# Kid-friendly mode
make kids                # Simplified errors, bigger text
```

## Development Workflow

```bash
# Standard development cycle
make format              # Format code first
make test-fast           # Quick test cycle
make run                 # Test gameplay
make check               # Full validation before commit

# Performance profiling
make profile             # Run with profiling enabled
make memory-profile      # Check memory usage
```

## Poetry Commands

```bash
poetry install           # Install dependencies
poetry update            # Update dependencies
poetry run python src/main.py  # Run without make
poetry shell             # Enter virtual environment
```

## Environment Variables

```bash
# Debug options
DEBUG=true make run      # Enable all debug features
FPS_DEBUG=true make run  # Show FPS counter only
COLLISION_DEBUG=true make run  # Show collision boxes

# Scene overrides
START_SCENE=ski make run # Start at specific scene
SKIP_TITLE=true make run # Skip title screen
```

## Custom AI Commands (in game context)

```bash
# Sprite operations
/sprite-cut path.png 256 341  # Extract frames from sheet
/validate-sprites --fix       # Check and fix sprites
/generate-placeholder npc 128 128  # Create placeholder

# Scene creation
/create-scene bonus_room hub  # New hub room
/create-scene sky_race minigame  # New minigame

# Testing helpers
/test-minigame ski           # Run minigame tests
/balance-game pool easy      # Adjust difficulty