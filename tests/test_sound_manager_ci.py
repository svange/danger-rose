"""Tests for SoundManager in CI environments without audio."""

import pygame
from unittest.mock import patch
from src.managers.sound_manager import SoundManager


class TestSoundManagerCI:
    """Test SoundManager handles missing audio gracefully."""

    def test_sound_manager_handles_no_audio_device(self):
        """Test SoundManager initializes without crashing when no audio device."""
        # Mock pygame.mixer.init to raise error
        with patch("pygame.mixer.init", side_effect=pygame.error("No audio device")):
            # Should not crash
            sm = SoundManager()
            assert sm is not None

    def test_sound_manager_methods_safe_without_mixer(self):
        """Test all methods handle uninitialized mixer gracefully."""
        # Mock get_init to return None (not initialized)
        with patch("pygame.mixer.get_init", return_value=None):
            sm = SoundManager()

            # These should all return safely without crashing
            sm.play_music("test.ogg")
            sm.stop_music()
            sm.pause_music()
            sm.unpause_music()
            result = sm.play_sfx("test.wav")
            assert result is None
            sm.duck_audio()
            sm.restore_audio_levels()

    def test_sound_manager_singleton(self):
        """Test SoundManager maintains singleton pattern."""
        sm1 = SoundManager()
        sm2 = SoundManager()
        assert sm1 is sm2

    def test_volume_methods(self):
        """Test volume methods work without mixer."""
        with patch("pygame.mixer.get_init", return_value=None):
            sm = SoundManager()

            # Should handle volume changes
            sm.set_master_volume(0.5)
            assert sm.master_volume == 0.5

            sm.set_music_volume(0.7)
            assert sm.music_volume == 0.7

            sm.set_sfx_volume(0.3)
            assert sm.sfx_volume == 0.3

            volumes = sm.get_volumes()
            assert volumes["master"] == 0.5
            assert volumes["music"] == 0.7
            assert volumes["sfx"] == 0.3
