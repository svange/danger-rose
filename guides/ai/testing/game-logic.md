# Game Logic Testing

Testing gameplay mechanics, collision detection, and scoring for reliable family-friendly gameplay.

## Player Movement Testing

```python
import pytest
from src.entities.player import Player
from src.config.constants import PLAYER_SPEED

def test_player_basic_movement():
    """Test player responds to movement input correctly."""
    player = Player(400, 300, "danger")
    
    # Test horizontal movement
    player.move_right = True
    player.update(dt=1.0, boundaries=[])
    assert player.x > 400  # Moved right
    
    player.move_right = False
    player.move_left = True  
    player.update(dt=1.0, boundaries=[])
    assert player.x < 400  # Moved left

def test_diagonal_movement_normalization():
    """Test diagonal movement isn't faster than cardinal movement."""
    player = Player(400, 300, "danger")
    
    # Test pure horizontal movement
    player.move_right = True
    player.update(dt=1.0, boundaries=[])
    horizontal_distance = abs(player.x - 400)
    
    # Reset position
    player.x = 400
    
    # Test diagonal movement
    player.move_right = True
    player.move_up = True
    player.update(dt=1.0, boundaries=[])
    diagonal_distance = abs(player.x - 400)
    
    # Diagonal should be normalized (slower than pure horizontal)
    assert diagonal_distance < horizontal_distance
```

## Collision Detection Testing

```python
def test_boundary_collision():
    """Test player stops at boundaries correctly."""
    player = Player(100, 300, "danger")
    
    # Create wall boundary
    wall = pygame.Rect(150, 0, 50, 600)
    boundaries = [wall]
    
    # Try to move into wall
    player.move_right = True
    original_x = player.x
    player.update(dt=1.0, boundaries=boundaries)
    
    # Should not move past boundary
    assert player.x <= wall.left

def test_obstacle_collision():
    """Test collision with game obstacles."""
    from src.entities.snowflake import SnowflakeEffect
    
    player = Player(400, 300, "danger")
    obstacle = SnowflakeEffect(400, 300, speed=100)
    
    # Test collision detection
    collision = player.rect.colliderect(obstacle.rect)
    
    if collision:
        # Test collision response
        initial_lives = player.lives if hasattr(player, 'lives') else 3
        player.handle_collision_with_obstacle(obstacle)
        
        # Player should become invincible
        assert player.invincible == True
```

## Scoring System Testing

```python
def test_score_increment():
    """Test scoring increases correctly when collecting items."""
    from src.scenes.ski import SkiScene
    
    scene = SkiScene()
    initial_score = scene.score
    
    # Simulate collecting a snowflake
    from src.entities.snowflake import SnowflakeEffect
    snowflake = SnowflakeEffect(400, 300, speed=100)
    scene._handle_snowflake_collection(snowflake)
    
    assert scene.score > initial_score
    assert scene.score == initial_score + snowflake.points

def test_lives_system():
    """Test player lives decrease on damage and game over at zero."""
    from src.scenes.ski import SkiScene
    
    scene = SkiScene()
    scene.lives = 1  # Set to 1 life
    
    # Simulate collision that causes damage
    scene._handle_obstacle_collision()
    
    assert scene.lives == 0
    assert scene.game_over == True
```

## Game State Management Testing

```python
def test_game_timer():
    """Test game timer counts down correctly."""
    from src.scenes.pool import PoolScene
    
    scene = PoolScene()
    initial_time = scene.game_time
    
    # Update scene with time delta
    scene.update(dt=1.0)  # 1 second
    
    assert scene.game_time == initial_time + 1.0

def test_pause_functionality():
    """Test game can be paused and unpaused."""
    from src.scenes.pause_menu import PauseMenuScene
    from src.scene_manager import SceneManager
    
    manager = SceneManager()
    pause_scene = PauseMenuScene()
    
    # Test pause
    manager.push_scene("pause", pause_scene)
    assert manager.scene_stack[-1] == pause_scene
    
    # Test unpause  
    manager.pop_scene()
    assert manager.scene_stack[-1] != pause_scene
```

## Minigame-Specific Logic Testing

```python
def test_ski_slope_generation():
    """Test ski slope generates obstacles correctly."""
    from src.scenes.slope_generator import SlopeGenerator
    
    generator = SlopeGenerator()
    obstacles = generator.generate_slope_section(y_position=0, width=800)
    
    # Should generate some obstacles
    assert len(obstacles) > 0
    
    # Obstacles should be within screen bounds
    for obstacle in obstacles:
        assert 0 <= obstacle.x <= 800
        assert obstacle.y >= 0

def test_pool_target_spawning():
    """Test pool game spawns targets at correct intervals."""
    from src.scenes.pool import PoolScene
    
    scene = PoolScene()
    initial_target_count = len(scene.targets)
    
    # Simulate time passing for target spawn
    scene.last_target_spawn = 0  # Reset spawn timer
    scene.update(dt=5.0)  # 5 seconds
    
    # Should have spawned new targets
    assert len(scene.targets) > initial_target_count

def test_vegas_boss_behavior():
    """Test Vegas boss follows expected behavior patterns."""
    from src.entities.vegas_boss import VegasBoss
    
    boss = VegasBoss(400, 200)
    initial_x = boss.x
    
    # Test movement pattern
    boss.update(dt=1.0)
    
    # Boss should move (not static)
    assert boss.x != initial_x
    
    # Test attack pattern
    if hasattr(boss, 'can_attack'):
        boss.last_attack_time = 0  # Reset attack timer
        boss.update(dt=3.0)  # Trigger attack
        assert boss.last_attack_time > 0
```

## Save/Load System Testing

```python
def test_game_state_persistence():
    """Test game state saves and loads correctly."""
    from src.utils.save_manager import SaveManager
    
    save_manager = SaveManager()
    
    # Create test game state
    test_state = {
        "score": 1500,
        "level": "ski",
        "character": "danger",
        "completed_games": ["pool"]
    }
    
    # Save and load
    save_manager.save_game_state(test_state)
    loaded_state = save_manager.load_game_state()
    
    # Verify data integrity
    assert loaded_state["score"] == test_state["score"]
    assert loaded_state["character"] == test_state["character"]
    assert "pool" in loaded_state["completed_games"]

def test_high_score_tracking():
    """Test high scores are tracked and sorted correctly."""
    from src.utils.high_score_manager import HighScoreManager
    
    score_manager = HighScoreManager()
    
    # Add test scores
    score_manager.add_score("ski", "TestPlayer", 1000)
    score_manager.add_score("ski", "TestPlayer2", 1500)
    score_manager.add_score("ski", "TestPlayer3", 800)
    
    # Get high scores for ski game
    high_scores = score_manager.get_high_scores("ski")
    
    # Should be sorted by score (highest first)
    assert high_scores[0]["score"] >= high_scores[1]["score"]
    assert high_scores[1]["score"] >= high_scores[2]["score"]
```