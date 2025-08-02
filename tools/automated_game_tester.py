"""
Automated Game Tester for Danger Rose
=====================================

This tool runs the game in headless mode and automatically detects:
- Visual bugs (missing sprites, rendering errors)
- Audio issues (missing sounds, playback errors)
- Crashes and exceptions
- Performance problems
- UI element positioning issues
"""

import os
import sys
import time
import json
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pygame
import numpy as np

# Set headless mode before importing game modules
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"


@dataclass
class VisualBug:
    """Represents a detected visual bug."""
    timestamp: float
    scene: str
    bug_type: str
    description: str
    location: Optional[Tuple[int, int]] = None
    severity: str = "medium"
    screenshot_path: Optional[str] = None


@dataclass
class AudioBug:
    """Represents a detected audio bug."""
    timestamp: float
    scene: str
    bug_type: str
    description: str
    file_path: Optional[str] = None
    severity: str = "medium"


@dataclass
class PerformanceIssue:
    """Represents a performance problem."""
    timestamp: float
    scene: str
    fps: float
    frame_time_ms: float
    description: str
    severity: str = "low"


@dataclass
class CrashReport:
    """Represents a crash or exception."""
    timestamp: float
    scene: str
    exception_type: str
    message: str
    traceback: str
    severity: str = "high"


