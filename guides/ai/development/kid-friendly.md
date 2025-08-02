# Kid-Friendly Coding Patterns

## Clear Variable Names

Use descriptive names that explain what things do, not cryptic abbreviations.

```python
# Good: Clear and descriptive
player_speed = 300.0
lives_remaining = 3
points_earned = 0
game_is_paused = False
character_is_jumping = False

# Avoid: Cryptic abbreviations
spd = 300.0
hp = 3
pts = 0
paused = False
jmp = False
```

## Simple Functions with Clear Purpose

```python
def make_player_jump():
    """Make the player character jump up in the air."""
    if player_is_on_ground:
        player.velocity_y = JUMP_POWER  # Negative goes up
        player_is_jumping = True
        play_sound("jump.wav")

def collect_treasure(treasure_item):
    """Player found a treasure! Add points and remove treasure."""
    points_earned += treasure_item.points
    treasure_item.disappear()
    show_happy_sparkles(treasure_item.x, treasure_item.y)
    play_sound("collect.wav")

def check_if_player_wins():
    """See if the player collected enough treasures to win."""
    if points_earned >= points_needed_to_win:
        show_victory_message()
        play_victory_music()
        return True
    return False
```

## Helpful Comments for Learning

```python
class Player:
    def __init__(self, starting_x, starting_y, character_name):
        # Where the player starts on screen
        self.x = starting_x
        self.y = starting_y

        # How fast the player moves (pixels per second)
        self.speed = 300.0

        # Which direction is the player facing? (True = right, False = left)
        self.facing_right = True

        # Load the character's pictures for animation
        self.sprite = AnimatedCharacter(character_name, "hub", (128, 128))

    def move_left(self):
        """Move the player to the left side of screen."""
        self.x -= self.speed * time_passed  # Subtract moves left
        self.facing_right = False  # Now facing left

    def move_right(self):
        """Move the player to the right side of screen."""
        self.x += self.speed * time_passed  # Add moves right
        self.facing_right = True  # Now facing right
```

## Constants with Explanations

```python
# Game Screen Settings - How big is our game window?
SCREEN_WIDTH = 1280  # Width in pixels (dots across)
SCREEN_HEIGHT = 720  # Height in pixels (dots down)
FPS = 60  # How many times per second we redraw everything

# Player Movement - How the character moves around
PLAYER_SPEED = 300.0  # How fast player moves (pixels per second)
JUMP_POWER = -500.0   # How strong the jump is (negative goes up!)
GRAVITY = 800.0       # How fast things fall down

# Game Rules - What makes the game fun?
MAX_LIVES = 3         # How many times player can get hurt
POINTS_FOR_COIN = 10  # Points you get for collecting a coin
GAME_TIME = 60.0      # How many seconds to play the game
```

## Visual Feedback Patterns

```python
def show_player_got_hurt():
    """Flash the screen red when player gets hurt."""
    # Make the screen flash red briefly
    hurt_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    hurt_overlay.fill(COLOR_RED)
    hurt_overlay.set_alpha(100)  # Make it see-through
    screen.blit(hurt_overlay, (0, 0))

    # Play hurt sound
    play_sound("ouch.wav")

    # Make player blink for a few seconds so they can't get hurt again
    player.invincible_time = 2.0  # Safe for 2 seconds

def show_victory_celebration():
    """Show exciting effects when player wins!"""
    # Sparkles everywhere!
    for i in range(50):
        sparkle_x = random.randint(0, SCREEN_WIDTH)
        sparkle_y = random.randint(0, SCREEN_HEIGHT)
        create_sparkle(sparkle_x, sparkle_y)

    # Victory message
    big_text = font_huge.render("YOU WON!", True, COLOR_GOLD)
    screen.blit(big_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))

    # Happy music
    play_victory_music()
```

## Simple Error Handling

```python
def load_player_sprite(character_name):
    """Try to load the character's picture. If it fails, use a placeholder."""
    try:
        # Try to load the real character picture
        sprite_path = f"assets/characters/{character_name}.png"
        player_image = pygame.image.load(sprite_path)
        print(f"Loaded {character_name} successfully!")
        return player_image

    except:
        # Oops! The picture file is missing. Let's make a simple colored square.
        print(f"Couldn't find picture for {character_name}, using placeholder")
        placeholder = pygame.Surface((128, 128))
        placeholder.fill(COLOR_PURPLE)  # Purple square as backup
        return placeholder

def save_high_score(player_name, points):
    """Save the player's score. Don't crash if something goes wrong."""
    try:
        # Try to save the score
        save_manager.add_high_score("game", player_name, {"score": points})
        print(f"Saved {player_name}'s score of {points} points!")

    except:
        # If saving fails, just tell the player - don't break the game
        print("Couldn't save high score right now, but great job playing!")
```

## Kid-Friendly Debug Output

```python
def debug_print_player_info():
    """Show helpful info about what the player is doing."""
    if DEBUG_MODE:
        print(f"Player is at position ({player.x}, {player.y})")
        print(f"Player is moving {player.speed} pixels per second")
        print(f"Player is facing {'right' if player.facing_right else 'left'}")
        print(f"Player has {player.lives} lives left")
        print(f"Current animation: {player.sprite.current_animation}")
```
