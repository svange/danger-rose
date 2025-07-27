"""Tests for the HubWorld scene."""

import pytest
import pygame
from unittest.mock import Mock, patch
from src.scenes.hub import HubWorld
from src.config.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class TestHubWorld:
    """Test suite for HubWorld scene."""

    @pytest.fixture
    def mock_scene_manager(self):
        """Create a mock scene manager."""
        manager = Mock()
        manager.game_data = {"selected_character": "danger"}
        manager.debug_mode = False
        return manager

    @pytest.fixture
    def hub_world(self, mock_scene_manager):
        """Create a HubWorld instance with mocked dependencies."""
        # Initialize pygame display for sprite loading
        pygame.init()
        pygame.display.set_mode((800, 600))
        
        with patch("pygame.font.Font"):
            with patch("pygame.image.load"):
                with patch("pygame.transform.scale"):
                    return HubWorld(mock_scene_manager)

    def test_initialization(self, hub_world, mock_scene_manager):
        """Test HubWorld initialization."""
        assert hub_world.scene_manager == mock_scene_manager
        assert hub_world.selected_character == "danger"
        assert hub_world.background is not None
        assert hub_world.player is not None
        assert hub_world.player.x == SCREEN_WIDTH // 2
        assert hub_world.player.y == SCREEN_HEIGHT // 2

    def test_boundaries_setup(self, hub_world):
        """Test that room boundaries are properly set up."""
        # Check boundaries exist
        assert len(hub_world.boundaries) == 4

        # Check door areas
        assert "ski" in hub_world.door_areas
        assert "pool" in hub_world.door_areas
        assert "vegas" in hub_world.door_areas

        # Check interactive areas
        assert hub_world.trophy_shelf_area is not None
        assert hub_world.couch_area is not None

    def test_player_movement_events(self, hub_world):
        """Test that movement events are passed to player."""
        # Test arrow key movement
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_LEFT
        
        hub_world.handle_event(event)
        assert hub_world.player.move_left is True
        
        # Test WASD movement
        event.key = pygame.K_d
        hub_world.handle_event(event)
        assert hub_world.player.move_right is True

    def test_handle_escape_key(self, hub_world):
        """Test escape key returns to settings."""
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_ESCAPE

        result = hub_world.handle_event(event)
        assert result == "settings"

    def test_handle_minigame_keys(self, hub_world):
        """Test number keys navigate to minigames."""
        # Test ski game
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_1
        assert hub_world.handle_event(event) == "ski"

        # Test pool game
        event.key = pygame.K_2
        assert hub_world.handle_event(event) == "pool"

        # Test vegas game
        event.key = pygame.K_3
        assert hub_world.handle_event(event) == "vegas"

    def test_handle_other_events(self, hub_world):
        """Test that other events return None."""
        # Mouse event
        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN
        assert hub_world.handle_event(event) is None

        # Other key
        event.type = pygame.KEYDOWN
        event.key = pygame.K_SPACE
        assert hub_world.handle_event(event) is None

    def test_update_method(self, hub_world):
        """Test update method exists and runs without error."""
        # Should not raise any exceptions
        hub_world.update(0.016)  # 60 FPS frame time
        
    def test_player_update_with_collision(self, hub_world):
        """Test that player update is called with boundaries."""
        # Mock the player update method
        hub_world.player.update = Mock()
        
        hub_world.update(0.016)
        
        # Verify player.update was called with correct arguments
        hub_world.player.update.assert_called_once_with(0.016, hub_world.boundaries)

    def test_draw_method(self, hub_world):
        """Test draw method renders without error."""
        mock_screen = Mock()
        mock_screen.blit = Mock()
        
        # Mock player draw method
        hub_world.player.draw = Mock()

        # Should not raise any exceptions
        hub_world.draw(mock_screen)

        # Check that background was drawn
        mock_screen.blit.assert_called()
        
        # Check that player was drawn
        hub_world.player.draw.assert_called_once_with(mock_screen)

    def test_on_enter_from_character_select(self, hub_world, mock_scene_manager):
        """Test entering hub from character select updates character."""
        data = {"selected_character": "rose"}
        hub_world.on_enter("character_select", data)

        assert hub_world.selected_character == "rose"
        assert mock_scene_manager.game_data["selected_character"] == "rose"
        
        # Check that player was recreated with new character
        assert hub_world.player is not None
        assert hub_world.player.sprite.character_name == "rose"

    def test_on_enter_from_other_scene(self, hub_world):
        """Test entering hub from other scenes."""
        original_character = hub_world.selected_character
        hub_world.on_enter("settings", {})

        # Character should not change
        assert hub_world.selected_character == original_character

    def test_on_exit(self, hub_world):
        """Test on_exit returns proper data."""
        data = hub_world.on_exit()
        assert data == {"from_scene": "hub"}

    def test_debug_mode_rendering(self, hub_world, mock_scene_manager):
        """Test that debug mode shows door areas."""
        mock_scene_manager.debug_mode = True
        mock_screen = Mock()
        mock_screen.blit = Mock()

        with patch("pygame.draw.rect") as mock_draw_rect:
            hub_world.draw(mock_screen)

            # Should draw rectangles for door areas
            assert mock_draw_rect.called

    def test_background_fallback(self, mock_scene_manager):
        """Test background creation when image load fails."""
        with patch("pygame.font.Font"):
            with patch("pygame.image.load", side_effect=pygame.error):
                with patch("pygame.Surface") as mock_surface:
                    hub = HubWorld(mock_scene_manager)

                    # Should create a fallback surface
                    mock_surface.assert_called_with((SCREEN_WIDTH, SCREEN_HEIGHT))
                    assert hub.background is not None