class AutomatedGameTester:
    """Automated testing system for Danger Rose game."""
    
    def __init__(self, output_dir: str = "test_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Test results
        self.visual_bugs: List[VisualBug] = []
        self.audio_bugs: List[AudioBug] = []
        self.performance_issues: List[PerformanceIssue] = []
        self.crashes: List[CrashReport] = []
        
        # Test state
        self.current_scene = "unknown"
        self.start_time = time.time()
        self.frame_count = 0
        self.last_fps_check = time.time()
        self.fps_samples = []
        
        # Screenshot comparison
        self.reference_screenshots = {}
        self.screenshot_dir = self.output_dir / "screenshots"
        self.screenshot_dir.mkdir(exist_ok=True)
        
        # Audio tracking
        self.audio_files_checked = set()
        self.missing_audio_files = set()
        
        # Visual detection thresholds
        self.black_screen_threshold = 0.95  # 95% black pixels = black screen
        self.missing_sprite_threshold = 0.8  # 80% transparent = missing sprite
        
    def run_automated_test(self, duration_seconds: int = 60) -> Dict[str, Any]:
        """Run automated test for specified duration."""
        print(f"🤖 Starting automated game test for {duration_seconds} seconds...")
        
        try:
            # Initialize pygame
            pygame.init()
            screen = pygame.display.set_mode((800, 600))
            clock = pygame.time.Clock()
            
            # Import game modules after pygame init
            from src.scene_manager import SceneManager
            
            # Create scene manager
            scene_manager = SceneManager(800, 600)
            
            # Test sequence: navigate through different scenes
            test_sequence = [
                ("start", 3.0),  # Title screen
                ("select_character", 2.0),  # Character selection
                ("start_game", 5.0),  # Hub world
                ("enter_ski", 10.0),  # Ski game
                ("return_to_hub", 5.0),  # Back to hub
                ("enter_pool", 10.0),  # Pool game
                ("return_to_hub", 5.0),  # Back to hub
                ("enter_vegas", 10.0),  # Vegas game
                ("pause_game", 2.0),  # Pause menu
                ("resume_game", 3.0),  # Resume
            ]
            
            sequence_index = 0
            sequence_timer = 0
            test_start = time.time()
            
            # Main test loop
            while time.time() - test_start < duration_seconds:
                dt = clock.tick(60) / 1000.0
                self.frame_count += 1
                
                # Update FPS tracking
                self._track_performance(dt)
                
                # Handle test sequence
                if sequence_index < len(test_sequence):
                    action, duration = test_sequence[sequence_index]
                    sequence_timer += dt
                    
                    if sequence_timer >= duration:
                        self._perform_action(action, scene_manager)
                        sequence_index += 1
                        sequence_timer = 0
                
                # Process game events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        break
                    scene_manager.handle_event(event)
                
                # Update game
                try:
                    scene_manager.update(dt)
                except Exception as e:
                    self._record_crash(e, scene_manager)
                
                # Draw and analyze frame
                try:
                    screen.fill((0, 0, 0))
                    scene_manager.draw(screen)
                    pygame.display.flip()
                    
                    # Analyze current frame
                    self._analyze_frame(screen, scene_manager)
                    
                except Exception as e:
                    self._record_crash(e, scene_manager)
                
                # Check audio status periodically
                if self.frame_count % 60 == 0:  # Once per second
                    self._check_audio_status(scene_manager)
            
        except Exception as e:
            self._record_crash(e, None)
        
        finally:
            pygame.quit()
            
        # Generate report
        return self._generate_report()
    
    def _perform_action(self, action: str, scene_manager) -> None:
        """Perform a test action."""
        print(f"🎮 Performing action: {action}")
        
        if action == "start":
            # Simulate pressing start button
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
            scene_manager.handle_event(event)
            
        elif action == "select_character":
            # Simulate selecting Dad character
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
            scene_manager.handle_event(event)
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
            scene_manager.handle_event(event)
            
        elif action == "start_game":
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
            scene_manager.handle_event(event)
            
        elif action == "enter_ski":
            # Move to ski door and enter
            self._simulate_movement(scene_manager, target_x=200, target_y=300)
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            scene_manager.handle_event(event)
            
        elif action == "enter_pool":
            # Move to pool door and enter
            self._simulate_movement(scene_manager, target_x=400, target_y=300)
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            scene_manager.handle_event(event)
            
        elif action == "enter_vegas":
            # Move to vegas door and enter
            self._simulate_movement(scene_manager, target_x=600, target_y=300)
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            scene_manager.handle_event(event)
            
        elif action == "return_to_hub":
            # Press ESC to return
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
            scene_manager.handle_event(event)
            
        elif action == "pause_game":
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
            scene_manager.handle_event(event)
            
        elif action == "resume_game":
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
            scene_manager.handle_event(event)
    
    def _simulate_movement(self, scene_manager, target_x: int, target_y: int) -> None:
        """Simulate player movement to a target position."""
        # This is simplified - in reality we'd need to track player position
        # and send appropriate movement events
        pass
    
    def _analyze_frame(self, screen: pygame.Surface, scene_manager) -> None:
        """Analyze current frame for visual issues."""
        # Get current scene name
        current_scene = self._get_scene_name(scene_manager)
        if current_scene != self.current_scene:
            print(f"📍 Scene changed: {self.current_scene} -> {current_scene}")
            self.current_scene = current_scene
        
        # Convert surface to numpy array for analysis
        pixels = pygame.surfarray.array3d(screen)
        
        # Check for black screen
        if self._is_black_screen(pixels):
            self.visual_bugs.append(VisualBug(
                timestamp=time.time() - self.start_time,
                scene=current_scene,
                bug_type="black_screen",
                description="Screen is completely or mostly black",
                severity="high"
            ))
            self._save_screenshot(screen, f"black_screen_{current_scene}")
        
        # Check for missing sprites (large transparent areas)
        transparent_regions = self._find_transparent_regions(screen)
        for region in transparent_regions:
            self.visual_bugs.append(VisualBug(
                timestamp=time.time() - self.start_time,
                scene=current_scene,
                bug_type="missing_sprite",
                description=f"Large transparent region detected at {region}",
                location=region,
                severity="medium"
            ))
        
        # Check for UI element positioning
        self._check_ui_elements(screen, current_scene)
        
        # Take reference screenshot periodically
        if self.frame_count % 300 == 0:  # Every 5 seconds at 60 FPS
            self._save_screenshot(screen, f"reference_{current_scene}_{self.frame_count}")
    
    def _is_black_screen(self, pixels: np.ndarray) -> bool:
        """Check if screen is mostly black."""
        # Count black or near-black pixels
        black_pixels = np.sum(np.all(pixels < 10, axis=2))
        total_pixels = pixels.shape[0] * pixels.shape[1]
        black_ratio = black_pixels / total_pixels
        
        return black_ratio > self.black_screen_threshold
    
    def _find_transparent_regions(self, screen: pygame.Surface) -> List[Tuple[int, int]]:
        """Find large transparent regions that might indicate missing sprites."""
        # This is simplified - in a real implementation we'd use more sophisticated
        # image processing to detect actual missing sprites vs intentional transparency
        transparent_regions = []
        
        # Check common sprite locations
        sprite_locations = [
            (400, 300),  # Center (player)
            (100, 100),  # Top-left (UI)
            (700, 100),  # Top-right (UI)
        ]
        
        for x, y in sprite_locations:
            # Check a region around each location
            region_size = 50
            if self._is_region_transparent(screen, x - region_size, y - region_size, 
                                          region_size * 2, region_size * 2):
                transparent_regions.append((x, y))
        
        return transparent_regions
    
    def _is_region_transparent(self, screen: pygame.Surface, x: int, y: int, 
                              width: int, height: int) -> bool:
        """Check if a region is mostly transparent."""
        # Simplified check - in reality we'd sample the region properly
        try:
            color = screen.get_at((x + width // 2, y + height // 2))
            return color.a < 128  # Less than 50% opacity
        except:
            return False
    
    def _check_ui_elements(self, screen: pygame.Surface, scene: str) -> None:
        """Check if UI elements are properly positioned."""
        # Scene-specific UI checks
        if scene == "hub_world":
            # Check if doors are visible
            door_positions = [(200, 300), (400, 300), (600, 300)]
            for x, y in door_positions:
                color = screen.get_at((x, y))
                if color == (0, 0, 0, 255):  # Pure black
                    self.visual_bugs.append(VisualBug(
                        timestamp=time.time() - self.start_time,
                        scene=scene,
                        bug_type="missing_ui_element",
                        description=f"Door not visible at position ({x}, {y})",
                        location=(x, y),
                        severity="medium"
                    ))
    
    def _check_audio_status(self, scene_manager) -> None:
        """Check audio system status."""
        try:
            # Check if music is playing
            if hasattr(scene_manager, 'sound_manager'):
                sound_manager = scene_manager.sound_manager
                
                # Check if any music should be playing
                if not pygame.mixer.music.get_busy():
                    self.audio_bugs.append(AudioBug(
                        timestamp=time.time() - self.start_time,
                        scene=self.current_scene,
                        bug_type="no_music",
                        description="No background music playing",
                        severity="low"
                    ))
                
                # Check volume levels
                volume = pygame.mixer.music.get_volume()
                if volume == 0:
                    self.audio_bugs.append(AudioBug(
                        timestamp=time.time() - self.start_time,
                        scene=self.current_scene,
                        bug_type="muted_music",
                        description="Music volume is set to 0",
                        severity="medium"
                    ))
        
        except Exception as e:
            self.audio_bugs.append(AudioBug(
                timestamp=time.time() - self.start_time,
                scene=self.current_scene,
                bug_type="audio_error",
                description=f"Error checking audio: {str(e)}",
                severity="high"
            ))
    
    def _track_performance(self, dt: float) -> None:
        """Track performance metrics."""
        current_time = time.time()
        
        # Calculate FPS every second
        if current_time - self.last_fps_check >= 1.0:
            fps = self.frame_count / (current_time - self.start_time)
            self.fps_samples.append(fps)
            
            # Check for low FPS
            if fps < 30:
                self.performance_issues.append(PerformanceIssue(
                    timestamp=current_time - self.start_time,
                    scene=self.current_scene,
                    fps=fps,
                    frame_time_ms=1000 / fps if fps > 0 else 999,
                    description=f"Low FPS detected: {fps:.1f}",
                    severity="medium" if fps > 20 else "high"
                ))
            
            self.last_fps_check = current_time
    
    def _record_crash(self, exception: Exception, scene_manager) -> None:
        """Record a crash or exception."""
        self.crashes.append(CrashReport(
            timestamp=time.time() - self.start_time,
            scene=self.current_scene,
            exception_type=type(exception).__name__,
            message=str(exception),
            traceback=traceback.format_exc(),
            severity="high"
        ))
    
    def _get_scene_name(self, scene_manager) -> str:
        """Get current scene name from scene manager."""
        try:
            if hasattr(scene_manager, '_get_current_scene_name'):
                return scene_manager._get_current_scene_name() or "unknown"
        except:
            pass
        return "unknown"
    
    def _save_screenshot(self, screen: pygame.Surface, name: str) -> str:
        """Save a screenshot for analysis."""
        filename = f"{name}_{int(time.time())}.png"
        filepath = self.screenshot_dir / filename
        pygame.image.save(screen, str(filepath))
        return str(filepath)
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate test report."""
        report = {
            "test_duration": time.time() - self.start_time,
            "total_frames": self.frame_count,
            "average_fps": sum(self.fps_samples) / len(self.fps_samples) if self.fps_samples else 0,
            "visual_bugs": len(self.visual_bugs),
            "audio_bugs": len(self.audio_bugs),
            "performance_issues": len(self.performance_issues),
            "crashes": len(self.crashes),
            "details": {
                "visual_bugs": [asdict(bug) for bug in self.visual_bugs],
                "audio_bugs": [asdict(bug) for bug in self.audio_bugs],
                "performance_issues": [asdict(issue) for issue in self.performance_issues],
                "crashes": [asdict(crash) for crash in self.crashes]
            }
        }
        
        # Save report to file
        report_path = self.output_dir / f"test_report_{int(time.time())}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        self._print_summary(report)
        
        return report
    
    def _print_summary(self, report: Dict[str, Any]) -> None:
        """Print test summary."""
        print("\n" + "="*60)
        print("🤖 AUTOMATED TEST REPORT")
        print("="*60)
        print(f"Duration: {report['test_duration']:.1f} seconds")
        print(f"Frames: {report['total_frames']}")
        print(f"Average FPS: {report['average_fps']:.1f}")
        print("\n🐛 Issues Found:")
        print(f"  Visual Bugs: {report['visual_bugs']}")
        print(f"  Audio Bugs: {report['audio_bugs']}")
        print(f"  Performance Issues: {report['performance_issues']}")
        print(f"  Crashes: {report['crashes']}")
        
        # Print critical issues
        if report['crashes'] > 0:
            print("\n❌ CRITICAL: Game crashed during testing!")
            for crash in report['details']['crashes']:
                print(f"  - {crash['exception_type']}: {crash['message']}")
        
        if report['visual_bugs'] > 0:
            print("\n⚠️  Visual issues detected:")
            bug_types = defaultdict(int)
            for bug in report['details']['visual_bugs']:
                bug_types[bug['bug_type']] += 1
            for bug_type, count in bug_types.items():
                print(f"  - {bug_type}: {count} occurrences")
        
        print("\n📊 Full report saved to:", self.output_dir)
        print("="*60)


def main():
    """Run automated game test."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated bug detection for Danger Rose")
    parser.add_argument("--duration", type=int, default=30, 
                       help="Test duration in seconds (default: 30)")
    args = parser.parse_args()
    
    tester = AutomatedGameTester()
    
    # Run test
    report = tester.run_automated_test(duration_seconds=args.duration)
    
    # Return exit code based on critical issues
    if report['crashes'] > 0:
        return 1
    elif report['visual_bugs'] > 5 or report['performance_issues'] > 10:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())