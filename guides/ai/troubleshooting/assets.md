# Asset Troubleshooting

## Missing Asset Handling

Danger Rose uses a robust placeholder system for missing assets.

### Image Placeholders
```python
def load_image(path: str) -> pygame.Surface:
    if not os.path.exists(path):
        # Creates bright magenta placeholder (easy to spot)
        surface = pygame.Surface((64, 64))
        surface.fill(COLOR_PLACEHOLDER)  # Magenta (255, 0, 255)
        return surface
```

### Audio Placeholders
```python
# Silent audio clips for missing sounds
if not os.path.exists(audio_path):
    # Create 1-second silent audio
    silent_sound = pygame.mixer.Sound(buffer=bytes(22050 * 2))
    return silent_sound
```

## Asset Validation

### Check All Assets
```bash
make assets-check              # Comprehensive asset validation
poetry run python tools/check_assets.py
```

### Validate Specific Asset Types
```bash
# Check audio files
ls -la assets/audio/music/*.ogg
ls -la assets/audio/sfx/*.ogg

# Check character sprites
ls -la assets/images/characters/
```

## Character Sprite Issues

### Missing Character Files
```python
# Expected structure:
assets/images/characters/
├── danger.png          # Main sprite sheet
├── rose.png
├── dad_kenney.png
└── new_sprites/       # Individual animation frames
    ├── danger/
    ├── rose/
    └── dad/
```

### Animation Frame Loading
```python
# AnimatedCharacter looks for individual files first
character_path = f"assets/images/characters/new_sprites/{character_name}"
if not os.path.exists(character_path):
    # Falls back to sprite sheet
    print(f"Using sprite sheet for {character_name}")
```

### Sprite Sheet Problems
```python
# Verify sprite sheet dimensions
def validate_sprite_sheet(image_path: str):
    if os.path.exists(image_path):
        image = pygame.image.load(image_path)
        width, height = image.get_size()
        print(f"Sprite sheet: {width}x{height}")
        # Expected: 1024x1024 for 3x4 grid
        if width != 1024 or height != 1024:
            print("Warning: Non-standard sprite sheet size")
```

## Audio Asset Issues

### Format Compatibility
```python
# Preferred formats:
# Music: OGG Vorbis (better compression)
# SFX: OGG or WAV (short sounds)

# Check audio format
import pygame.mixer
try:
    sound = pygame.mixer.Sound("assets/audio/sfx/jump.ogg")
    print("Audio loaded successfully")
except pygame.error as e:
    print(f"Audio loading failed: {e}")
```

### Missing Audio Files
```bash
# Download audio assets
make audio-download
python scripts/download_audio.py

# Check current audio status
make audio-check
```

## Tileset and Background Issues

### Missing Game Backgrounds
```python
# Each game scene needs background tilesets:
BACKGROUNDS = {
    "ski": "assets/images/tilesets/ski/winter_tileset.png",
    "pool": "assets/images/tilesets/pool/",
    "vegas": "assets/images/tilesets/vegas/",
    "hub": "assets/images/tilesets/living_room.png"
}
```

### Object Sprite Issues
```python
# Ski game objects
ski_objects = [
    "assets/images/tilesets/ski/tree.png",
    "assets/images/tilesets/ski/rock.png",
    "assets/images/tilesets/ski/snowball.png"
]

# Pool game objects
pool_objects = [
    "assets/images/tilesets/pool/water_balloon.png",
    "assets/images/tilesets/pool/splash_01.png"
]
```

## Build-Time Asset Issues

### Assets Not Included in Build
```python
# Verify PyInstaller spec includes all assets
datas=[
    ('assets', 'assets'),              # All assets
    ('src/config', 'src/config'),      # Config files
]
```

### Runtime Asset Path Resolution
```python
import sys
import os

def get_asset_path(relative_path: str) -> str:
    """Get asset path that works in both dev and build."""
    if hasattr(sys, '_MEIPASS'):  # PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path

# Usage
asset_path = get_asset_path("assets/images/characters/danger.png")
```

## Debugging Asset Loading

### Verbose Asset Loading
```python
def load_image_debug(path: str) -> pygame.Surface:
    print(f"Loading image: {path}")
    if not os.path.exists(path):
        print(f"Asset missing: {path} - using placeholder")
    # ... rest of loading logic
```
