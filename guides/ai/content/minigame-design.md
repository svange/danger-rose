# Minigame Design Patterns

Patterns for creating new minigames following Danger Rose's family-friendly approach.

## Base Minigame Structure

```python
class MyMinigameScene(Scene):
    def __init__(self):
        # Core game state
        self.score = 0
        self.lives = SKI_MAX_LIVES  # Use constants from config
        self.game_time = 0.0
        self.game_over = False
        
        # Player setup
        self.player = Player(400, 300, "danger")  # Default character
        self.player_animations = load_character_animations("danger.png")
        
        # Game objects
        self.obstacles = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
```

## Input Handling Pattern

```python
def handle_event(self, event: pygame.event.Event) -> str | None:
    if self.game_over and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            return SCENE_LEADERBOARD
        elif event.key == pygame.K_ESCAPE:
            return SCENE_HUB_WORLD
    
    # Standard movement keys
    if event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.player.move_left = True
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.player.move_right = True
        elif event.key == pygame.K_SPACE:
            self.handle_action()  # Jump, shoot, etc.
    elif event.type == pygame.KEYUP:
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.player.move_left = False
```

## Game Loop Structure

```python
def update(self, dt: float) -> None:
    if self.game_over:
        return
        
    self.game_time += dt
    
    # Update entities
    self.player.update(dt, self.obstacles)
    self.obstacles.update(dt)
    self.collectibles.update(dt)
    
    # Handle collisions
    self._check_collectible_collisions()
    self._check_obstacle_collisions()
    
    # Check win/lose conditions
    if self.game_time >= GAME_DURATION:
        self._handle_game_end()
    elif self.lives <= 0:
        self._handle_game_over()
```

## Visual Feedback System

```python
def draw(self, screen: pygame.Surface) -> None:
    # Background
    screen.fill(COLOR_SKY_BLUE)
    
    # Game objects
    self.player.draw(screen)
    self.obstacles.draw(screen)
    self.collectibles.draw(screen)
    self.effects.draw(screen)
    
    # UI elements
    self._draw_ui(screen)
    
    if self.game_over:
        self._draw_game_over_overlay(screen)

def _draw_ui(self, screen: pygame.Surface):
    draw_lives(screen, self.lives, SKI_MAX_LIVES, y=20)
    draw_text_with_background(
        screen, f"Score: {self.score}", 
        FONT_LARGE, (screen.get_width() // 2, 50)
    )
```

## Collision and Scoring

```python
def _check_collectible_collisions(self):
    collected = pygame.sprite.spritecollide(
        self.player, self.collectibles, True
    )
    for item in collected:
        self.score += item.points
        self._create_score_effect(item.rect.center)
        SoundManager().play_sound("collect_item")

def _create_score_effect(self, position):
    # Visual feedback for scoring
    effect = ScorePopup(position, "+10", COLOR_GREEN)
    self.effects.add(effect)
```

## Kid-Friendly Error Handling

```python
def _handle_collision_with_obstacle(self, obstacle):
    if not self.player.invincible:
        self.lives -= 1
        self.player.make_invincible(PLAYER_INVINCIBILITY_DURATION)
        
        # Kid-friendly feedback
        self._show_encouragement_message()
        SoundManager().play_sound("player_hurt")
        
        if self.lives <= 0:
            self._handle_game_over()

def _show_encouragement_message(self):
    messages = ["Try again!", "You can do it!", "Almost there!"]
    message = random.choice(messages)
    self.notification = Notification(message, duration=2.0)
```