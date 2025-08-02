# Asset Management in Builds

## Asset Structure

Danger Rose automatically includes all assets in builds:
```
assets/
├── audio/
│   ├── music/          # Background music (OGG format)
│   └── sfx/           # Sound effects
├── images/
│   ├── characters/    # Player sprites
│   ├── tilesets/      # Game backgrounds and objects
│   └── icons/         # UI elements
└── trophies/          # Achievement graphics
```

## Placeholder System

Missing assets are automatically handled:
```python
def load_image(path: str) -> pygame.Surface:
    if not os.path.exists(path):
        # Creates magenta placeholder
        surface = pygame.Surface((64, 64))
        surface.fill(COLOR_PLACEHOLDER)
        return surface
```

## Asset Validation

Before building, check assets:
```bash
make assets-check       # Validate all required assets
poetry run python tools/check_assets.py
```

## Build Asset Inclusion

PyInstaller spec automatically bundles:
```python
datas=[
    ('assets', 'assets'),           # All game assets
    ('src/config', 'src/config'),   # Configuration files
]
```

## Runtime Asset Loading

Assets load from bundled location:
```python
# Automatically detects if running from build or source
def get_asset_path(relative_path: str) -> str:
    if hasattr(sys, '_MEIPASS'):  # PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path
```

## Audio Asset Best Practices

- Use OGG format for cross-platform compatibility
- Keep file sizes reasonable (<5MB per file)
- Test audio on target platforms

## Image Asset Guidelines

- PNG format with transparency support
- Power-of-2 dimensions for better performance
- Sprite sheets: 1024x1024 max recommended
- Individual frames: 256x341 for characters

## Missing Asset Handling

Game continues with placeholders:
- Magenta squares for missing images
- Silent audio for missing sounds
- Logs warnings for debugging

## Build Size Optimization

Current asset sizes:
- Music: ~20MB total
- Images: ~10MB total
- Total build: ~80-120MB depending on platform
