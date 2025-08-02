# Performance Testing

FPS testing, memory profiling, and optimization for smooth family-friendly gameplay.

## Frame Rate Testing

```python
import time
import pytest
from src.scenes.hub import HubScene
from src.scene_manager import SceneManager

def test_scene_update_performance():
    """Test scene updates meet 60 FPS target."""
    scene = HubScene()
    
    # Measure update performance
    update_times = []
    for _ in range(100):
        start_time = time.perf_counter()
        scene.update(dt=0.016)  # 60 FPS delta time
        update_time = time.perf_counter() - start_time
        update_times.append(update_time)
    
    avg_update_time = sum(update_times) / len(update_times)
    max_update_time = max(update_times)
    
    # Should update in less than 16ms for 60 FPS
    assert avg_update_time < 0.016
    assert max_update_time < 0.020  # Allow some variance

def test_draw_performance():
    """Test scene drawing performance."""
    scene = HubScene()
    screen = pygame.Surface((800, 600))
    
    draw_times = []
    for _ in range(50):
        start_time = time.perf_counter()
        scene.draw(screen)
        draw_time = time.perf_counter() - start_time
        draw_times.append(draw_time)
    
    avg_draw_time = sum(draw_times) / len(draw_times)
    
    # Drawing should be fast
    assert avg_draw_time < 0.010  # 10ms max for drawing
```

## Memory Usage Testing

```python
import psutil
import gc

def test_memory_usage_stability():
    """Test memory usage remains stable during gameplay."""
    from src.scenes.ski import SkiScene
    
    # Force garbage collection
    gc.collect()
    process = psutil.Process()
    initial_memory = process.memory_info().rss
    
    # Simulate extended gameplay
    scene = SkiScene()
    for i in range(1000):
        scene.update(dt=0.016)
        
        # Periodically check memory
        if i % 100 == 0:
            current_memory = process.memory_info().rss
            memory_increase = current_memory - initial_memory
            
            # Memory increase should be reasonable (< 50MB)
            assert memory_increase < 50 * 1024 * 1024

def test_sprite_memory_efficiency():
    """Test sprite loading doesn't cause memory leaks."""
    from src.utils.sprite_loader import load_character_animations
    
    gc.collect()
    initial_objects = len(gc.get_objects())
    
    # Load and unload sprites multiple times
    for _ in range(10):
        animations = load_character_animations("assets/images/characters/danger.png")
        del animations
        gc.collect()
    
    final_objects = len(gc.get_objects())
    object_increase = final_objects - initial_objects
    
    # Should not accumulate many objects
    assert object_increase < 100
```

## Particle System Performance

```python
def test_particle_system_performance():
    """Test particle systems maintain performance with many particles."""
    from src.effects.trophy_particles import TrophyParticles
    
    # Create multiple particle systems
    particle_systems = []
    for i in range(10):
        particles = TrophyParticles(400 + i * 10, 300, "gold")
        particle_systems.append(particles)
    
    # Measure update performance
    start_time = time.perf_counter()
    for _ in range(100):
        for system in particle_systems:
            system.update(0.016)
    
    total_time = time.perf_counter() - start_time
    avg_time_per_update = total_time / 100
    
    # Should handle multiple particle systems efficiently
    assert avg_time_per_update < 0.005  # 5ms for all systems

def test_collision_detection_performance():
    """Test collision detection scales well with object count."""
    from src.entities.player import Player
    
    player = Player(400, 300, "danger")
    
    # Create many obstacles
    obstacles = []
    for i in range(100):
        obstacle = pygame.Rect(i * 8, 200, 10, 10)
        obstacles.append(obstacle)
    
    # Measure collision checking performance
    start_time = time.perf_counter()
    for _ in range(1000):
        collisions = [obs for obs in obstacles if player.rect.colliderect(obs)]
    
    total_time = time.perf_counter() - start_time
    assert total_time < 0.1  # Should be very fast
```

## Audio Performance Testing

