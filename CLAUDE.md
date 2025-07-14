# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Danger-Rose is a family-friendly Pygame project featuring a cozy apartment hub world with three themed minigames: Ski Downhill, Pool Splash, and Vegas Dash. The project is currently in early development with basic Pygame setup in `src/main.py`.

## Development Commands

### Environment Setup
```bash
# Install dependencies using Poetry
poetry install

# Activate virtual environment (if not using Poetry shell)
poetry shell
```

### Running the Game
```bash
# Run the main game
poetry run python src/main.py
```

### Development Tools
```bash
# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src

# Run tests with HTML coverage report
poetry run pytest --cov=src --cov-report=html

# Format code with Black
poetry run black src/

# Lint code with Ruff
poetry run ruff check src/

# Fix linting issues
poetry run ruff check src/ --fix

# Run pre-commit hooks
poetry run pre-commit run --all-files
```

## Architecture

### Current Structure
- `src/main.py` - Entry point with basic Pygame initialization and game loop
- `src/__init__.py` - Package initialization
- Poetry configuration uses `package-mode = false` for application-style project

### Planned Architecture (from README)
The project will expand to include:
- **Scene Management**: Hub world and minigame scenes
- **Game Scenes**: `scenes/hub.py`, `scenes/ski.py`, `scenes/pool.py`, `scenes/vegas.py`
- **Utilities**: `utils/sprite_loader.py`, `utils/ui.py`
- **Assets**: Organized in `assets/images/` and `assets/audio/`

### Key Technical Details
- Uses `pygame-ce` (Community Edition) instead of regular pygame
- Screen resolution: 1920x1080 (defined in `src/main.py`)
- Poetry virtual environment configured to install in-project (`.venv/`)
- Python 3.12+ required

### Asset Management
- **Asset Paths**: Use `src/utils/asset_paths.py` for consistent asset path resolution
- **Sprite Loader**: `src/utils/sprite_loader.py` handles image loading with fallback placeholders
- **Character Animations**: `src/utils/animated_character.py` manages sprite sheet animations

**Common Asset Functions:**
```python
from src.utils.asset_paths import (
    get_living_room_bg,      # Background image
    get_danger_sprite,       # Danger character sprite sheet
    get_rose_sprite,         # Rose character sprite sheet
    get_character_sprite_path,  # Generic character sprite
    get_tileset_path,        # Tileset images
    get_icon_path,           # UI icons
    get_music_path,          # Background music
    get_sfx_path             # Sound effects
)
```

## Development Dependencies
- `pytest` - Testing framework
- `pytest-html` - HTML test reports
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `ruff` - Fast Python linter
- `pre-commit` - Git hooks
- `augint-github` - GitHub integration tool