# Animation System Architecture

## Core Animation Components

The Danger Rose animation system supports both sprite sheets and individual PNG files with frame timing and state management.

## AnimatedCharacter Class

```python
from src.utils.attack_character import AnimatedCharacter

# Create character with scene-specific sprites
character = AnimatedCharacter(
    character_name="danger",
    scene="hub",  # hub, ski, pool, vegas
    scale=(128, 128)
)

# Update animation system
character.update()
current_sprite = character.get_current_sprite()
```

## Animation States

```python
# Set animation with looping control
character.set_animation("walk", loop=True)
character.set_animation("attack", loop=False)  # Plays once

# Available animations
animations = ["idle", "walk", "jump", "attack", "hurt", "victory"]

# Check animation status
if character.has_animation("attack"):
    character.set_animation("attack")
```

## Frame Timing System

```python
# Animation speeds (seconds per frame)
animation_speeds = {
    "idle": 0.2,      # Slow idle cycle
    "walk": 0.1,      # Medium walk cycle
    "jump": 0.15,     # Smooth jump
    "attack": 0.05,   # Fast attack
    "hurt": 0.2,      # Brief hurt flash
    "victory": 0.15   # Celebratory victory
}

# Frame timing updates automatically in character.update()
def update(self):
    current_time = time.time()
    speed = self.animation_speeds.get(self.current_animation, 0.1)

    if current_time - self.last_frame_time >= speed:
        if self.loop_animation:
            self.current_frame = (self.current_frame + 1) % len(frames)
        else:
            self.current_frame = min(self.current_frame + 1, len(frames) - 1)
```

## Sprite Loading Priority

```python
# 1. Try individual PNG files first
# assets/images/characters/new_sprites/danger/hub/idle_01.png
animations = load_character_individual_files(
    character_name="danger",
    scene="hub",
    scale=(128, 128)
)

# 2. Fallback to sprite sheets
# assets/images/characters/danger.png
animations = load_character_animations(sprite_path, scale)

# 3. Generate placeholders if missing
placeholder = pygame.Surface((128, 128))
placeholder.fill((255, 0, 255))  # Magenta placeholder
```

## Integration with Player

```python
class Player:
    def __init__(self, x, y, character_name):
        self.sprite = AnimatedCharacter(
            character_name.lower(),
            "hub",
            scale=(SPRITE_DISPLAY_SIZE, SPRITE_DISPLAY_SIZE)
        )

    def update(self, dt, boundaries):
        # Update animation based on movement
        if self.is_moving():
            self.sprite.set_animation("walk", loop=True)
        else:
            self.sprite.set_animation("idle", loop=True)

        self.sprite.update()

    def draw(self, screen):
        sprite = self.sprite.get_current_sprite()

        # Handle sprite flipping for direction
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)

        screen.blit(sprite, (self.x, self.y))
```
