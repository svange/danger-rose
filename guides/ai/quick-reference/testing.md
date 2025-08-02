# Testing Guide - Quick Reference

## Running Tests

```bash
# All tests
poetry run pytest

# Quick unit tests only
poetry run pytest tests/unit -v

# With coverage
poetry run pytest --cov=src --cov-report=html

# Specific test file
poetry run pytest tests/unit/test_player.py -v

# Run tests matching pattern
poetry run pytest -k "test_collision"
```

## Test Categories

```bash
# Unit tests (fast, isolated)
pytest -m unit

# Integration tests (multi-component)
pytest -m integration  

# Visual tests (requires display)
pytest -m visual

# Performance tests
pytest -m performance
```

## Writing Game Tests

### Basic Test Structure
```python
def test_player_movement():
    """Test player moves correctly with input"""
    player = Player(x=100, y=100)
    player.velocity_x = 5
    player.update(1.0)  # 1 second delta
    
    assert player.x == 105
    assert player.y == 100
```

### Testing Collisions
```python
def test_player_wall_collision():
    """Test player stops at walls"""
    player = Player(x=50, y=50)
    wall = pygame.Rect(100, 0, 20, 200)
    
    player.move_right(dt=1.0)
    player.check_collision(wall)
    
    assert player.x < 100  # Stopped before wall
```

### Testing Scene Transitions
```python
def test_door_interaction():
    """Test door takes player to new scene"""
    scene = HubWorld()
    door = scene.doors["ski"]
    
    next_scene = scene.handle_event(
        create_key_event(pygame.K_SPACE)
    )
    
    assert next_scene == "ski_game"
```

## Mock Patterns

### Mock Display
```python
@pytest.fixture
def mock_display(monkeypatch):
    """Mock pygame display for headless testing"""
    mock_screen = MagicMock()
    mock_screen.get_size.return_value = (1920, 1080)
    monkeypatch.setattr(
        "pygame.display.set_mode", 
        lambda *args: mock_screen
    )
    return mock_screen
```

### Mock Audio
```python
@pytest.fixture
def mock_audio(monkeypatch):
    """Disable audio for tests"""
    monkeypatch.setattr(
        "pygame.mixer.init", 
        lambda: None
    )
```

## Coverage Requirements

```bash
# Check coverage
make coverage

# Minimum coverage: 55%
# Target coverage: 70%+
# Exclude UI/rendering code from coverage
```

## Test Organization

```
tests/
├── unit/           # Fast, isolated tests
│   ├── test_player.py
│   ├── test_entities.py
│   └── test_utils.py
├── integration/    # Multi-component tests
│   ├── test_scene_flow.py
│   └── test_save_system.py
├── visual/         # Rendering tests
│   └── test_animations.py
└── conftest.py     # Shared fixtures
```

## Common Test Helpers

```python
# Create test events
def create_key_event(key, type=pygame.KEYDOWN):
    return pygame.event.Event(type, {"key": key})

# Create test sprite
def create_test_sprite(color=(255, 0, 0)):
    surface = pygame.Surface((64, 64))
    surface.fill(color)
    return surface

# Assert position roughly equal (floating point)
def assert_pos_equal(pos1, pos2, tolerance=0.1):
    assert abs(pos1[0] - pos2[0]) < tolerance
    assert abs(pos1[1] - pos2[1]) < tolerance
```
