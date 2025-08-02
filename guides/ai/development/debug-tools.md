# Debug Tools and Features

## Environment Variable Debug Controls

Control debug features through environment variables for easy testing.

```bash
# Debug rendering
DEBUG_SHOW_FPS=true make run          # Show FPS counter
DEBUG_SHOW_HITBOXES=true make run     # Show collision boxes
DEBUG_SHOW_GRID=true make run         # Show grid overlay

# Scene debugging
START_SCENE=ski make run              # Skip to specific scene
SKIP_TITLE=true make run              # Skip title screen

# Audio debugging
MUTE_AUDIO=true make run              # Disable all audio
MUSIC_VOLUME=0.3 make run             # Set music volume
```

## GameConfig Debug Settings

```python
from src.config.game_config import get_config

config = get_config()

# Access debug settings
if config.show_fps:
    draw_fps_counter(screen, clock.get_fps())

if config.get("debug.show_hitboxes", False):
    for entity in entities:
        pygame.draw.rect(screen, COLOR_RED, entity.rect, 2)

if config.get("debug.show_grid", False):
    draw_debug_grid(screen)
```

## Visual Debug Helpers

```python
def draw_debug_info(screen, player, entities):
    """Draw debug overlays for development."""
    if not DEBUG_MODE:
        return

    # Player info
    debug_font = pygame.font.Font(None, 24)

    # Position and velocity
    pos_text = f"Pos: ({player.x:.1f}, {player.y:.1f})"
    vel_text = f"Vel: ({player.vx:.1f}, {player.vy:.1f})"

    screen.blit(debug_font.render(pos_text, True, COLOR_WHITE), (10, 10))
    screen.blit(debug_font.render(vel_text, True, COLOR_WHITE), (10, 35))

    # Animation info
    anim_info = player.sprite.get_animation_info()
    screen.blit(debug_font.render(anim_info, True, COLOR_WHITE), (10, 60))

    # Collision boxes
    pygame.draw.rect(screen, COLOR_RED, player.rect, 2)

    # Entity hitboxes
    for entity in entities:
        pygame.draw.rect(screen, COLOR_YELLOW, entity.rect, 1)

def draw_fps_counter(screen, fps):
    """Draw FPS counter in top-right corner."""
    fps_font = pygame.font.Font(None, 36)
    fps_text = fps_font.render(f"FPS: {fps:.1f}", True, COLOR_WHITE)
    screen.blit(fps_text, (screen.get_width() - 120, 10))
```

## Asset Debug Tools

```python
# tools/check_assets.py - Validate all game assets
def check_character_sprites():
    """Check if all character sprite files exist."""
    characters = ["danger", "rose", "dad"]
    scenes = ["hub", "ski", "pool", "vegas"]
    animations = ["idle", "walk", "jump", "attack", "hurt", "victory"]

    missing_files = []

    for character in characters:
        for scene in scenes:
            for animation in animations:
                for frame in range(1, 6):  # Check up to 5 frames
                    path = f"assets/images/characters/new_sprites/{character}/{scene}/{animation}_{frame:02d}.png"
                    if not os.path.exists(path):
                        missing_files.append(path)

    if missing_files:
        print("Missing sprite files:")
        for file in missing_files[:10]:  # Show first 10
            print(f"  - {file}")
    else:
        print("All sprite files found!")

# Usage in code
def load_with_debug(path):
    """Load image with debug logging."""
    if DEBUG_MODE:
        print(f"Loading asset: {path}")

    if not os.path.exists(path):
        print(f"WARNING: Missing asset {path}")
        return create_placeholder()

    return pygame.image.load(path)
```

## Performance Profiling

```python
import time
import cProfile

class PerformanceMonitor:
    def __init__(self):
        self.frame_times = []
        self.update_times = []
        self.draw_times = []

    def start_frame(self):
        self.frame_start = time.perf_counter()

    def start_update(self):
        self.update_start = time.perf_counter()

    def end_update(self):
        self.update_times.append(time.perf_counter() - self.update_start)

    def start_draw(self):
        self.draw_start = time.perf_counter()

    def end_draw(self):
        self.draw_times.append(time.perf_counter() - self.draw_start)

    def end_frame(self):
        self.frame_times.append(time.perf_counter() - self.frame_start)

    def get_stats(self):
        if not self.frame_times:
            return "No performance data"

        avg_frame = sum(self.frame_times) / len(self.frame_times) * 1000
        avg_update = sum(self.update_times) / len(self.update_times) * 1000
        avg_draw = sum(self.draw_times) / len(self.draw_times) * 1000

        return f"Frame: {avg_frame:.2f}ms, Update: {avg_update:.2f}ms, Draw: {avg_draw:.2f}ms"

# Usage in main game loop
perf = PerformanceMonitor()

while running:
    perf.start_frame()

    # Handle events...

    perf.start_update()
    scene.update(dt)
    perf.end_update()

    perf.start_draw()
    scene.draw(screen)
    perf.end_draw()

    perf.end_frame()

    # Print stats every 60 frames
    if frame_count % 60 == 0:
        print(perf.get_stats())
```

## Console Debug Commands

```python
class DebugConsole:
    def __init__(self, game_scene):
        self.scene = game_scene
        self.commands = {
            "give_lives": self.give_lives,
            "set_score": self.set_score,
            "toggle_invincible": self.toggle_invincible,
            "spawn_powerup": self.spawn_powerup,
            "teleport": self.teleport_player,
        }

    def process_command(self, command_line):
        parts = command_line.split()
        if not parts:
            return

        command = parts[0]
        args = parts[1:]

        if command in self.commands:
            try:
                self.commands[command](*args)
            except Exception as e:
                print(f"Debug command error: {e}")
        else:
            print(f"Unknown command: {command}")

    def give_lives(self, count="1"):
        self.scene.player.lives += int(count)
        print(f"Gave {count} lives. Total: {self.scene.player.lives}")

    def set_score(self, score="0"):
        self.scene.score = int(score)
        print(f"Set score to {score}")

    def teleport_player(self, x="0", y="0"):
        self.scene.player.x = float(x)
        self.scene.player.y = float(y)
        print(f"Teleported to ({x}, {y})")

# In game scene
def handle_event(self, event):
    if DEBUG_MODE and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_F1:
            self.debug_console.process_command("give_lives 1")
        elif event.key == pygame.K_F2:
            self.debug_console.process_command("spawn_powerup")
```

## Save File Debugging

```python
def debug_save_data():
    """Print save data in readable format."""
    save_manager = SaveManager()
    data = save_manager.load()

    print("=== SAVE DATA DEBUG ===")
    print(f"Version: {data.get('version')}")
    print(f"Character: {data.get('player', {}).get('selected_character')}")
    print(f"Settings: {data.get('settings', {})}")

    high_scores = data.get('high_scores', {})
    for game, characters in high_scores.items():
        print(f"\n{game.upper()} High Scores:")
        for character, difficulties in characters.items():
            for difficulty, scores in difficulties.items():
                if scores:
                    best = max(scores, key=lambda x: x.get('score', 0))
                    print(f"  {character} ({difficulty}): {best.get('score', 0)}")

# Check save file integrity
def validate_save_file():
    """Check if save file is valid JSON."""
    save_path = SaveManager().save_file_path
    if save_path.exists():
        try:
            with open(save_path) as f:
                json.load(f)
            print("Save file is valid JSON")
        except json.JSONDecodeError as e:
            print(f"Save file is corrupted: {e}")
    else:
        print("No save file found")
```
