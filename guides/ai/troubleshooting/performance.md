# Performance Troubleshooting

## Measuring Performance

### Enable Debug Mode
```bash
make debug              # Shows FPS counter
DEBUG=true make run     # Environment variable
```

### Profile Game Performance
```bash
make profile           # Creates profile.stats
# Analyze with: python -m pstats profile.stats
```

## Common FPS Issues

### Target: 60 FPS
```python
# Check actual FPS
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000.0  # 60 FPS target
```

### Heavy Draw Operations
```python
# Optimize drawing in game loops
def draw(self, screen):
    # Use dirty rectangle updates
    dirty_rects = []
    for entity in self.entities:
        if entity.needs_redraw:
            dirty_rects.append(entity.rect)

    # Only update changed areas
    pygame.display.update(dirty_rects)
```

### Sprite Loading Bottlenecks
```python
# Pre-load sprites in __init__
class SkiGame(Scene):
    def __init__(self):
        # Load once, reuse many times
        self.tree_sprite = load_image("assets/images/tilesets/ski/tree.png")
        self.rock_sprite = load_image("assets/images/tilesets/ski/rock.png")
```

## Memory Optimization

### Monitor Memory Usage
```bash
MEMORY_DEBUG=true make run  # Enable memory debugging
```

### Large Sprite Sheets
```python
# Break down large assets
# Instead of 1024x1024 sheet, use individual frames
animations = load_character_individual_files(
    character_name="danger",
    scale=(128, 128)  # Scale down to reduce memory
)
```

### Entity Management
```python
# Remove off-screen entities
def update(self, dt):
    for obstacle in self.obstacles[:]:  # Copy list for safe removal
        if obstacle.y > SCREEN_HEIGHT + 100:
            self.obstacles.remove(obstacle)
            del obstacle  # Explicit cleanup
```

## Specific Scene Optimizations

### Ski Game Performance
```python
# Limit obstacle generation
MAX_OBSTACLES = 50
if len(self.obstacles) < MAX_OBSTACLES:
    self.generate_obstacle()

# Use sprite groups for batch operations
self.obstacles = pygame.sprite.Group()
self.obstacles.update(dt)  # Batch update
```

### Hub World Collision
```python
# Pre-calculate static collision boundaries
def __init__(self):
    self.static_boundaries = [
        pygame.Rect(0, 0, 50, SCREEN_HEIGHT),    # Left wall
        pygame.Rect(SCREEN_WIDTH-50, 0, 50, SCREEN_HEIGHT)  # Right wall
    ]
```

### Pool Game Water Effects
```python
# Limit particle count
MAX_PARTICLES = 100
if len(self.water_particles) > MAX_PARTICLES:
    # Remove oldest particles
    self.water_particles = self.water_particles[-MAX_PARTICLES:]
```

## Platform-Specific Issues

### Windows Performance
- Use fullscreen mode for better performance
- Disable Windows Game Mode if causing issues

### macOS Performance
- Check Retina display scaling
- May need to reduce sprite sizes

### Linux Performance
- Verify hardware acceleration enabled
- Check audio driver compatibility

## Debug Tools

### Visual Debug Info
```python
if DEBUG:
    # Show FPS
    fps_text = font.render(f"FPS: {clock.get_fps():.1f}", True, COLOR_WHITE)
    screen.blit(fps_text, (10, 10))

    # Show entity count
    count_text = font.render(f"Entities: {len(self.entities)}", True, COLOR_WHITE)
    screen.blit(count_text, (10, 30))
```
