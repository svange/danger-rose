# Character Template

## Player Character Template

```python
"""Template for player characters in Danger Rose."""

import pygame
from src.config.constants import (
    PLAYER_SPEED,
    SPRITE_DISPLAY_SIZE,
    COLOR_WHITE
)
from src.utils.attack_character import AnimatedCharacter

class PlayerCharacter:
    """Template for player character with movement and animation."""
    
    def __init__(self, x: float, y: float, character_name: str):
        """Initialize player character.
        
        Args:
            x: Initial x position
            y: Initial y position  
            character_name: Character name (danger, rose, dad)
        """
        # Position and movement
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        
        # Movement state
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.facing_right = True
        
        # Character properties
        self.character_name = character_name
        self.health = 100
        self.max_health = 100
        self.lives = 3
        self.invulnerable = False
        self.invulnerable_time = 0.0
        
        # Animation system
        self.sprite = AnimatedCharacter(
            character_name.lower(),
            "hub",  # Default scene
            scale=(SPRITE_DISPLAY_SIZE, SPRITE_DISPLAY_SIZE)
        )
        
        # Collision rectangle
        self.rect = pygame.Rect(
            self.x - SPRITE_DISPLAY_SIZE // 2,
            self.y - SPRITE_DISPLAY_SIZE // 2,
            SPRITE_DISPLAY_SIZE,
            SPRITE_DISPLAY_SIZE
        )
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.move_left = True
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.move_right = True
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.move_up = True
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.move_down = True
            elif event.key == pygame.K_SPACE:
                self.attack()
                
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.move_left = False
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.move_right = False
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.move_up = False
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.move_down = False
                
    def update(self, dt: float, boundaries: list = None) -> None:
        """Update character physics and animation."""
        boundaries = boundaries or []
        
        # Update invulnerability
        if self.invulnerable:
            self.invulnerable_time -= dt
            if self.invulnerable_time <= 0:
                self.invulnerable = False
                
        # Calculate movement
        target_vx = 0.0
        target_vy = 0.0
        
        if self.move_left:
            target_vx -= PLAYER_SPEED
        if self.move_right:
            target_vx += PLAYER_SPEED
        if self.move_up:
            target_vy -= PLAYER_SPEED
        if self.move_down:
            target_vy += PLAYER_SPEED
        
        # Normalize diagonal movement
        if target_vx != 0 and target_vy != 0:
            diagonal_factor = 0.707  # 1/sqrt(2)
            target_vx *= diagonal_factor
            target_vy *= diagonal_factor
            
        self.vx = target_vx
        self.vy = target_vy
        
        # Update position with collision
        self.move_with_collision(dt, boundaries)
        
        # Update facing direction
        if self.vx > 0:
            self.facing_right = True
        elif self.vx < 0:
            self.facing_right = False
            
        # Update animation
        self.update_animation()
        
    def move_with_collision(self, dt: float, boundaries: list):
        """Move with collision detection."""
        old_x, old_y = self.x, self.y
        
        # Try full movement
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.update_rect()
        
        # Check collision
        if self.check_collision(boundaries):
            # Try horizontal only
            self.x = old_x + self.vx * dt
            self.y = old_y
            self.update_rect()
            
            if self.check_collision(boundaries):
                # Try vertical only
                self.x = old_x
                self.y = old_y + self.vy * dt
                self.update_rect()
                
                if self.check_collision(boundaries):
                    # Can't move, stay in place
                    self.x, self.y = old_x, old_y
                    self.update_rect()
                    
    def check_collision(self, boundaries: list) -> bool:
        """Check collision with boundaries."""
        for boundary in boundaries:
            if self.rect.colliderect(boundary):
                return True
        return False
        
    def update_rect(self):
        """Update collision rectangle."""
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        
    def update_animation(self):
        """Update character animation based on state."""
        if abs(self.vx) > 10 or abs(self.vy) > 10:
            self.sprite.set_animation("walk", loop=True)
        else:
            self.sprite.set_animation("idle", loop=True)
            
        self.sprite.update()
        
    def attack(self):
        """Perform attack animation."""
        self.sprite.set_animation("attack", loop=False)
        
    def take_damage(self, damage: int):
        """Take damage if not invulnerable."""
        if self.invulnerable:
            return
            
        self.health -= damage
        self.invulnerable = True
        self.invulnerable_time = 1.0  # 1 second invulnerability
        
        if self.health <= 0:
            self.lose_life()
            
    def lose_life(self):
        """Lose a life and reset health."""
        self.lives -= 1
        self.health = self.max_health
        self.sprite.set_animation("hurt", loop=False)
        
    def heal(self, amount: int):
        """Heal character."""
        self.health = min(self.max_health, self.health + amount)
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw character to screen."""
        sprite = self.sprite.get_current_sprite()
        
        # Flip sprite based on direction
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
            
        # Flash if invulnerable
        if self.invulnerable and int(self.invulnerable_time * 10) % 2:
            # Make semi-transparent when flashing
            sprite = sprite.copy()
            sprite.set_alpha(128)
            
        # Draw centered on position
        sprite_rect = sprite.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(sprite, sprite_rect)
        
        # Debug: Draw collision rect
        # pygame.draw.rect(screen, COLOR_WHITE, self.rect, 1)
        
    def get_position(self) -> tuple[float, float]:
        """Get current position."""
        return (self.x, self.y)
        
    def set_position(self, x: float, y: float):
        """Set position."""
        self.x = x
        self.y = y
        self.update_rect()
        
    def is_moving(self) -> bool:
        """Check if character is moving."""
        return abs(self.vx) > 10 or abs(self.vy) > 10
        
    def is_alive(self) -> bool:  
        """Check if character is alive."""
        return self.lives > 0
```

## NPC Character Template

```python
class NPCCharacter:
    """Template for non-player characters."""
    
    def __init__(self, x: float, y: float, character_name: str):
        self.x = x
        self.y = y
        self.character_name = character_name
        
        # AI state
        self.target = None
        self.behavior_state = "idle"
        self.behavior_timer = 0.0
        
        # Animation
        self.sprite = AnimatedCharacter(
            character_name.lower(),
            "hub",
            scale=(SPRITE_DISPLAY_SIZE, SPRITE_DISPLAY_SIZE)
        )
        
    def update(self, dt: float, player_pos: tuple[float, float]):
        """Update NPC behavior."""
        self.behavior_timer += dt
        
        if self.behavior_state == "idle":
            self.sprite.set_animation("idle", loop=True)
            if self.behavior_timer > 3.0:  # Change behavior every 3 seconds
                self.behavior_state = "wander"
                self.behavior_timer = 0.0
                
        elif self.behavior_state == "wander":
            # Simple wandering behavior
            self.sprite.set_animation("walk", loop=True)
            # ... implement wandering logic
            
        self.sprite.update()
        
    def draw(self, screen: pygame.Surface):
        """Draw NPC."""
        sprite = self.sprite.get_current_sprite()
        sprite_rect = sprite.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(sprite, sprite_rect)
```

## Character Factory

```python
def create_character(character_type: str, x: float, y: float, name: str):
    """Factory function for creating characters."""
    if character_type == "player":
        return PlayerCharacter(x, y, name)
    elif character_type == "npc":
        return NPCCharacter(x, y, name)
    else:
        raise ValueError(f"Unknown character type: {character_type}")
```