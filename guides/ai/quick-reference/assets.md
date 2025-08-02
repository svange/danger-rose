# Asset Pipeline - Quick Reference

## Asset Organization

```
assets/
├── images/
│   ├── characters/     # Player sprites (256x341px)
│   ├── backgrounds/    # Scene backgrounds
│   ├── ui/            # Menu elements
│   └── effects/       # Particles, explosions
├── audio/
│   ├── music/         # Background tracks (.ogg)
│   └── sfx/           # Sound effects (.wav/.ogg)
└── fonts/             # TTF font files
```

## Sprite Specifications

### Character Sprites
```
Size: 256x341 pixels per frame
Sheet: 1024x1024 (3x4 grid = 12 frames)
Display: Scaled to 128x128 in-game
Format: PNG with transparency
Animations: idle, walk, jump, attack, hurt, victory
```

### Background Images
```
Size: 1920x1080 pixels (full screen)
Format: PNG or JPG
Compression: Moderate for file size
Style: Pixel art or low-res friendly
```

## Loading Assets

### Basic Image Loading
```python
from src.utils.sprite_loader import load_sprite

# Load single image
sprite = load_sprite("characters/danger_idle.png")

# Load with fallback
sprite = load_sprite_with_fallback(
    "characters/danger_idle.png",
    size=(128, 128),
    color=(255, 0, 255)  # Magenta placeholder
)
```

### Animation Loading
```python
from src.utils.animation import AnimatedCharacter

# Load character animations
character = AnimatedCharacter(
    "characters/danger",
    frame_size=(256, 341),
    scale_to=(128, 128)
)

# Play animation
character.play_animation("walk")
character.update(dt)
```

### Audio Loading
```python
from src.managers.sound_manager import SoundManager

sound_mgr = SoundManager()

# Load background music
sound_mgr.load_music("music/hub_theme.ogg")

# Load sound effect
sound_mgr.load_sound("sfx/jump.wav", "jump")

# Play audio
sound_mgr.play_music("hub_theme")
sound_mgr.play_sound("jump")
```

## Asset Validation

### Check Sprites
```bash
# Validate all sprites exist
/validate-sprites

# Fix missing sprites with placeholders
/validate-sprites --fix

# Check specific directory
/validate-sprites assets/images/characters/
```

### Generate Placeholders
```bash
# Create placeholder sprite
/generate-placeholder character danger 128 128

# Create placeholder background
/generate-placeholder background hub 1920 1080
```

## Sprite Sheet Tools

### Extract Frames
```bash
# Cut sprite sheet into frames
/sprite-cut assets/images/characters/danger.png 256 341

# Output: danger_00.png, danger_01.png, etc.
```

### Create Sprite Sheet
```python
from src.utils.sprite_tools import create_sprite_sheet

frames = [
    "danger_idle_00.png",
    "danger_idle_01.png",
    # ...
]

create_sprite_sheet(
    frames,
    output="danger_idle_sheet.png",
    grid_size=(4, 3)
)
```

## Performance Tips

### Optimize Loading
```python
# Pre-load common assets
assets = {
    "player": load_sprite("characters/danger.png"),
    "background": load_sprite("backgrounds/hub.png")
}

# Use sprite groups for batch operations
sprite_group = pygame.sprite.Group()
sprite_group.add(player_sprite)
```

### Memory Management
```python
# Convert surfaces after loading
surface = pygame.image.load(path).convert_alpha()

# Use appropriate color depth
surface = surface.convert()  # No alpha needed
surface = surface.convert_alpha()  # With transparency
```

## Common Asset Patterns

### Character States
```
danger_idle.png      # Standing still
danger_walk_00.png   # Walking cycle frame 1
danger_walk_01.png   # Walking cycle frame 2
danger_jump.png      # Jumping pose
danger_hurt.png      # Taking damage
```

### UI Elements
```
button_normal.png    # Default button state
button_hover.png     # Mouse over state
button_pressed.png   # Clicked state
ui_panel.png         # Background panel
ui_cursor.png        # Custom cursor
```

### Effects
```
explosion_00.png     # Animation frame 1
explosion_01.png     # Animation frame 2
particle_spark.png   # Single particle
dust_cloud.png       # Environmental effect
```
