# Common Game Patterns

## Entity-Component Pattern

Standard pattern for game objects with position, movement, and collision.

```python
class Player:
    def __init__(self, x: float, y: float, character_name: str):
        # Position and physics
        self.x, self.y = x, y
        self.vx, self.vy = 0.0, 0.0

        # Input state
        self.move_left = self.move_right = False
        self.move_up = self.move_down = False

        # Visual representation
        self.sprite = AnimatedCharacter(character_name, "hub", (128, 128))
        self.rect = pygame.Rect(x - 64, y - 64, 128, 128)
        self.facing_right = True

    def update(self, dt: float, boundaries: list[pygame.Rect]):
        # Handle movement input
        self._update_velocity()
        self._update_position(dt)
        self._handle_collisions(boundaries)
        self._update_animation()
        self.sprite.update()
```

## State-Based Movement

```python
def _update_velocity(self):
    target_vx = target_vy = 0.0

    if self.move_left: target_vx -= PLAYER_SPEED
    if self.move_right: target_vx += PLAYER_SPEED
    if self.move_up: target_vy -= PLAYER_SPEED
    if self.move_down: target_vy += PLAYER_SPEED

    # Normalize diagonal movement
    if target_vx != 0 and target_vy != 0:
        diagonal_factor = 0.707  # 1/sqrt(2)
        target_vx *= diagonal_factor
        target_vy *= diagonal_factor

    self.vx, self.vy = target_vx, target_vy
```

## Collision Detection Pattern

```python
def _handle_collisions(self, boundaries):
    old_x, old_y = self.x, self.y

    # Update position
    self.x += self.vx * dt
    self.y += self.vy * dt
    self.rect.center = (int(self.x), int(self.y))

    # Check for collisions
    if any(self.rect.colliderect(b) for b in boundaries):
        # Try horizontal movement only
        self.x = old_x + self.vx * dt
        self.y = old_y
        self.rect.center = (int(self.x), int(self.y))

        if any(self.rect.colliderect(b) for b in boundaries):
            # Try vertical movement only
            self.x = old_x
            self.y = old_y + self.vy * dt
            self.rect.center = (int(self.x), int(self.y))

            if any(self.rect.colliderect(b) for b in boundaries):
                # Can't move, revert to old position
                self.x, self.y = old_x, old_y
                self.rect.center = (int(self.x), int(self.y))
```

## Game Loop Structure

```python
class GameScene(Scene):
    def __init__(self):
        self.entities = pygame.sprite.Group()
        self.player = None
        self.obstacles = []
        self.collectibles = []

    def update(self, dt: float):
        # Update all entities
        self.player.update(dt, self.obstacles)
        self.entities.update(dt)

        # Handle collisions
        collected = pygame.sprite.spritecollide(
            self.player, self.collectibles, True
        )
        for item in collected:
            self.handle_collection(item)

    def draw(self, screen: pygame.Surface):
        screen.fill(COLOR_SKY_BLUE)
        self.player.draw(screen)
        self.entities.draw(screen)
```

## Input Handling Pattern

```python
def handle_event(self, event: pygame.event.Event) -> str | None:
    if event.type == pygame.KEYDOWN:
        # Movement keys
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
            return self.handle_action()
        elif event.key == pygame.K_ESCAPE:
            return "pause"

    elif event.type == pygame.KEYUP:
        # Release movement keys
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.player.move_left = False
        # ... etc

    return None
```

## UI Drawing Helpers

```python
from src.ui.drawing_helpers import draw_text_with_background, draw_lives

def draw_ui(self, screen: pygame.Surface):
    # Score display
    draw_text_with_background(
        screen, f"Score: {self.score}", self.font,
        (screen.get_width() // 2, 50),
        text_color=COLOR_BLACK,
        bg_color=COLOR_WHITE
    )

    # Lives display
    draw_lives(screen, self.lives, self.max_lives, y=20, right_align=True)

    # Timer
    time_left = max(0, self.game_duration - self.elapsed_time)
    draw_text_with_background(
        screen, f"Time: {time_left:.0f}", self.font,
        (screen.get_width() // 2, 100)
    )
```

## Particle System Pattern

```python
class Particle:
    def __init__(self, x, y, vx, vy, color, lifetime=1.0):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.color = color
        self.lifetime = self.max_lifetime = lifetime

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt
        return self.lifetime > 0

    def draw(self, screen):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = (*self.color, alpha)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 3)

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, count=10):
        for _ in range(count):
            vx = random.uniform(-100, 100)
            vy = random.uniform(-100, 100)
            self.particles.append(Particle(x, y, vx, vy, COLOR_YELLOW))

    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
```
