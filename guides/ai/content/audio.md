# Audio Integration with SoundManager

Music and sound effects integration for immersive family-friendly gameplay.

## SoundManager Basic Usage

```python
from src.managers.sound_manager import SoundManager

class GameScene(Scene):
    def __init__(self):
        self.sound_manager = SoundManager()

        # Start scene music
        self.sound_manager.play_music("ski_theme.ogg")

        # Preload common sound effects
        self.sound_manager.preload_sounds([
            "jump.ogg",
            "collect_item.ogg",
            "collision.ogg",
            "victory.ogg"
        ])
```

## Scene-Based Music Management

```python
def on_enter(self, previous_scene: str = None, data: dict = None):
    """Start appropriate music when entering scene."""
    music_tracks = {
        "hub": "hub_theme.ogg",
        "ski": "ski_theme.ogg",
        "pool": "pool_theme.ogg",
        "vegas": "vegas_theme.ogg",
        "title": "title_theme.ogg"
    }

    scene_name = self.__class__.__name__.lower().replace("scene", "")
    if scene_name in music_tracks:
        self.sound_manager.play_music(music_tracks[scene_name])

def on_exit(self) -> dict:
    """Fade out music when leaving scene."""
    self.sound_manager.stop_music(fade_time=1000)  # 1 second fade
    return {}
```

## Sound Effect Patterns

```python
# Player actions
def handle_jump(self):
    self.sound_manager.play_sound("jump.ogg")
    self.player.start_jump()

def handle_collect_item(self, item):
    # Different sounds for different item types
    sound_map = {
        "snowflake": "collect_item.ogg",
        "coin": "collect_item.ogg",
        "powerup": "victory.ogg"
    }
    sound = sound_map.get(item.type, "collect_item.ogg")
    self.sound_manager.play_sound(sound)

# Collision feedback
def handle_collision(self, collision_type):
    if collision_type == "obstacle":
        self.sound_manager.play_sound("collision.ogg")
    elif collision_type == "enemy":
        self.sound_manager.play_sound("player_hurt.wav")
```

## Dynamic Volume Control

```python
def update_audio_based_on_game_state(self):
    """Adjust audio dynamically based on game events."""

    # Lower music volume during intense moments
    if self.lives <= 1:
        self.sound_manager.set_music_volume(0.3)
    else:
        self.sound_manager.set_music_volume(0.7)

    # Pause audio when game is paused
    if self.paused:
        self.sound_manager.pause_music()
    else:
        self.sound_manager.unpause_music()
```

## Audio Feedback for UI

```python
def handle_menu_navigation(self, direction):
    """Audio feedback for menu interactions."""
    self.sound_manager.play_sound("menu_move.ogg")

def handle_menu_selection(self):
    """Confirmation sound for selections."""
    self.sound_manager.play_sound("menu_select.ogg")

def handle_door_interaction(self):
    """Door opening sound effect."""
    self.sound_manager.play_sound("door_open.wav")
```

## Kid-Friendly Audio Patterns

```python
def create_encouraging_audio_sequence(self):
    """Play encouraging sounds for young players."""
    encouragement_sounds = [
        "victory.ogg",
        "collect_item.ogg",
        "jump.ogg"
    ]

    # Play a sequence of positive sounds
    for i, sound in enumerate(encouragement_sounds):
        pygame.time.set_timer(
            pygame.USEREVENT + i,
            i * 500  # 500ms between sounds
        )
        # Handle in event loop to play sound

def handle_failure_gently(self):
    """Gentle audio feedback for mistakes."""
    # Use softer collision sound for kids
    self.sound_manager.play_sound("player_hurt.wav", volume=0.5)

    # Follow up with encouraging sound after delay
    pygame.time.set_timer(pygame.USEREVENT + 10, 1000)
```

## Audio Settings Integration

```python
class AudioSettings:
    def __init__(self):
        self.sound_manager = SoundManager()
        self.master_volume = 0.7
        self.music_volume = 0.8
        self.sfx_volume = 0.9

    def apply_settings(self):
        """Apply current audio settings."""
        self.sound_manager.set_master_volume(self.master_volume)
        self.sound_manager.set_music_volume(self.music_volume)
        self.sound_manager.set_sfx_volume(self.sfx_volume)

    def save_settings(self):
        """Save audio preferences."""
        settings = {
            "master_volume": self.master_volume,
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume
        }
        SaveManager().save_settings(settings)
```

## Spatial Audio for Game Feel

```python
def play_positional_sound(self, sound_name: str, position: tuple, player_position: tuple):
    """Play sound with volume based on distance from player."""
    distance = math.sqrt(
        (position[0] - player_position[0]) ** 2 +
        (position[1] - player_position[1]) ** 2
    )

    # Calculate volume based on distance (closer = louder)
    max_distance = 300  # Maximum audible distance
    volume = max(0.1, 1.0 - (distance / max_distance))

    self.sound_manager.play_sound(sound_name, volume=volume)

# Usage in game
def update_environmental_audio(self):
    # Play ambient sounds based on player position
    if self.player.x < 200:  # Near water area
        self.play_positional_sound("splash.wav", (100, 300), (self.player.x, self.player.y))
```
