"""Unit tests for AttackCharacter class.

Tests sprite animation system with proper mocking of pygame and time functions.
"""

from unittest.mock import Mock, patch
import pygame

from src.utils.attack_character import AttackCharacter


class TestAttackCharacterInitialization:
    """Tests for AttackCharacter initialization."""

    @patch("src.utils.attack_character.pygame.image.load")
    @patch("src.utils.attack_character.pygame.display.get_surface")
    @patch("src.utils.attack_character.pygame.Surface")
    @patch("src.utils.attack_character.pygame.transform.scale")
    def test_init_with_valid_sprite_path(
        self, mock_scale, mock_surface_class, mock_get_surface, mock_load
    ):
        """AttackCharacter should initialize with valid sprite path."""
        # Arrange
        mock_get_surface.return_value = None  # No display
        mock_sheet = Mock()
        mock_sheet.convert.return_value = mock_sheet
        mock_sheet.get_width.return_value = 1024
        mock_sheet.get_height.return_value = 1024
        mock_load.return_value = mock_sheet

        # Mock frame creation
        mock_frames = [Mock() for _ in range(3)]
        mock_scaled_frames = [Mock() for _ in range(3)]
        mock_surface_class.side_effect = mock_frames
        mock_scale.side_effect = mock_scaled_frames

        # Act
        character = AttackCharacter("test_char", "test.png", (128, 128))

        # Assert
        assert character.character_name == "test_char"
        assert character.scale == (128, 128)
        assert character.current_frame == 0
        assert character.animation_speed == 0.3
        assert len(character.attack_frames) == 3  # 3 attack frames

    @patch("src.utils.attack_character.pygame.Surface")
    def test_init_with_empty_sprite_path(self, mock_surface_class):
        """AttackCharacter should create placeholder when sprite path is empty."""
        # Arrange
        mock_placeholder = Mock()
        mock_surface_class.return_value = mock_placeholder

        # Act
        character = AttackCharacter("test_char", "", (64, 64))

        # Assert
        assert len(character.attack_frames) == 3
        assert all(frame == mock_placeholder for frame in character.attack_frames)
        mock_placeholder.fill.assert_called_with((255, 0, 255))

    @patch("src.utils.attack_character.pygame.image.load")
    @patch("src.utils.attack_character.pygame.Surface")
    def test_init_handles_pygame_error(self, mock_surface_class, mock_load):
        """AttackCharacter should handle pygame loading errors gracefully."""
        # Arrange
        mock_load.side_effect = pygame.error("Load failed")
        mock_placeholder = Mock()
        mock_surface_class.return_value = mock_placeholder

        # Act
        character = AttackCharacter("test_char", "corrupt.png", (64, 64))

        # Assert
        assert len(character.attack_frames) == 3
        mock_placeholder.fill.assert_called_with((255, 0, 255))


class TestAttackFrameLoading:
    """Tests for attack frame loading logic."""

    @patch("src.utils.attack_character.pygame.image.load")
    @patch("src.utils.attack_character.pygame.display.get_surface")
    @patch("src.utils.attack_character.pygame.Surface")
    def test_load_attack_frames_extracts_correct_row(
        self, mock_surface_class, mock_get_surface, mock_load
    ):
        """_load_attack_frames should extract frames from row 2 with offset."""
        # Arrange
        mock_get_surface.return_value = Mock()  # Has display
        mock_sheet = Mock()
        mock_sheet.convert_alpha.return_value = mock_sheet
        mock_sheet.get_width.return_value = 1024
        mock_sheet.get_height.return_value = 1024
        mock_load.return_value = mock_sheet

        # Create 3 mock frames
        mock_frames = [Mock() for _ in range(3)]
        mock_surface_class.side_effect = mock_frames

        # Act
        AttackCharacter("test_char", "test.png", scale=None)

        # Assert
        # Verify the correct y position with offset (row 2 * 341 - 113 = 569)
        expected_y = 569  # 682 - 113
        for i in range(3):
            expected_x = i * 256
            mock_frames[i].blit.assert_called_once_with(
                mock_sheet, (0, 0), (expected_x, expected_y, 256, 341)
            )

    @patch("src.utils.attack_character.pygame.image.load")
    @patch("src.utils.attack_character.pygame.display.get_surface")
    @patch("src.utils.attack_character.pygame.Surface")
    @patch("src.utils.attack_character.pygame.transform.scale")
    def test_load_attack_frames_with_scaling(
        self, mock_scale, mock_surface_class, mock_get_surface, mock_load
    ):
        """_load_attack_frames should scale frames when scale is provided."""
        # Arrange
        mock_get_surface.return_value = None
        mock_sheet = Mock()
        mock_sheet.convert.return_value = mock_sheet
        mock_sheet.get_width.return_value = 1024
        mock_sheet.get_height.return_value = 1024
        mock_load.return_value = mock_sheet

        mock_frames = [Mock() for _ in range(3)]
        mock_scaled_frames = [Mock() for _ in range(3)]
        mock_surface_class.side_effect = mock_frames
        mock_scale.side_effect = mock_scaled_frames

        # Act
        character = AttackCharacter("test_char", "test.png", (64, 64))

        # Assert
        assert character.attack_frames == mock_scaled_frames
        assert mock_scale.call_count == 3