```python
def test_audio_loading_performance():
    """Test audio files load efficiently."""
    from src.managers.sound_manager import SoundManager
    
    sound_manager = SoundManager()
    
    # Test music loading time
    start_time = time.perf_counter()
    sound_manager.load_music("assets/audio/music/hub_theme.ogg")
    music_load_time = time.perf_counter() - start_time
    
    assert music_load_time < 0.5  # Should load quickly
    
    # Test sound effect loading
    sounds_to_test = ["jump.ogg", "collect_item.ogg", "collision.ogg"]
    
    start_time = time.perf_counter()
    for sound in sounds_to_test:
        sound_manager.load_sound(f"assets/audio/sfx/{sound}")
    
    sfx_load_time = time.perf_counter() - start_time
    assert sfx_load_time < 1.0  # All SFX should load in 1 second

def test_concurrent_audio_performance():
    """Test playing multiple sounds simultaneously."""
    from src.managers.sound_manager import SoundManager
    
    sound_manager = SoundManager()
    
    # Play multiple sounds at once
    start_time = time.perf_counter()
    for _ in range(5):
        sound_manager.play_sound("collect_item.ogg")
        sound_manager.play_sound("jump.ogg")
    
    play_time = time.perf_counter() - start_time
    assert play_time < 0.1  # Should handle concurrent playback
```

## Scene Transition Performance

```python
def test_scene_transition_performance():
    """Test scene transitions are smooth and fast."""
    from src.scene_manager import SceneManager
    from src.scenes.title_screen import TitleScreen
    from src.scenes.hub import HubScene
    
    manager = SceneManager()
    
    # Test transition timing
    start_time = time.perf_counter()
    
    title_scene = TitleScreen()
    hub_scene = HubScene()
    
    manager.change_scene("title", title_scene)
    manager.change_scene("hub", hub_scene)
    
    transition_time = time.perf_counter() - start_time
    
    # Scene changes should be nearly instantaneous
    assert transition_time < 0.1

def test_asset_preloading_efficiency():
    """Test asset preloading improves performance."""
    from src.utils.sprite_loader import preload_common_sprites
    
    # Measure without preloading
    start_time = time.perf_counter()
    sprite1 = pygame.image.load("assets/images/characters/danger.png")
    no_preload_time = time.perf_counter() - start_time
    
    # Preload assets
    preload_common_sprites()
    
    # Measure with preloading (should use cache)
    start_time = time.perf_counter()
    sprite2 = pygame.image.load("assets/images/characters/danger.png")
    preload_time = time.perf_counter() - start_time
    
    # Preloading should make subsequent loads faster
    assert preload_time <= no_preload_time
```

## Profiling Helpers

```python
def profile_scene_performance(scene_class, duration=5.0):
    """Profile a scene's performance over time."""
    import cProfile
    import pstats
    
    scene = scene_class()
    screen = pygame.Surface((800, 600))
    
    def run_scene():
        start_time = time.time()
        while time.time() - start_time < duration:
            scene.update(0.016)
            scene.draw(screen)
    
    # Profile the scene
    profiler = cProfile.Profile()
    profiler.enable()
    run_scene()
    profiler.disable()
    
    # Analyze results
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    
    # Return top time-consuming functions
    return stats.get_stats_profile()

def measure_fps_stability(scene_class, test_duration=10.0):
    """Measure FPS stability over time."""
    scene = scene_class()
    screen = pygame.Surface((800, 600))
    
    frame_times = []
    start_time = time.perf_counter()
    last_frame_time = start_time
    
    while time.perf_counter() - start_time < test_duration:
        scene.update(0.016)
        scene.draw(screen)
        
        current_time = time.perf_counter()
        frame_time = current_time - last_frame_time
        frame_times.append(frame_time)
        last_frame_time = current_time
    
    # Calculate FPS statistics
    avg_frame_time = sum(frame_times) / len(frame_times)
    avg_fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
    
    fps_variance = sum((1.0/ft - avg_fps)**2 for ft in frame_times if ft > 0) / len(frame_times)
    
    return {
        "average_fps": avg_fps,
        "fps_variance": fps_variance,
        "frame_count": len(frame_times)
    }
```