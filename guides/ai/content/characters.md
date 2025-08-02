# Character Setup and Animation

Player and NPC setup with animations and states for family-friendly gameplay.

## Character Creation Pattern

```python
from src.utils.animated_character import AnimatedCharacter
from src.utils.sprite_loader import load_character_animations

class Player:
    def __init__(self, x: float, y: float, character_name: str):
        self.x, self.y = x, y
        self.character_name = character_name
        
        # Animation setup
        sprite_path = f"assets/images/characters/{character_name}.png"
        self.sprite = AnimatedCharacter(character_name, sprite_path)
        
        # Physics
        self.vx = self.vy = 0.0
        self.speed = PLAYER_SPEED
        
        # State management
        self.facing_right = True
        self.current_state = "idle"
        self.invincible = False
        self.invincible_timer = 0.0
```

## Animation State Management

```python
def _update_animation(self):
    # Determine animation based on movement
    if self.vx != 0 or self.vy != 0:
        new_state = "walking"
    elif self.is_jumping:
        new_state = "jumping"
    elif self.is_attacking:
        new_state = "attacking"
    else:
        new_state = "idle"
    
    # Update sprite direction
    if self.vx > 0:
        self.facing_right = True
    elif self.vx < 0:
        self.facing_right = False
    
    # Apply animation change
    if new_state != self.current_state:
        self.current_state = new_state
        self.sprite.set_animation(new_state)
    
    self.sprite.update()
```

## Character Drawing with Invincibility

```python
def draw(self, screen: pygame.Surface):
    # Handle invincibility flashing
    if self.invincible:
        # Flash effect for visual feedback
        flash_rate = FLASH_INVINCIBILITY_RATE
        if int(time.time() * flash_rate) % 2:
            return  # Skip drawing for flash effect
    
    # Get current sprite frame
    sprite_surface = self.sprite.get_current_frame()
    
    # Flip sprite if facing left
    if not self.facing_right:
        sprite_surface = pygame.transform.flip(sprite_surface, True, False)
    
    # Draw centered on position
    rect = sprite_surface.get_rect()
    rect.center = (int(self.x), int(self.y))
    screen.blit(sprite_surface, rect)
```

## NPC AI Pattern (Dad Character)

```python
class DadAI:
    def __init__(self, player, boundaries):
        self.player = player
        self.boundaries = boundaries
        
        # AI behavior states
        self.behavior = "follow"  # follow, patrol, idle
        self.target_position = None
        self.path_points = []
        
        # Character setup
        self.sprite = AnimatedCharacter("dad", "dad.png")
        self.speed = PLAYER_SPEED * 0.8  # Slightly slower than player
        
    def update(self, dt: float):
        if self.behavior == "follow":
            self._follow_player(dt)
        elif self.behavior == "patrol":
            self._patrol_area(dt)
        
        self._update_animation()
        self.sprite.update()
    
    def _follow_player(self, dt: float):
        # Simple following behavior with distance check
        distance_to_player = self._distance_to(self.player)
        
        if distance_to_player > MIN_FOLLOW_DISTANCE:
            direction = self._direction_to(self.player)
            self.x += direction[0] * self.speed * dt
            self.y += direction[1] * self.speed * dt
```

## Character Animation Configurations

```python
# Animation frame counts for each character
ANIMATION_FRAMES = {
    "danger": {
        "idle": 4,
        "walking": 4, 
        "jumping": 3,
        "attacking": 4
    },
    "rose": {
        "idle": 4,
        "walking": 4,
        "jumping": 3, 
        "attacking": 4
    },
    "dad": {
        "idle": 4,
        "walking": 4,
        "jumping": 3
    }
}

# Load character with specific frame counts
def load_character_sprite(character_name: str):
    frames = ANIMATION_FRAMES.get(character_name, ANIMATION_FRAMES["danger"])
    return load_character_animations(
        f"assets/images/characters/{character_name}.png",
        frame_counts=frames
    )
```

## Character State Machine

```python
class CharacterState:
    def __init__(self, character):
        self.character = character
        self.states = {
            "idle": IdleState(character),
            "moving": MovingState(character), 
            "jumping": JumpingState(character),
            "hurt": HurtState(character)
        }
        self.current_state = "idle"
    
    def update(self, dt: float):
        current = self.states[self.current_state]
        new_state = current.update(dt)
        
        if new_state and new_state != self.current_state:
            self.states[self.current_state].on_exit()
            self.current_state = new_state
            self.states[self.current_state].on_enter()

class IdleState:
    def update(self, dt: float) -> str:
        if self.character.vx != 0 or self.character.vy != 0:
            return "moving"
        return "idle"
```