class TestAnimationUpdate:
    """Tests for animation update logic."""

    @patch("src.utils.attack_character.time.time")
    @patch("src.utils.attack_character.pygame.Surface")
    def test_update_advances_frame_after_animation_speed(
        self, mock_surface_class, mock_time
    ):
        """update should advance frame when enough time has passed."""
        # Arrange
        mock_surface_class.return_value = Mock()

        # Mock time for initialization and update
        mock_time.return_value = 0.0  # Initial time
        character = AttackCharacter("test_char", "", (64, 64))

        # Reset for test
        character.last_frame_time = 0.0
        character.current_frame = 0

        # Set time to trigger frame advance (0.3 seconds later)
        mock_time.return_value = 0.5

        # Act
        character.update()

        # Assert
        assert character.current_frame == 1
        assert character.last_frame_time == 0.5

    @patch("src.utils.attack_character.time.time")
    @patch("src.utils.attack_character.pygame.Surface")
    def test_update_wraps_around_at_end(self, mock_surface_class, mock_time):
        """update should wrap frame counter back to 0 after last frame."""
        # Arrange
        mock_surface_class.return_value = Mock()

        # Mock time for initialization
        mock_time.return_value = 0.0
        character = AttackCharacter("test_char", "", (64, 64))

        # Set up at last frame
        character.current_frame = 2  # Last frame (0-indexed)
        character.last_frame_time = 0.0

        # Set time to trigger frame advance
        mock_time.return_value = 0.5

        # Act
        character.update()

        # Assert
        assert character.current_frame == 0  # Wrapped around

    @patch("src.utils.attack_character.time.time")
    @patch("src.utils.attack_character.pygame.Surface")
    def test_update_does_not_advance_before_animation_speed(
        self, mock_surface_class, mock_time
    ):
        """update should not advance frame before animation_speed time has passed."""
        # Arrange
        mock_surface_class.return_value = Mock()

        # Mock time for initialization
        mock_time.return_value = 0.0
        character = AttackCharacter("test_char", "", (64, 64))

        # Reset for test
        character.last_frame_time = 0.0
        character.current_frame = 0

        # Set time to NOT trigger frame advance (only 0.1 seconds later)
        mock_time.return_value = 0.1

        # Act
        character.update()

        # Assert
        assert character.current_frame == 0  # No change
        assert character.last_frame_time == 0.0  # Not updated


class TestSpriteRetrieval:
    """Tests for getting current sprite."""

    @patch("src.utils.attack_character.pygame.Surface")
    def test_get_current_sprite_returns_correct_frame(self, mock_surface_class):
        """get_current_sprite should return the current animation frame."""
        # Arrange
        mock_frames = [Mock() for _ in range(3)]
        character = AttackCharacter("test_char", "", (64, 64))
        character.attack_frames = mock_frames
        character.current_frame = 1

        # Act
        result = character.get_current_sprite()

        # Assert
        assert result == mock_frames[1]

    @patch("src.utils.attack_character.pygame.Surface")
    def test_get_current_sprite_handles_invalid_frame_index(self, mock_surface_class):
        """get_current_sprite should return fallback for invalid frame index."""
        # Arrange
        mock_fallback = Mock()
        mock_surface_class.return_value = mock_fallback
        character = AttackCharacter("test_char", "", (64, 64))
        character.current_frame = 999  # Invalid index

        # Act
        result = character.get_current_sprite()

        # Assert
        assert result == mock_fallback
        mock_fallback.fill.assert_called_with((255, 0, 255))

    @patch("src.utils.attack_character.pygame.Surface")
    def test_get_current_sprite_handles_empty_frames(self, mock_surface_class):
        """get_current_sprite should return fallback when no frames loaded."""
        # Arrange
        mock_fallback = Mock()
        mock_surface_class.return_value = mock_fallback
        character = AttackCharacter("test_char", "", (64, 64))
        character.attack_frames = []  # No frames

        # Act
        result = character.get_current_sprite()

        # Assert
        assert result == mock_fallback
        mock_fallback.fill.assert_called_with((255, 0, 255))


class TestUtilityMethods:
    """Tests for utility methods."""

    @patch("src.utils.attack_character.pygame.Surface")
    def test_get_frame_count(self, mock_surface_class):
        """get_frame_count should return number of attack frames."""
        # Arrange
        mock_surface_class.return_value = Mock()
        character = AttackCharacter("test_char", "", (64, 64))

        # Act
        result = character.get_frame_count()

        # Assert
        assert result == 3

    @patch("src.utils.attack_character.pygame.Surface")
    def test_get_animation_info(self, mock_surface_class):
        """get_animation_info should return formatted string with current frame info."""
        # Arrange
        mock_surface_class.return_value = Mock()
        character = AttackCharacter("test_char", "", (64, 64))
        character.current_frame = 1

        # Act
        result = character.get_animation_info()

        # Assert
        assert result == "Attack (Frame 2/3)"  # 1-indexed for display
