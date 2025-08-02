# Scene Template

## Basic Scene Structure

```python
"""New game scene for Danger Rose."""

import pygame
from src.scenes.base_scene import Scene
from src.config.constants import (
    COLOR_WHITE,
    COLOR_BLACK,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FONT_LARGE
)

class NewScene(Scene):
    """Template for a new game scene."""

    def __init__(self):
        """Initialize scene components."""
        self.font = pygame.font.Font(None, FONT_LARGE)
        self.background_color = COLOR_BLACK

        # Scene-specific state
        self.initialized = False
        self.entities = pygame.sprite.Group()

    def on_enter(self, previous_scene: str | None = None, data: dict | None = None):
        """Initialize scene when entering."""
        self.previous_scene = previous_scene
        self.scene_data = data or {}

        # Get character from scene data
        self.character = self.scene_data.get("selected_character", "danger")

        # Initialize scene
        self.initialized = True

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "hub"  # Return to hub world
            elif event.key == pygame.K_SPACE:
                # Handle action
                pass

        return None

    def update(self, dt: float) -> None:
        """Update scene logic."""
        if not self.initialized:
            return

        # Update entities
        self.entities.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw scene to screen."""
        if not self.initialized:
            return

        # Clear screen
        screen.fill(self.background_color)

        # Draw entities
        self.entities.draw(screen)

        # Draw UI elements
        title_text = self.font.render("New Scene", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

    def on_exit(self) -> dict:
        """Cleanup when leaving scene."""
        return {
            "last_scene": "new_scene",
            "character": self.character
        }
```

## Menu Scene Template

```python
class MenuScene(Scene):
    """Template for menu-style scenes."""

    def __init__(self):
        self.options = ["Option 1", "Option 2", "Back"]
        self.selected = 0
        self.font = pygame.font.Font(None, FONT_LARGE)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = max(0, self.selected - 1)
            elif event.key == pygame.K_DOWN:
                self.selected = min(len(self.options) - 1, self.selected + 1)
            elif event.key == pygame.K_RETURN:
                selected_option = self.options[self.selected]
                if selected_option == "Back":
                    return "hub"
                # Handle other options

        return None
```

## Game Scene Template

```python
class GameScene(Scene):
    """Template for interactive game scenes."""

    def __init__(self):
        self.player = None
        self.obstacles = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.score = 0
        self.game_over = False

    def on_enter(self, previous_scene: str | None = None, data: dict | None = None):
        character = data.get("selected_character", "danger") if data else "danger"
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, character)

    def update(self, dt: float):
        if self.game_over:
            return

        self.player.update(dt, [])
        self.obstacles.update(dt)

        # Check collisions
        if pygame.sprite.spritecollide(self.player, self.obstacles, False):
            self.game_over = True
```
