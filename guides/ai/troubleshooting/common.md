# Common Issues & Solutions

## Game Won't Start

### ImportError: No module named 'pygame'
```bash
# Solution: Install dependencies
poetry install
# Or directly: pip install pygame
```

### Scene Not Found Error
```python
# Error: KeyError: 'scene_name' in SceneManager
# Solution: Check scene registration
scenes = {
    "title": TitleScreen(),
    "hub": HubWorld(),     # Must match exact name
    "ski": SkiGame()
}
```

### Asset Loading Failures
```bash
# Check assets exist
make assets-check
# Regenerate missing assets
make sprites
```

## Performance Issues

### Low FPS in Hub World
```python
# Check collision detection optimization
boundaries = []  # Pre-calculate boundaries
for door in doors:
    boundaries.append(door.rect)
```

### Memory Leaks
```python
# Ensure proper cleanup in scenes
def on_exit(self) -> dict:
    # Clean up sprites
    self.entities.empty()
    # Clean up surfaces
    if hasattr(self, 'background'):
        del self.background
    return {}
```

## Character Animation Issues

### Sprites Not Loading
```python
# Check character name spelling
character = AnimatedCharacter(
    "danger",  # Must match folder name exactly
    "hub",     # Must match scene name
    scale=(128, 128)
)
```

### Animation Not Playing
```python
# Verify animation state setting
self.sprite.set_animation("walk", loop=True)
self.sprite.update()  # Must call update() each frame
```

## Scene Transition Problems

### Black Screen After Transition
```python
# Ensure on_enter is implemented
def on_enter(self, previous_scene: str, data: dict):
    self.initialized = True  # Add initialization flag
    
def draw(self, screen):
    if not hasattr(self, 'initialized'):
        return  # Don't draw until initialized
```

### Data Not Passing Between Scenes
```python
# Proper data passing
def on_exit(self) -> dict:
    return {
        "character": self.selected_character,
        "score": self.score
    }
    
def on_enter(self, previous_scene: str, data: dict):
    self.character = data.get("character", "danger")
```

## Audio Issues

### No Sound Playing
```bash
# Check audio files exist
ls assets/audio/music/
ls assets/audio/sfx/

# Test audio system
make run
# Look for audio initialization messages
```

### Audio Cutting Out
```python
# Increase mixer buffer size
pygame.mixer.pre_init(
    frequency=22050,
    size=-16,
    channels=2,
    buffer=1024  # Increase if audio cuts out
)
```