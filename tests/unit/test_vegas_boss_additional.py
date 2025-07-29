"""Additional tests for Vegas boss to improve coverage."""

import pygame
import pytest
from unittest.mock import Mock
from src.entities.vegas_boss import VegasBoss, BossPhase, Projectile


class TestVegasBossAdditional:
    """Additional Vegas boss tests for coverage."""

    @pytest.fixture
    def boss(self):
        """Create a boss instance for testing."""
        pygame.init()
        return VegasBoss(640, 300)

    def test_boss_update_rect(self, boss):
        """Test boss rect update method."""
        boss.x = 500
        boss.y = 400
        boss.update_rect()

        assert boss.rect.centerx == 500
        assert boss.rect.centery == 400

    def test_projectile_draw(self):
        """Test projectile drawing."""
        proj = Projectile(100, 100, 0, 0, (255, 0, 0))
        mock_screen = Mock()

        # Active projectile should draw
        proj.draw(mock_screen, 0)
        mock_screen.blit.assert_called()

        # Inactive projectile should not draw
        proj.active = False
        mock_screen.reset_mock()
        proj.draw(mock_screen, 0)
        mock_screen.blit.assert_not_called()

    def test_boss_phase_transition_effects(self, boss):
        """Test phase transition visual effects."""
        boss.transitioning = True
        boss.phase_transition_time = 0.5

        boss.update(0.1, 500, 400)

        # Scale should change during transition
        assert boss.scale != 1.0

    def test_boss_particle_cleanup(self, boss):
        """Test particle system cleanup."""
        # Add some particles
        for i in range(5):
            boss.particles.append(
                {
                    "x": 100,
                    "y": 100,
                    "vx": 10,
                    "vy": -10,
                    "lifetime": i * 0.3,
                    "color": (255, 0, 0),
                }
            )

        # Update to clean old particles
        boss.update(0.1, 500, 400)

        # Particles with lifetime > 1.0 should be removed
        assert len(boss.particles) < 5

    def test_boss_draw_with_effects(self, boss):
        """Test boss drawing with various effects."""
        mock_screen = Mock()

        # Test with hit flash
        boss.hit_flash_timer = 0.2
        boss.draw(mock_screen, 0)

        # Test when invulnerable
        boss.invulnerable = True
        boss.draw(mock_screen, 0)

        # Test when defeated and off screen
        boss.phase = BossPhase.DEFEATED
        boss.y = 900
        mock_screen.reset_mock()
        boss.draw(mock_screen, 0)
        # Should not draw when fallen off screen
        mock_screen.blit.assert_not_called()

    def test_projectile_lifetime(self):
        """Test projectile deactivation by lifetime."""
        proj = Projectile(100, 100, 0, 0, (255, 0, 0))
        proj.lifetime = 11  # Over max lifetime

        proj.update(0.1)

        assert not proj.active

    def test_boss_movement_phase_specific(self, boss):
        """Test phase-specific movement patterns."""
        # Test phase 1 movement
        boss.phase = BossPhase.PHASE_1_HAPPY
        initial_x = boss.x
        boss.update_movement(0.1, 500)
        # Should have gentle movement
        assert abs(boss.x - initial_x) < 10

        # Test phase 3 chaotic movement
        boss.phase = BossPhase.PHASE_3_DIZZY
        boss.float_time = 0
        boss.update_movement(0.1, 500)
        # Rotation should increase significantly
        assert boss.rotation > 0
