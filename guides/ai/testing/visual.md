# Visual Testing for Sprites and Animations

Testing patterns for sprites, animations, and rendering in family-friendly games.

## Sprite Animation Testing

```python
import pytest
from src.utils.animated_character import AnimatedCharacter
from src.utils.sprite_loader import load_character_animations

def test_character_animation_frames():
    """Test that character animations load correct frame counts."""
    character = AnimatedCharacter("danger", "assets/images/characters/danger.png")

    # Verify expected animations exist
    expected_animations = ["walking", "jumping", "attacking", "idle"]
    for animation in expected_animations:
        assert animation in character.animations
        assert len(character.animations[animation]) > 0

    # Test frame progression
    character.set_animation("walking")
    initial_frame = character.current_frame
    character.update()  # Should advance frame
    assert character.current_frame != initial_frame or len(character.animations["walking"]) == 1

def test_sprite_flipping():
    """Test character sprite direction changes."""
    character = AnimatedCharacter("danger", "assets/images/characters/danger.png")

    # Test initial state
    original_frame = character.get_current_frame()

    # Test horizontal flip
    flipped_frame = pygame.transform.flip(original_frame, True, False)
    assert flipped_frame.get_size() == original_frame.get_size()
    assert flipped_frame != original_frame  # Should be different after flip
```

## Visual Regression Testing

```python
def test_scene_rendering(tmpdir):
    """Test that scenes render without visual artifacts."""
    from src.scenes.hub import HubScene

    # Create test screen
    test_screen = pygame.Surface((800, 600))
    scene = HubScene()

    # Render scene
    scene.draw(test_screen)

    # Save reference image for comparison
    reference_path = tmpdir.join("hub_scene_reference.png")
    pygame.image.save(test_screen, str(reference_path))

    # Verify image was created and has content
    assert reference_path.exists()
    assert reference_path.size() > 1000  # Non-empty image

def test_ui_element_positioning():
    """Test UI elements appear in correct screen positions."""
    from src.ui.drawing_helpers import draw_text_with_background

    screen = pygame.Surface((800, 600))
    font = pygame.font.Font(None, 36)

    # Test centered text
    draw_text_with_background(
        screen, "Test Text", font, (400, 300),
        text_color=(0, 0, 0), bg_color=(255, 255, 255)
    )

    # Check that pixels were modified around center
    center_color = screen.get_at((400, 300))
    assert center_color != (0, 0, 0)  # Should not be black (default)
```

## Animation State Testing

```python
def test_player_animation_states():
    """Test player animation changes based on movement."""
    from src.entities.player import Player

    player = Player(400, 300, "danger")

    # Test idle state
    player.vx = player.vy = 0
    player._update_animation()
    assert player.current_state == "idle"

    # Test walking state
    player.vx = 5.0
    player._update_animation()
    assert player.current_state == "walking"

    # Test jumping state
    player.is_jumping = True
    player._update_animation()
    assert player.current_state == "jumping"

def test_animation_timing():
    """Test animation frame timing consistency."""
    character = AnimatedCharacter("danger", "assets/images/characters/danger.png")
    character.set_animation("walking")

    # Record frame changes over time
    frame_changes = []
    for i in range(100):  # Simulate 100 update cycles
        old_frame = character.current_frame
        character.update()
        if character.current_frame != old_frame:
            frame_changes.append(i)

    # Should have regular frame changes
    assert len(frame_changes) > 0
    if len(frame_changes) > 1:
        # Check timing consistency
        intervals = [frame_changes[i+1] - frame_changes[i] for i in range(len(frame_changes)-1)]
        avg_interval = sum(intervals) / len(intervals)
        assert all(abs(interval - avg_interval) < 5 for interval in intervals)
```

## Color and Visual Effects Testing

```python
def test_invincibility_flashing():
    """Test visual feedback for player invincibility."""
    from src.entities.player import Player

    player = Player(400, 300, "danger")
    player.make_invincible(2.0)  # 2 second invincibility

    screen = pygame.Surface((800, 600))

    # Test that player sometimes doesn't draw (flashing effect)
    draws = []
    for i in range(20):
        screen.fill((0, 0, 0))  # Clear screen
        player.draw(screen)

        # Check if anything was drawn (non-black pixels)
        drawn = any(screen.get_at((x, y)) != (0, 0, 0)
                   for x in range(390, 410)
                   for y in range(290, 310))
        draws.append(drawn)

        # Advance time slightly
        player.invincible_timer -= 0.1

    # Should have mix of drawn and not drawn frames
    assert True in draws and False in draws

def test_collision_visual_feedback():
    """Test visual effects appear during collisions."""
    from src.effects.trophy_particles import TrophyParticles

    effect = TrophyParticles(400, 300, "gold")
    screen = pygame.Surface((800, 600))

    # Test initial particle count
    initial_count = len(effect.particles)
    assert initial_count > 0

    # Update and draw particles
    effect.update(0.1)
    effect.draw(screen)

    # Verify particles are being rendered
    particle_pixels = sum(1 for x in range(800) for y in range(600)
                         if screen.get_at((x, y)) != (0, 0, 0))
    assert particle_pixels > 0
```

## Performance Visual Testing

```python
def test_sprite_loading_performance():
    """Test sprite loading doesn't cause visual delays."""
    import time
    from src.utils.sprite_loader import load_character_animations

    start_time = time.time()
    animations = load_character_animations("assets/images/characters/danger.png")
    load_time = time.time() - start_time

    # Loading should be fast enough for smooth gameplay
    assert load_time < 0.5  # Less than 500ms
    assert animations is not None
    assert len(animations) > 0

def test_scene_draw_performance():
    """Test scene drawing performance for smooth framerate."""
    from src.scenes.ski import SkiScene

    scene = SkiScene()
    screen = pygame.Surface((800, 600))

    # Measure multiple draw calls
    draw_times = []
    for _ in range(10):
        start_time = time.time()
        scene.draw(screen)
        draw_time = time.time() - start_time
        draw_times.append(draw_time)

    avg_draw_time = sum(draw_times) / len(draw_times)
    # Should draw fast enough for 60 FPS (16.67ms per frame)
    assert avg_draw_time < 0.016
```
