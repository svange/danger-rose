# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Danger-Rose is a family-friendly Pygame project featuring a cozy apartment hub world with three themed minigames: Ski Downhill, Pool Splash, and Vegas Dash. The project is currently in early development with title screen and character selection implemented.

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

### Testing
```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src

# Run tests with HTML coverage report
poetry run pytest --cov=src --cov-report=html

# Run a specific test file
poetry run pytest tests/test_sprite_layout.py

# Run tests with verbose output
poetry run pytest -v
```

### Code Quality
```bash
# Format code with Black
poetry run black src/ tests/

# Lint code with Ruff
poetry run ruff check src/ tests/

# Fix linting issues automatically
poetry run ruff check src/ tests/ --fix

# Run pre-commit hooks on all files
poetry run pre-commit run --all-files
```

## Architecture

### Core Systems
- **Scene Management**: `SceneManager` in `src/scene_manager.py` handles scene transitions and game state
- **Title Screen**: `TitleScreen` in `src/scenes/title_screen.py` implements character selection with attack animations
- **Sprite System**: `AttackCharacter` in `src/utils/attack_character.py` manages sprite sheet animations
- **Asset Loading**: `SpriteLoader` in `src/utils/sprite_loader.py` provides fallback placeholders for missing assets

### Game Flow
1. `main.py` initializes Pygame and creates the `SceneManager`
2. `SceneManager` starts with the `TitleScreen` scene
3. Player selects character (Danger or Rose) using arrow keys and Space
4. Character selection stored in `scene_manager.game_data`
5. Future: Transition to hub world scene

### Asset Management
- **Asset Paths**: Use `src/utils/asset_paths.py` for consistent asset path resolution
- **Sprite Specifications**: 128x128 base sprite size with sprite sheets for animations
- **Fallback System**: Missing assets automatically replaced with colored placeholders

**Key Asset Functions:**
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

### Animation System
The `AttackCharacter` class handles sprite animations with:
- Attack animation playback
- Frame timing control
- Automatic idle state return
- Sprite sheet cutting based on frame dimensions

## Testing Approach
- **Test Structure**: Tests in `tests/` directory mirror source structure
- **Fixtures**: `conftest.py` provides Pygame initialization for all tests
- **Visual Tests**: Several tests generate visual outputs for sprite validation

## Key Technical Details
- **Pygame Version**: Uses `pygame-ce` (Community Edition) for better compatibility
- **Screen Resolution**: 1920x1080 fullscreen-ready
- **Frame Rate**: 60 FPS target
- **Python Version**: 3.12+ required
- **Package Management**: Poetry with `package-mode = false` for application deployment