"""Tests for the ski minigame scene."""

import pytest
import pygame
import time
from unittest.mock import Mock
from src.scenes.ski import SkiGame, SkiPlayer
from src.scene_manager import SceneManager
from src.config.constants import SCENE_HUB_WORLD


@pytest.fixture
def scene_manager():
    """Create a mock scene manager."""
    manager = Mock(spec=SceneManager)
    manager.screen_width = 800
    manager.screen_height = 600
    manager.game_data = {"selected_character": "Danger"}
    return manager


@pytest.fixture
def ski_game(scene_manager):
    """Create a ski game instance."""
    return SkiGame(scene_manager)


class TestSkiPlayer:
    """Test the SkiPlayer class."""

    def test_player_initialization(self):
        """Test player is created with correct initial values."""
        player = SkiPlayer(400, 300, "Danger")
        assert player.x == 400
        assert player.y == 300
        assert player.character_name == "Danger"
        assert player.speed == 5
        # Rect is initialized at x,y not centered
        assert player.rect.x == 400
        assert player.rect.y == 300

    def test_player_movement_left(self):
        """Test player moves left with arrow key."""
        player = SkiPlayer(400, 300, "Danger")

        # Create a mock keys dictionary
        keys = {
            pygame.K_LEFT: True,
            pygame.K_RIGHT: False,
            pygame.K_a: False,
            pygame.K_d: False,
        }

        # Mock pygame.key.get_pressed to return our dictionary
        mock_keys = Mock()
        mock_keys.__getitem__ = Mock(side_effect=lambda k: keys.get(k, False))

        # Move player
        player.handle_input(mock_keys, 800)
        assert player.x == 395  # 400 - 5

    def test_player_movement_right(self):
        """Test player moves right with arrow key."""
        player = SkiPlayer(400, 300, "Danger")

        # Create a mock keys dictionary
        keys = {
            pygame.K_RIGHT: True,
            pygame.K_LEFT: False,
            pygame.K_a: False,
            pygame.K_d: False,
        }

        # Mock pygame.key.get_pressed to return our dictionary
        mock_keys = Mock()
        mock_keys.__getitem__ = Mock(side_effect=lambda k: keys.get(k, False))

        # Move player
        player.handle_input(mock_keys, 800)
        assert player.x == 405  # 400 + 5

    def test_player_screen_boundaries(self):
        """Test player stays within screen boundaries."""
        player = SkiPlayer(50, 300, "Danger")

        # Try to move past left boundary
        keys = {
            pygame.K_LEFT: True,
            pygame.K_RIGHT: False,
            pygame.K_a: False,
            pygame.K_d: False,
        }

        # Mock pygame.key.get_pressed to return our dictionary
        mock_keys = Mock()
        mock_keys.__getitem__ = Mock(side_effect=lambda k: keys.get(k, False))

        # Move left multiple times
        for _ in range(20):
            player.handle_input(mock_keys, 800)

        assert player.x >= 32  # Should not go below minimum

        # Try to move past right boundary
        player.x = 750
        keys = {
            pygame.K_RIGHT: True,
            pygame.K_LEFT: False,
            pygame.K_a: False,
            pygame.K_d: False,
        }
        mock_keys = Mock()
        mock_keys.__getitem__ = Mock(side_effect=lambda k: keys.get(k, False))

        for _ in range(20):
            player.handle_input(mock_keys, 800)

        assert player.x <= 768  # Should not exceed maximum (800 - 32)


class TestSkiGame:
    """Test the SkiGame scene."""

    def test_game_initialization(self, ski_game):
        """Test ski game initializes correctly."""
        assert ski_game.state == SkiGame.STATE_READY
        assert ski_game.time_remaining == 60.0
        assert ski_game.game_duration == 60.0
        assert ski_game.start_time is None
        assert ski_game.player is not None
        assert ski_game.player.character_name == "Danger"

    def test_game_start(self, ski_game):
        """Test game transitions from ready to playing state."""
        # Simulate space key press in ready state
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_SPACE

        result = ski_game.handle_event(event)

        assert ski_game.state == SkiGame.STATE_PLAYING
        assert ski_game.start_time is not None
        assert result is None

    def test_escape_to_hub_from_ready(self, ski_game):
        """Test escape key returns to hub from ready state."""
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_ESCAPE

        result = ski_game.handle_event(event)

        assert result == SCENE_HUB_WORLD

    def test_escape_to_hub_from_playing(self, ski_game):
        """Test escape key returns to hub from playing state."""
        # Start the game first
        ski_game.start_game()

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_ESCAPE

        result = ski_game.handle_event(event)

        assert result == SCENE_HUB_WORLD

    def test_game_timer_countdown(self, ski_game):
        """Test game timer counts down during play."""
        ski_game.start_game()
        initial_time = ski_game.time_remaining

        # Simulate some time passing
        time.sleep(0.1)
        ski_game.update(0.1)

        assert ski_game.time_remaining < initial_time
        assert ski_game.state == SkiGame.STATE_PLAYING

    def test_game_over_when_time_expires(self, ski_game):
        """Test game transitions to game over when time runs out."""
        ski_game.start_game()

        # Manually set time to expired
        ski_game.start_time = time.time() - 61  # Started 61 seconds ago
        ski_game.update(0.016)  # One frame update

        assert ski_game.state == SkiGame.STATE_GAME_OVER
        assert ski_game.time_remaining == 0

    def test_game_reset(self, ski_game):
        """Test game resets properly."""
        # Start and modify game state
        ski_game.start_game()
        ski_game.scroll_offset = 100
        ski_game.player.x = 200

        # Reset the game
        ski_game.reset_game()

        assert ski_game.state == SkiGame.STATE_READY
        assert ski_game.time_remaining == 60.0
        assert ski_game.scroll_offset == 0
        assert ski_game.player.x == ski_game.screen_width // 2

    def test_restart_from_game_over(self, ski_game):
        """Test space key restarts game from game over state."""
        ski_game.state = SkiGame.STATE_GAME_OVER

        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_SPACE

        result = ski_game.handle_event(event)

        assert ski_game.state == SkiGame.STATE_READY
        assert result is None

    def test_on_enter_resets_game(self, ski_game):
        """Test entering scene resets game state."""
        # Modify game state
        ski_game.state = SkiGame.STATE_PLAYING
        ski_game.scroll_offset = 100

        # Enter the scene
        ski_game.on_enter(SCENE_HUB_WORLD, {})

        assert ski_game.state == SkiGame.STATE_READY
        assert ski_game.scroll_offset == 0

    def test_scrolling_updates(self, ski_game):
        """Test slope scrolling updates during gameplay."""
        ski_game.start_game()
        initial_offset = ski_game.scroll_offset

        # Update for one frame
        ski_game.update(0.016)  # 60 FPS frame time

        assert ski_game.scroll_offset > initial_offset

    def test_player_update_during_gameplay(self, ski_game):
        """Test player is updated during gameplay."""
        ski_game.start_game()

        # Mock pygame key state - return a dict-like object
        mock_keys = Mock()
        mock_keys.__getitem__ = Mock(return_value=False)
        pygame.key.get_pressed = Mock(return_value=mock_keys)

        # Mock player update to track if it was called
        ski_game.player.update = Mock()

        ski_game.update(0.016)

        ski_game.player.update.assert_called_once()
