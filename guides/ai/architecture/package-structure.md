# Package Structure Guide

## Directory Layout

```
src/
├── main.py              # Entry point, pygame init, main loop
├── scene_manager.py     # Central scene coordinator
├── config/
│   └── constants.py     # All game constants (colors, sizes, speeds)
├── scenes/              # Game screens and levels
│   ├── __init__.py
│   ├── title_screen.py
│   ├── character_select.py
│   ├── hub_world.py
│   ├── ski_game.py
│   ├── pool_game.py
│   └── vegas_game.py
├── entities/            # Game objects with physics/rendering
│   ├── __init__.py
│   ├── player.py
│   ├── doors.py
│   ├── furniture.py
│   └── obstacles.py
├── managers/            # Singleton services
│   ├── __init__.py
│   ├── sound_manager.py
│   ├── save_manager.py
│   └── high_score_manager.py
├── utils/               # Helper functions and utilities
│   ├── __init__.py
│   ├── sprite_loader.py
│   ├── asset_paths.py
│   ├── collision.py
│   └── math_utils.py
└── effects/             # Visual effects and particles
    ├── __init__.py
    ├── particles.py
    └── animations.py
```

## Module Responsibilities

### Core Game Loop (`main.py`)
```python
# Entry point responsibilities:
- pygame.init() and display setup
- Create SceneManager instance
- Main game loop with FPS control
- Global event handling (quit, fullscreen)
- Error handling and cleanup
```

### Scene Management (`scene_manager.py`)
```python
# Centralized scene control:
- Scene registration and storage
- Scene transition orchestration
- Global game state persistence
- Pause system implementation
- Debug scene overrides
```

### Configuration (`config/constants.py`)
```python
# Single source of truth for:
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
PLAYER_SPEED = 300
COLORS = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "PLACEHOLDER": (255, 0, 255)  # Magenta
}
```

### Game Scenes (`scenes/`)
```python
# Each scene implements Scene interface:
class HubWorld(Scene):
    def __init__(self):
        self.entities = pygame.sprite.Group()
        self.doors = {}
        self.furniture = {}

    def handle_event(self, event) -> str | None
    def update(self, dt: float) -> None
    def draw(self, screen) -> None
```

### Entities (`entities/`)
```python
# Game objects with standard interface:
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = pygame.Vector2(0, 0)

    def update(self, dt: float)
    def draw(self, screen)
```

### Managers (`managers/`)
```python
# Singleton services:
class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

## Import Patterns

### Standard Imports
```python
# Always at top of file
import pygame
import sys
from typing import Optional, Dict, List
from abc import ABC, abstractmethod

# Project imports grouped
from src.config.constants import SCREEN_WIDTH, COLORS
from src.entities.player import Player
from src.utils.sprite_loader import load_sprite
```

### Avoiding Circular Imports
```python
# Use TYPE_CHECKING for type hints
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.scene_manager import SceneManager

# Import inside functions when needed
def transition_to_scene(scene_name: str):
    from src.scene_manager import SceneManager
    SceneManager().transition_to(scene_name)
```

## Configuration Hierarchy

### Global Constants (`config/constants.py`)
```python
# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Physics
GRAVITY = 980  # pixels/second²
PLAYER_SPEED = 300  # pixels/second

# Colors (RGB tuples)
COLORS = {
    "BACKGROUND": (50, 50, 80),
    "UI_TEXT": (255, 255, 255)
}
```

### Scene-Specific Config
```python
# In scene files
class SkiGame(Scene):
    # Scene constants
    MOUNTAIN_SPEED = 400
    OBSTACLE_SPAWN_RATE = 2.0
    COLLECTIBLE_POINTS = 10
```

## Asset Path Management

### Centralized Paths (`utils/asset_paths.py`)
```python
from pathlib import Path

ASSETS_DIR = Path("assets")
IMAGES_DIR = ASSETS_DIR / "images"
AUDIO_DIR = ASSETS_DIR / "audio"

def get_character_sprite(character: str, animation: str) -> Path:
    return IMAGES_DIR / "characters" / f"{character}_{animation}.png"

def get_background(scene: str) -> Path:
    return IMAGES_DIR / "backgrounds" / f"{scene}_bg.png"
```

## Testing Structure

### Test Organization
```python
tests/
├── unit/                # Fast, isolated tests
│   ├── test_entities/
│   ├── test_utils/
│   └── test_managers/
├── integration/         # Multi-component tests
│   ├── test_scene_flow.py
│   └── test_save_system.py
└── conftest.py         # Shared fixtures
```

### Test Utilities
```python
# tests/conftest.py
@pytest.fixture
def mock_pygame():
    """Mock pygame for headless testing"""
    # Setup pygame mocks

@pytest.fixture
def sample_scene():
    """Create test scene instance"""
    return HubWorld()
```
