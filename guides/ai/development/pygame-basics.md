# Pygame Basics for Danger Rose

## Core Pygame Loop

Every Danger Rose scene follows the standard pygame pattern: handle events, update game state, draw to screen.

```python
class GameScene(Scene):
    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Process input events - keyboard, mouse, etc."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.jump()
        return None
    
    def update(self, dt: float) -> None:
        """Update game logic with delta time in seconds."""
        self.player.update(dt, self.obstacles)
        self.entities.update(dt)
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw everything to the screen."""
        screen.fill(COLOR_SKY_BLUE)
        self.player.draw(screen)
        self.entities.draw(screen)
```

## Surface and Rect System

```python
# Create surfaces for sprites and UI
player_surface = pygame.image.load("player.png").convert_alpha()
background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill(COLOR_SKY_BLUE)

# Rects for collision detection and positioning
player_rect = player_surface.get_rect(center=(640, 360))
obstacle_rect = pygame.Rect(100, 200, 64, 64)

# Check collisions
if player_rect.colliderect(obstacle_rect):
    handle_collision()

# Draw with positioning
screen.blit(player_surface, player_rect)
screen.blit(background, (0, 0))
```

## Event Handling Patterns

```python
def handle_event(self, event: pygame.event.Event) -> str | None:
    if event.type == pygame.KEYDOWN:
        # Character movement (multiple key support)
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.player.move_left = True
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.player.move_right = True
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.player.move_up = True
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.player.move_down = True
            
        # Action keys
        elif event.key == pygame.K_SPACE:
            self.player.jump()
        elif event.key == pygame.K_ESCAPE:
            return "pause"  # Scene transition
            
    elif event.type == pygame.KEYUP:
        # Stop movement when key released
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.player.move_left = False
        # ... etc
            
    return None
```

## Sprite Groups and Collision

```python
class GameScene(Scene):
    def __init__(self):
        # Sprite groups for organization
        self.all_entities = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # Add sprites to groups
        self.all_entities.add(snowflake, tree, coin)
        self.obstacles.add(tree)
        self.collectibles.add(coin)

    def update(self, dt: float):
        # Update all sprites
        self.all_entities.update(dt)
        
        # Check collisions between groups
        collected = pygame.sprite.spritecollide(
            self.player, self.collectibles, True  # Remove collected items
        )
        for item in collected:
            self.score += item.points
            
        # Check obstacle collisions
        if pygame.sprite.spritecollide(self.player, self.obstacles, False):
            self.player.handle_collision()
```

## Animation with pygame.time

```python
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames: list[pygame.Surface]):
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        
        # Animation timing
        self.frame_duration = 100  # milliseconds
        self.last_frame_time = pygame.time.get_ticks()
    
    def update(self, dt: float):
        # Update animation based on real time
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_frame_time = current_time
```

## Delta Time Movement

```python
class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0  # velocity x
        self.vy = 0.0  # velocity y
        self.speed = 300.0  # pixels per second
        
    def update(self, dt: float):
        # Delta time ensures consistent movement regardless of framerate
        # dt is in seconds (e.g., 0.016 for 60 FPS)
        
        # Update position based on velocity and time
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Apply gravity
        self.vy += GRAVITY * dt
        
        # Speed limit
        if self.vy > MAX_FALL_SPEED:
            self.vy = MAX_FALL_SPEED
            
        # Update collision rect
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
```

## Sound Integration

```python
from src.managers.sound_manager import SoundManager

class GameScene(Scene):
    def __init__(self):
        self.sound_manager = SoundManager()
        self.sound_manager.load_sounds()
        
    def on_enter(self, previous_scene, data):
        # Start background music for this scene
        self.sound_manager.play_music("hub_theme.ogg", loop=True)
        
    def handle_player_jump(self):
        # Play sound effects for actions
        self.sound_manager.play_sfx("jump.wav")
        
    def handle_collision(self):
        self.sound_manager.play_sfx("collision.ogg")
        
    def on_exit(self):
        # Stop music when leaving scene
        self.sound_manager.stop_music()
```

## Drawing Helpers Usage

```python
from src.ui.drawing_helpers import (
    draw_text_with_background, 
    draw_lives, 
    draw_progress_bar
)

def draw_ui(self, screen: pygame.Surface):
    # Score with background
    draw_text_with_background(
        screen, f"Score: {self.score}", self.font,
        (screen.get_width() // 2, 50),
        text_color=COLOR_BLACK,
        bg_color=COLOR_WHITE,
        border_color=COLOR_BLACK
    )
    
    # Health/lives display
    draw_lives(screen, self.lives, MAX_LIVES, y=20, right_align=True)
    
    # Power-up timer bar
    if self.powerup_active:
        progress = self.powerup_time_left / self.powerup_duration
        draw_progress_bar(
            screen, 50, 100, 200, 20, progress,
            bg_color=COLOR_BLACK, fill_color=COLOR_YELLOW
        )
```

## Constants Integration

```python
from src.config.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PLAYER_SPEED, GRAVITY, JUMP_VELOCITY,
    COLOR_SKY_BLUE, COLOR_WHITE, COLOR_RED
)

class SkiGame(Scene):
    def __init__(self):
        # Use project constants for consistency
        self.player_speed = PLAYER_SPEED
        self.scroll_speed = SKI_SCROLL_SPEED
        self.max_lives = SKI_MAX_LIVES
        
        # Screen boundaries
        self.screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
```