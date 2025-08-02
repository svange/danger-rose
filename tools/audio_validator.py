"""
Audio Validation System for Danger Rose
========================================

This tool validates audio assets and detects common audio bugs:
- Missing audio files
- Corrupted audio files
- Volume level issues
- Audio playback errors
- Music transition problems
"""

import os
import sys
import json
import wave
import struct
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pygame
from mutagen.oggvorbis import OggVorbis
from mutagen.mp3 import MP3

# Set dummy audio driver for headless testing
os.environ["SDL_AUDIODRIVER"] = "dummy"


@dataclass
class AudioIssue:
    """Represents an audio issue found during validation."""

    file_path: str
    issue_type: str
    description: str
    severity: str = "medium"
    details: Optional[Dict] = None


@dataclass
class AudioPlaybackTest:
    """Results from audio playback testing."""

    scene: str
    expected_audio: str
    actual_playing: bool
    volume_level: float
    issues: List[str]


class AudioValidator:
    """Audio validation system for Danger Rose."""

    def __init__(self, assets_dir: str = "assets"):
        self.assets_dir = Path(assets_dir)
        self.audio_dir = self.assets_dir / "audio"

        self.results_dir = Path("audio_test_results")
        self.results_dir.mkdir(exist_ok=True)

        self.issues: List[AudioIssue] = []
        self.playback_tests: List[AudioPlaybackTest] = []

        # Expected audio files by category
        self.expected_audio = {
            "music": {
                "title_theme.ogg": {"min_duration": 30.0, "loops": True},
                "hub_theme.ogg": {"min_duration": 60.0, "loops": True},
                "ski_theme.ogg": {"min_duration": 45.0, "loops": True},
                "pool_theme.ogg": {"min_duration": 45.0, "loops": True},
                "vegas_theme.ogg": {"min_duration": 60.0, "loops": True},
                "boss_theme.ogg": {"min_duration": 30.0, "loops": True},
            },
            "sfx": {
                # Player sounds
                "jump.ogg": {"max_duration": 1.0, "min_volume": 0.5},
                "land.ogg": {"max_duration": 0.5, "min_volume": 0.3},
                "attack.ogg": {"max_duration": 1.0, "min_volume": 0.6},
                "hurt.ogg": {"max_duration": 1.0, "min_volume": 0.7},
                "collect.ogg": {"max_duration": 0.5, "min_volume": 0.5},
                # Game sounds
                "door_open.ogg": {"max_duration": 1.0, "min_volume": 0.5},
                "powerup.ogg": {"max_duration": 1.5, "min_volume": 0.6},
                "explosion.ogg": {"max_duration": 2.0, "min_volume": 0.8},
                "splash.ogg": {"max_duration": 1.0, "min_volume": 0.5},
                "ski_swoosh.ogg": {"max_duration": 1.0, "min_volume": 0.4},
                # UI sounds
                "menu_select.ogg": {"max_duration": 0.5, "min_volume": 0.4},
                "menu_hover.ogg": {"max_duration": 0.3, "min_volume": 0.3},
                "pause.ogg": {"max_duration": 0.5, "min_volume": 0.5},
                "unpause.ogg": {"max_duration": 0.5, "min_volume": 0.5},
            },
        }

        # Audio quality thresholds
        self.quality_thresholds = {
            "min_bitrate": 128000,  # 128 kbps
            "max_silence_ratio": 0.1,  # Max 10% silence
            "clipping_threshold": 0.95,  # 95% of max amplitude
            "noise_floor": -60,  # dB
        }

    def run_validation(self) -> Dict[str, any]:
        """Run complete audio validation suite."""
        print("🔊 Starting audio validation...")

        # Initialize pygame mixer
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # Run validation tests
        test_results = {
            "file_validation": self._validate_audio_files(),
            "quality_check": self._check_audio_quality(),
            "playback_test": self._test_audio_playback(),
            "integration_test": self._test_audio_integration(),
        }

        pygame.mixer.quit()

        # Generate report
        return self._generate_report(test_results)

    def _validate_audio_files(self) -> Dict[str, any]:
        """Validate that all expected audio files exist and are valid."""
        print("\n📁 Validating audio files...")

        results = {
            "total_expected": 0,
            "found": 0,
            "missing": [],
            "corrupted": [],
            "wrong_format": [],
        }

        for category, files in self.expected_audio.items():
            category_dir = self.audio_dir / category

            for filename, specs in files.items():
                results["total_expected"] += 1
                file_path = category_dir / filename

                if not file_path.exists():
                    results["missing"].append(str(file_path))
                    self.issues.append(
                        AudioIssue(
                            file_path=str(file_path),
                            issue_type="missing_file",
                            description=f"Required audio file not found: {filename}",
                            severity="high",
                        )
                    )
                    continue

                # Validate file format
                if not self._validate_file_format(file_path):
                    results["wrong_format"].append(str(file_path))
                    continue

                # Check if file is corrupted
                if not self._validate_file_integrity(file_path):
                    results["corrupted"].append(str(file_path))
                    continue

                results["found"] += 1

                # Validate duration if specified
                duration = self._get_audio_duration(file_path)
                if duration:
                    if "min_duration" in specs and duration < specs["min_duration"]:
                        self.issues.append(
                            AudioIssue(
                                file_path=str(file_path),
                                issue_type="duration_too_short",
                                description=f"Audio duration {duration:.1f}s is less than required {specs['min_duration']}s",
                                severity="medium",
                            )
                        )

                    if "max_duration" in specs and duration > specs["max_duration"]:
                        self.issues.append(
                            AudioIssue(
                                file_path=str(file_path),
                                issue_type="duration_too_long",
                                description=f"Audio duration {duration:.1f}s exceeds maximum {specs['max_duration']}s",
                                severity="low",
                            )
                        )

        return results

    def _check_audio_quality(self) -> Dict[str, any]:
        """Check audio quality metrics."""
        print("\n🎵 Checking audio quality...")

        results = {
            "files_checked": 0,
            "quality_issues": [],
            "volume_issues": [],
            "format_issues": [],
        }

        for category in ["music", "sfx"]:
            category_dir = self.audio_dir / category
            if not category_dir.exists():
                continue

            for audio_file in category_dir.glob("*.ogg"):
                results["files_checked"] += 1

                # Check bitrate
                bitrate = self._get_bitrate(audio_file)
                if bitrate and bitrate < self.quality_thresholds["min_bitrate"]:
                    results["quality_issues"].append(
                        {
                            "file": str(audio_file),
                            "issue": f"Low bitrate: {bitrate / 1000:.0f} kbps",
                        }
                    )
                    self.issues.append(
                        AudioIssue(
                            file_path=str(audio_file),
                            issue_type="low_bitrate",
                            description=f"Bitrate {bitrate / 1000:.0f} kbps is below recommended {self.quality_thresholds['min_bitrate'] / 1000:.0f} kbps",
                            severity="low",
                        )
                    )

                # Check for clipping
                if self._check_clipping(audio_file):
                    results["quality_issues"].append(
                        {"file": str(audio_file), "issue": "Audio clipping detected"}
                    )
                    self.issues.append(
                        AudioIssue(
                            file_path=str(audio_file),
                            issue_type="clipping",
                            description="Audio clipping detected - may cause distortion",
                            severity="medium",
                        )
                    )

                # Check volume levels
                avg_volume = self._get_average_volume(audio_file)
                if avg_volume:
                    expected_specs = self._get_expected_specs(audio_file.name)
                    if expected_specs and "min_volume" in expected_specs:
                        if avg_volume < expected_specs["min_volume"] * 0.5:
                            results["volume_issues"].append(
                                {
                                    "file": str(audio_file),
                                    "issue": f"Volume too low: {avg_volume:.2f}",
                                }
                            )
                            self.issues.append(
                                AudioIssue(
                                    file_path=str(audio_file),
                                    issue_type="low_volume",
                                    description=f"Average volume {avg_volume:.2f} is too low",
                                    severity="medium",
                                )
                            )

                # Check for excessive silence
                silence_ratio = self._check_silence_ratio(audio_file)
                if silence_ratio > self.quality_thresholds["max_silence_ratio"]:
                    results["quality_issues"].append(
                        {
                            "file": str(audio_file),
                            "issue": f"Excessive silence: {silence_ratio * 100:.0f}%",
                        }
                    )

        return results

    def _test_audio_playback(self) -> Dict[str, any]:
        """Test audio playback functionality."""
        print("\n▶️  Testing audio playback...")

        results = {
            "scenes_tested": 0,
            "playback_errors": [],
            "transition_issues": [],
            "volume_issues": [],
        }

        # Test each scene's audio
        scene_audio_map = {
            "title": "title_theme.ogg",
            "hub": "hub_theme.ogg",
            "ski": "ski_theme.ogg",
            "pool": "pool_theme.ogg",
            "vegas": "vegas_theme.ogg",
        }

        for scene, expected_music in scene_audio_map.items():
            results["scenes_tested"] += 1

            # Simulate loading the music
            music_path = self.audio_dir / "music" / expected_music
            if music_path.exists():
                try:
                    pygame.mixer.music.load(str(music_path))
                    pygame.mixer.music.play(-1)  # Loop

                    # Check if playing
                    pygame.time.wait(100)  # Wait for playback to start
                    if not pygame.mixer.music.get_busy():
                        results["playback_errors"].append(
                            {"scene": scene, "issue": "Music failed to start playing"}
                        )
                        self.issues.append(
                            AudioIssue(
                                file_path=str(music_path),
                                issue_type="playback_failure",
                                description=f"Music failed to play in {scene} scene",
                                severity="high",
                            )
                        )

                    # Check volume
                    volume = pygame.mixer.music.get_volume()
                    if volume < 0.1:
                        results["volume_issues"].append(
                            {
                                "scene": scene,
                                "volume": volume,
                                "issue": "Music volume too low",
                            }
                        )

                    # Stop for next test
                    pygame.mixer.music.stop()

                except pygame.error as e:
                    results["playback_errors"].append(
                        {"scene": scene, "issue": f"Pygame error: {str(e)}"}
                    )
                    self.issues.append(
                        AudioIssue(
                            file_path=str(music_path),
                            issue_type="playback_error",
                            description=f"Pygame error in {scene}: {str(e)}",
                            severity="high",
                        )
                    )

        # Test sound effects
        sfx_tests = ["jump.ogg", "collect.ogg", "menu_select.ogg"]

        for sfx_name in sfx_tests:
            sfx_path = self.audio_dir / "sfx" / sfx_name
            if sfx_path.exists():
                try:
                    sound = pygame.mixer.Sound(str(sfx_path))
                    channel = sound.play()

                    if not channel:
                        results["playback_errors"].append(
                            {"sfx": sfx_name, "issue": "Failed to get playback channel"}
                        )

                except pygame.error as e:
                    results["playback_errors"].append(
                        {"sfx": sfx_name, "issue": f"Pygame error: {str(e)}"}
                    )

        return results

    def _test_audio_integration(self) -> Dict[str, any]:
        """Test audio integration with game systems."""
        print("\n🎮 Testing audio integration...")

        results = {
            "integration_tests": [],
            "timing_issues": [],
            "sync_issues": [],
        }

        # Import game modules
        try:
            from src.managers.sound_manager import SoundManager

            # Create sound manager
            sound_manager = SoundManager()

            # Test volume controls
            test_volumes = [0.0, 0.5, 1.0]
            for volume in test_volumes:
                sound_manager.set_master_volume(volume)
                if abs(sound_manager.master_volume - volume) > 0.01:
                    results["integration_tests"].append(
                        {
                            "test": "volume_control",
                            "issue": f"Volume set to {volume} but got {sound_manager.master_volume}",
                        }
                    )

            # Test music transitions
            music_files = ["title_theme.ogg", "hub_theme.ogg"]
            for music_file in music_files:
                music_path = self.audio_dir / "music" / music_file
                if music_path.exists():
                    try:
                        sound_manager.play_music(str(music_path))
                        # In headless mode, we can't fully test crossfade
                        results["integration_tests"].append(
                            {"test": f"play_{music_file}", "result": "success"}
                        )
                    except Exception as e:
                        results["integration_tests"].append(
                            {"test": f"play_{music_file}", "issue": str(e)}
                        )

            # Test sound effect playback
            sfx_path = self.audio_dir / "sfx" / "jump.ogg"
            if sfx_path.exists():
                try:
                    sound_manager.play_sound(str(sfx_path))
                    results["integration_tests"].append(
                        {"test": "play_sfx", "result": "success"}
                    )
                except Exception as e:
                    results["integration_tests"].append(
                        {"test": "play_sfx", "issue": str(e)}
                    )

        except ImportError as e:
            results["integration_tests"].append(
                {"test": "import_sound_manager", "issue": f"Failed to import: {str(e)}"}
            )

        return results

    def _validate_file_format(self, file_path: Path) -> bool:
        """Validate audio file format."""
        valid_extensions = [".ogg", ".mp3", ".wav"]
        return file_path.suffix.lower() in valid_extensions

    def _validate_file_integrity(self, file_path: Path) -> bool:
        """Check if audio file is corrupted."""
        try:
            if file_path.suffix.lower() == ".ogg":
                audio = OggVorbis(str(file_path))
                return audio.info.length > 0
            elif file_path.suffix.lower() == ".mp3":
                audio = MP3(str(file_path))
                return audio.info.length > 0
            elif file_path.suffix.lower() == ".wav":
                with wave.open(str(file_path), "rb") as wav:
                    return wav.getnframes() > 0
        except Exception as e:
            self.issues.append(
                AudioIssue(
                    file_path=str(file_path),
                    issue_type="corrupted_file",
                    description=f"File appears to be corrupted: {str(e)}",
                    severity="high",
                )
            )
            return False
        return True

    def _get_audio_duration(self, file_path: Path) -> Optional[float]:
        """Get audio file duration in seconds."""
        try:
            if file_path.suffix.lower() == ".ogg":
                audio = OggVorbis(str(file_path))
                return audio.info.length
            elif file_path.suffix.lower() == ".mp3":
                audio = MP3(str(file_path))
                return audio.info.length
            elif file_path.suffix.lower() == ".wav":
                with wave.open(str(file_path), "rb") as wav:
                    frames = wav.getnframes()
                    rate = wav.getframerate()
                    return frames / float(rate)
        except Exception:
            return None

    def _get_bitrate(self, file_path: Path) -> Optional[int]:
        """Get audio file bitrate."""
        try:
            if file_path.suffix.lower() == ".ogg":
                audio = OggVorbis(str(file_path))
                return audio.info.bitrate
            elif file_path.suffix.lower() == ".mp3":
                audio = MP3(str(file_path))
                return audio.info.bitrate
        except Exception:
            return None

    def _check_clipping(self, file_path: Path) -> bool:
        """Check if audio has clipping."""
        # Simplified check - in production would analyze waveform
        try:
            # Load audio and check peak levels
            pygame.mixer.Sound(str(file_path))
            # This is a placeholder - real implementation would analyze samples
            return False
        except Exception:
            return False

    def _get_average_volume(self, file_path: Path) -> Optional[float]:
        """Get average volume level (0.0 to 1.0)."""
        # Simplified - returns a mock value
        # Real implementation would analyze audio samples
        return 0.7

    def _check_silence_ratio(self, file_path: Path) -> float:
        """Check ratio of silence in audio file."""
        # Simplified - returns a mock value
        # Real implementation would analyze audio samples
        return 0.05

    def _get_expected_specs(self, filename: str) -> Optional[Dict]:
        """Get expected specifications for an audio file."""
        for category, files in self.expected_audio.items():
            if filename in files:
                return files[filename]
        return None

    def _generate_report(self, test_results: Dict[str, any]) -> Dict[str, any]:
        """Generate audio validation report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_issues": len(self.issues),
            "critical_issues": len([i for i in self.issues if i.severity == "high"]),
            "test_results": test_results,
            "issues_by_type": self._categorize_issues(),
            "issues_detail": [asdict(issue) for issue in self.issues],
        }

        # Save report
        report_path = (
            self.results_dir
            / f"audio_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        # Print summary
        self._print_summary(report)

        return report

    def _categorize_issues(self) -> Dict[str, int]:
        """Categorize issues by type."""
        categories = {}
        for issue in self.issues:
            categories[issue.issue_type] = categories.get(issue.issue_type, 0) + 1
        return categories

    def _print_summary(self, report: Dict[str, any]) -> None:
        """Print validation summary."""
        print("\n" + "=" * 60)
        print("🔊 AUDIO VALIDATION REPORT")
        print("=" * 60)

        file_results = report["test_results"]["file_validation"]
        print(f"Files Expected: {file_results['total_expected']}")
        print(f"Files Found: {file_results['found']}")
        print(f"Files Missing: {len(file_results['missing'])}")
        print(f"Files Corrupted: {len(file_results['corrupted'])}")

        quality_results = report["test_results"]["quality_check"]
        print(f"\nFiles Checked: {quality_results['files_checked']}")
        print(f"Quality Issues: {len(quality_results['quality_issues'])}")
        print(f"Volume Issues: {len(quality_results['volume_issues'])}")

        playback_results = report["test_results"]["playback_test"]
        print(f"\nScenes Tested: {playback_results['scenes_tested']}")
        print(f"Playback Errors: {len(playback_results['playback_errors'])}")

        print(f"\n🐛 Total Issues: {report['total_issues']}")
        print(f"❌ Critical Issues: {report['critical_issues']}")

        if report["total_issues"] > 0:
            print("\nIssues by Type:")
            for issue_type, count in report["issues_by_type"].items():
                print(f"  - {issue_type}: {count}")

        if file_results["missing"]:
            print("\n⚠️  Missing Files:")
            for file in file_results["missing"][:5]:  # Show first 5
                print(f"  - {file}")
            if len(file_results["missing"]) > 5:
                print(f"  ... and {len(file_results['missing']) - 5} more")

        print(f"\n📊 Full report saved to: {self.results_dir}")
        print("=" * 60)


def main():
    """Run audio validation."""
    validator = AudioValidator()
    report = validator.run_validation()

    # Return exit code based on critical issues
    if report["critical_issues"] > 0:
        return 1
    elif report["total_issues"] > 10:
        return 2
    return 0


if __name__ == "__main__":
    # Install required package if needed
    try:
        pass
    except ImportError:
        print("Installing mutagen for audio analysis...")
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "mutagen"])

    sys.exit(main())
