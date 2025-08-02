# Minigame Template

## Complete Minigame Structure

```python
"""Template minigame following Danger Rose patterns."""

import random
import time
import pygame

from src.scenes.base_scene import Scene
from src.entities.player import Player
from src.config.constants import (
    COLOR_WHITE, COLOR_BLACK, COLOR_GREEN, COLOR_RED,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    FONT_LARGE, FONT_SMALL,
    GAME_DURATION,
    SCENE_HUB_WORLD, SCENE_LEADERBOARD
)
from src.utils.attack_character import AnimatedCharacter

class TemplateMinigame(Scene):
    """Template for creating new minigames."""

    def __init__(self):
        """Initialize minigame components."""
        # Game state
        self.game_active = False
        self.game_over = False
        self.paused = False
        self.score = 0
        self.lives = 3
        self.time_remaining = GAME_DURATION

        # Timing
        self.start_time = None
        self.last_spawn_time = 0
        self.spawn_interval = 2.0  # seconds

        # Entities
        self.player = None
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()

        # Fonts
        self.font_large = pygame.font.Font(None, FONT_LARGE)
        self.font_small = pygame.font.Font(None, FONT_SMALL)

        # Background
        self.background_color = COLOR_BLACK

    def on_enter(self, previous_scene: str | None = None, data: dict | None = None):
        """Initialize when entering minigame."""
        self.scene_data = data or {}
        character = self.scene_data.get("selected_character", "danger")

        # Create player
        self.player = Player(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100,
            character
        )

        # Start game
        self.start_game()

    def start_game(self):
        """Start the minigame."""
        self.game_active = True
        self.game_over = False
        self.start_time = time.time()
        self.score = 0
        self.lives = 3

        # Clear all entities
        self.enemies.empty()
        self.collectibles.empty()
        self.effects.empty()

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.game_over:
                    return SCENE_HUB_WORLD
                else:
                    self.paused = not self.paused

            elif event.key == pygame.K_r and self.game_over:
                self.start_game()  # Restart

            elif event.key == pygame.K_RETURN and self.game_over:
                # Go to leaderboard with score
                return SCENE_LEADERBOARD

        # Pass events to player when game active
        if self.game_active and not self.paused and not self.game_over:
            self.player.handle_event(event)

        return None

    def update(self, dt: float) -> None:
        """Update minigame logic."""
        if not self.game_active or self.paused:
            return

        if self.game_over:
            return

        # Update timer
        current_time = time.time()
        elapsed = current_time - self.start_time
        self.time_remaining = max(0, GAME_DURATION - elapsed)

        # Check time limit
        if self.time_remaining <= 0:
            self.end_game()
            return

        # Update player
        self.player.update(dt, [])

        # Spawn enemies/collectibles
        self.spawn_objects(current_time)

        # Update entities
        self.enemies.update(dt)
        self.collectibles.update(dt)
        self.effects.update(dt)

        # Check collisions
        self.check_collisions()

        # Remove off-screen entities
        self.cleanup_entities()

    def spawn_objects(self, current_time: float):
        """Spawn enemies and collectibles."""
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.last_spawn_time = current_time

            # Spawn enemy
            if random.random() < 0.7:  # 70% chance
                enemy = self.create_enemy()
                self.enemies.add(enemy)

            # Spawn collectible
            if random.random() < 0.3:  # 30% chance
                collectible = self.create_collectible()
                self.collectibles.add(collectible)

    def create_enemy(self) -> pygame.sprite.Sprite:
        """Create enemy sprite."""
        enemy = pygame.sprite.Sprite()
        enemy.image = pygame.Surface((32, 32))
        enemy.image.fill(COLOR_RED)
        enemy.rect = enemy.image.get_rect()
        enemy.rect.x = random.randint(0, SCREEN_WIDTH - 32)
        enemy.rect.y = -32
        enemy.speed = random.randint(100, 200)
        return enemy

    def create_collectible(self) -> pygame.sprite.Sprite:
        """Create collectible sprite."""
        collectible = pygame.sprite.Sprite()
        collectible.image = pygame.Surface((24, 24))
        collectible.image.fill(COLOR_GREEN)
        collectible.rect = collectible.image.get_rect()
        collectible.rect.x = random.randint(0, SCREEN_WIDTH - 24)
        collectible.rect.y = -24
        collectible.speed = random.randint(50, 150)
        collectible.points = 10
        return collectible

    def check_collisions(self):
        """Check all collision interactions."""
        player_rect = self.player.rect

        # Player vs enemies
        hit_enemies = pygame.sprite.spritecollide(
            self.player, self.enemies, True
        )
        if hit_enemies:
            self.lives -= 1
            if self.lives <= 0:
                self.end_game()

        # Player vs collectibles
        collected = pygame.sprite.spritecollide(
            self.player, self.collectibles, True
        )
        for item in collected:
            self.score += item.points

    def cleanup_entities(self):
        """Remove off-screen entities."""
        for enemy in self.enemies:
            if enemy.rect.y > SCREEN_HEIGHT:
                enemy.kill()

        for collectible in self.collectibles:
            if collectible.rect.y > SCREEN_HEIGHT:
                collectible.kill()

    def end_game(self):
        """End the minigame."""
        self.game_over = True

    def draw(self, screen: pygame.Surface) -> None:
        """Draw minigame to screen."""
        # Clear screen
        screen.fill(self.background_color)

        if not self.game_active:
            return

        # Draw entities
        self.enemies.draw(screen)
        self.collectibles.draw(screen)
        self.effects.draw(screen)

        # Draw player
        self.player.draw(screen)

        # Draw UI
        self.draw_ui(screen)

        # Draw pause/game over overlays
        if self.paused:
            self.draw_pause_overlay(screen)
        elif self.game_over:
            self.draw_game_over_overlay(screen)

    def draw_ui(self, screen: pygame.Surface):
        """Draw UI elements."""
        # Score
        score_text = self.font_small.render(f"Score: {self.score}", True, COLOR_WHITE)
        screen.blit(score_text, (10, 10))

        # Lives
        lives_text = self.font_small.render(f"Lives: {self.lives}", True, COLOR_WHITE)
        screen.blit(lives_text, (10, 35))

        # Timer
        timer_text = self.font_small.render(f"Time: {self.time_remaining:.1f}", True, COLOR_WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

    def draw_pause_overlay(self, screen: pygame.Surface):
        """Draw pause menu."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLOR_BLACK)
        screen.blit(overlay, (0, 0))

        pause_text = self.font_large.render("PAUSED", True, COLOR_WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(pause_text, pause_rect)

    def draw_game_over_overlay(self, screen: pygame.Surface):
        """Draw game over screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLOR_BLACK)
        screen.blit(overlay, (0, 0))

        # Game over text
        game_over_text = self.font_large.render("GAME OVER", True, COLOR_WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        # Final score
        score_text = self.font_large.render(f"Final Score: {self.score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_text, score_rect)

        # Instructions
        restart_text = self.font_small.render("R - Restart    Enter - Leaderboard    Esc - Hub", True, COLOR_WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(restart_text, restart_rect)

    def on_exit(self) -> dict:
        """Return data when leaving scene."""
        return {
            "last_score": self.score,
            "games_played": self.scene_data.get("games_played", 0) + 1,
            "selected_character": self.scene_data.get("selected_character", "danger")
        }
```

## Minigame Registration

Add to SceneManager:
```python
# In scene_manager.py
self.scenes["template"] = TemplateMinigame()
```

## Testing Minigame

```bash
# Run directly for testing
SCENE=template make run

# Run specific tests
poetry run pytest tests/test_template_minigame.py
```
