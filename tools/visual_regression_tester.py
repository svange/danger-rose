"""
Visual Regression Testing for Danger Rose
=========================================

This tool captures and compares screenshots to detect visual regressions
and common rendering bugs in the game.
"""

import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pygame
from PIL import Image, ImageChops, ImageStat

# Set headless mode
os.environ["SDL_VIDEODRIVER"] = "dummy"


@dataclass
class VisualRegression:
    """Represents a visual regression detected between screenshots."""

    scene: str
    test_name: str
    difference_percentage: float
    pixel_diff_count: int
    description: str
    reference_path: str
    current_path: str
    diff_path: str


class VisualRegressionTester:
    """Visual regression testing system for Danger Rose."""

    def __init__(self, reference_dir: str = "visual_references"):
        self.reference_dir = Path(reference_dir)
        self.reference_dir.mkdir(exist_ok=True)

        self.results_dir = Path("visual_test_results")
        self.results_dir.mkdir(exist_ok=True)

        self.current_test_dir = self.results_dir / datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
        self.current_test_dir.mkdir(exist_ok=True)

        self.regressions: list[VisualRegression] = []
        self.test_cases: dict[str, list[str]] = {}

        # Visual bug detection patterns
        self.bug_patterns = {
            "missing_sprite": self._detect_missing_sprite,
            "z_order_issue": self._detect_z_order_issue,
            "clipping_error": self._detect_clipping_error,
            "color_corruption": self._detect_color_corruption,
            "ui_misalignment": self._detect_ui_misalignment,
            "animation_glitch": self._detect_animation_glitch,
        }

    def run_visual_tests(self) -> dict[str, any]:
        """Run all visual regression tests."""
        print("🎨 Starting visual regression tests...")

        # Initialize pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))

        # Import game modules
        from src.scene_manager import SceneManager

        # Create scene manager
        scene_manager = SceneManager(800, 600)

        # Define test scenarios
        test_scenarios = [
            ("title_screen", self._test_title_screen),
            ("character_selection", self._test_character_selection),
            ("hub_world", self._test_hub_world),
            ("ski_game", self._test_ski_game),
            ("pool_game", self._test_pool_game),
            ("vegas_game", self._test_vegas_game),
            ("pause_menu", self._test_pause_menu),
            ("sprite_rendering", self._test_sprite_rendering),
            ("ui_elements", self._test_ui_elements),
            ("animation_states", self._test_animation_states),
        ]

        results = {}

        for test_name, test_func in test_scenarios:
            print(f"\n📸 Running test: {test_name}")
            try:
                test_results = test_func(screen, scene_manager)
                results[test_name] = test_results

                # Check for visual bugs in each screenshot
                for screenshot_name, screenshot_path in test_results.get(
                    "screenshots", {}
                ).items():
                    self._analyze_screenshot_for_bugs(
                        screenshot_path, test_name, screenshot_name
                    )

            except Exception as e:
                print(f"❌ Test failed: {test_name} - {str(e)}")
                results[test_name] = {"error": str(e)}

        pygame.quit()

        # Generate report
        return self._generate_report(results)

    def _test_title_screen(self, screen: pygame.Surface, scene_manager) -> dict:
        """Test title screen rendering."""
        results = {"screenshots": {}}

        # Ensure we're on title screen
        scene_manager.switch_scene("title")

        # Wait for scene to stabilize
        for _ in range(10):
            scene_manager.update(0.016)
            screen.fill((0, 0, 0))
            scene_manager.draw(screen)
            pygame.display.flip()

        # Capture screenshots
        screenshots = [
            ("title_base", "Basic title screen"),
            ("title_hover_start", "Title with start button hover"),
            ("title_hover_settings", "Title with settings button hover"),
        ]

        for name, description in screenshots:
            path = self._capture_screenshot(screen, name)
            results["screenshots"][name] = path

            # Compare with reference if exists
            regression = self._compare_with_reference(path, name)
            if regression:
                self.regressions.append(regression)

        return results

    def _test_character_selection(self, screen: pygame.Surface, scene_manager) -> dict:
        """Test character selection screen."""
        results = {"screenshots": {}}

        # Navigate to character selection
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        scene_manager.handle_event(event)

        # Test each character
        characters = ["danger", "rose", "dad"]
        for i, character in enumerate(characters):
            # Navigate to character
            for _ in range(i):
                event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
                scene_manager.handle_event(event)

            # Update and capture
            for _ in range(5):
                scene_manager.update(0.016)
                screen.fill((0, 0, 0))
                scene_manager.draw(screen)
                pygame.display.flip()

            path = self._capture_screenshot(screen, f"character_select_{character}")
            results["screenshots"][f"select_{character}"] = path

        return results

    def _test_hub_world(self, screen: pygame.Surface, scene_manager) -> dict:
        """Test hub world rendering."""
        results = {"screenshots": {}}

        # Start game
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        scene_manager.handle_event(event)

        # Capture different areas of hub
        test_positions = [
            ("hub_center", 400, 300),
            ("hub_ski_door", 200, 300),
            ("hub_pool_door", 400, 300),
            ("hub_vegas_door", 600, 300),
        ]

        for name, x, y in test_positions:
            # Update scene
            for _ in range(10):
                scene_manager.update(0.016)
                screen.fill((0, 0, 0))
                scene_manager.draw(screen)
                pygame.display.flip()

            path = self._capture_screenshot(screen, name)
            results["screenshots"][name] = path

        return results

    def _test_ski_game(self, screen: pygame.Surface, scene_manager) -> dict:
        """Test ski game rendering."""
        results = {"screenshots": {}}

        # Enter ski game
        scene_manager.switch_scene("ski")

        # Capture gameplay moments
        moments = [
            ("ski_start", 0),
            ("ski_gameplay", 30),
            ("ski_with_obstacles", 60),
        ]

        for name, frames in moments:
            for _ in range(frames):
                scene_manager.update(0.016)
                screen.fill((0, 0, 0))
                scene_manager.draw(screen)
                pygame.display.flip()

            path = self._capture_screenshot(screen, name)
            results["screenshots"][name] = path

        return results

    def _test_pool_game(self, screen: pygame.Surface, scene_manager) -> dict:
        """Test pool game rendering."""
        results = {"screenshots": {}}

        # Enter pool game
        scene_manager.switch_scene("pool")

        # Test different game states
        states = [
            ("pool_start", 0),
            ("pool_targets", 30),
            ("pool_powerup", 60),
        ]

        for name, frames in states:
            for _ in range(frames):
                scene_manager.update(0.016)
                screen.fill((0, 0, 0))
                scene_manager.draw(screen)
                pygame.display.flip()

            path = self._capture_screenshot(screen, name)
            results["screenshots"][name] = path

        return results

    def _test_vegas_game(self, screen: pygame.Surface, scene_manager) -> dict:
        """Test vegas game rendering."""
        results = {"screenshots": {}}

        # Enter vegas game
        scene_manager.switch_scene("vegas")

        # Test different areas
        areas = [
            ("vegas_start", 0),
            ("vegas_platforms", 30),
            ("vegas_boss", 90),
        ]

        for name, frames in areas:
            for _ in range(frames):
                scene_manager.update(0.016)
                screen.fill((0, 0, 0))
                scene_manager.draw(screen)
                pygame.display.flip()

            path = self._capture_screenshot(screen, name)
            results["screenshots"][name] = path

        return results

    def _test_pause_menu(self, screen: pygame.Surface, scene_manager) -> dict:
        """Test pause menu rendering."""
        results = {"screenshots": {}}

        # Pause during gameplay
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
        scene_manager.handle_event(event)

        # Update and capture
        for _ in range(5):
            scene_manager.update(0.016)
            screen.fill((0, 0, 0))
            scene_manager.draw(screen)
            pygame.display.flip()

        path = self._capture_screenshot(screen, "pause_menu")
        results["screenshots"]["pause_menu"] = path

        return results

    def _test_sprite_rendering(self, screen: pygame.Surface, scene_manager) -> dict:
        """Test sprite rendering quality."""
        results = {"screenshots": {}, "issues": []}

        # Test character sprites
        from src.entities.player import Player

        test_characters = ["danger", "rose", "dad"]
        test_animations = ["idle", "walking", "jumping", "attacking"]

        for character in test_characters:
            player = Player(400, 300, character)

            for animation in test_animations:
                # Set animation state
                if hasattr(player, "animated_character"):
                    player.animated_character.set_animation(animation)

                # Draw and capture
                screen.fill((100, 100, 100))  # Gray background to see transparency
                player.draw(screen)
                pygame.display.flip()

                screenshot_name = f"sprite_{character}_{animation}"
                path = self._capture_screenshot(screen, screenshot_name)
                results["screenshots"][screenshot_name] = path

                # Check for sprite issues
                issues = self._check_sprite_quality(screen, character, animation)
                if issues:
                    results["issues"].extend(issues)

        return results

    def _test_ui_elements(self, screen: pygame.Surface, scene_manager) -> dict:
        """Test UI element rendering."""
        results = {"screenshots": {}, "alignment_issues": []}

        # Test various UI elements
        ui_tests = [
            ("score_display", self._render_score_ui),
            ("health_display", self._render_health_ui),
            ("dialog_box", self._render_dialog_ui),
            ("menu_buttons", self._render_menu_buttons),
        ]

        for name, render_func in ui_tests:
            screen.fill((50, 50, 50))
            render_func(screen)
            pygame.display.flip()

            path = self._capture_screenshot(screen, f"ui_{name}")
            results["screenshots"][name] = path

            # Check alignment
            alignment_issues = self._check_ui_alignment(screen, name)
            if alignment_issues:
                results["alignment_issues"].extend(alignment_issues)

        return results

    def _test_animation_states(self, screen: pygame.Surface, scene_manager) -> dict:
        """Test animation state transitions."""
        results = {"screenshots": {}, "animation_issues": []}

        # Test smooth animation transitions
        from src.entities.player import Player

        player = Player(400, 300, "danger")

        # Test transition sequences
        transitions = [
            ("idle_to_walk", ["idle", "walking"]),
            ("walk_to_jump", ["walking", "jumping"]),
            ("jump_to_idle", ["jumping", "idle"]),
            ("idle_to_attack", ["idle", "attacking"]),
        ]

        for name, sequence in transitions:
            frames = []

            for state in sequence:
                if hasattr(player, "animated_character"):
                    player.animated_character.set_animation(state)

                # Capture multiple frames of transition
                for i in range(5):
                    screen.fill((0, 0, 0))
                    player.update(0.016)
                    player.draw(screen)
                    pygame.display.flip()

                    if i == 2:  # Middle frame
                        path = self._capture_screenshot(screen, f"anim_{name}_frame{i}")
                        frames.append(path)

            results["screenshots"][name] = frames

            # Check for animation glitches
            glitches = self._detect_animation_glitches(frames)
            if glitches:
                results["animation_issues"].extend(glitches)

        return results

    def _capture_screenshot(self, screen: pygame.Surface, name: str) -> str:
        """Capture and save a screenshot."""
        filename = f"{name}.png"
        filepath = self.current_test_dir / filename
        pygame.image.save(screen, str(filepath))
        return str(filepath)

    def _compare_with_reference(
        self, current_path: str, test_name: str
    ) -> VisualRegression | None:
        """Compare current screenshot with reference."""
        reference_path = self.reference_dir / f"{test_name}.png"

        if not reference_path.exists():
            # No reference exists, save current as reference
            import shutil

            shutil.copy(current_path, reference_path)
            print(f"📸 Saved new reference: {test_name}")
            return None

        # Load images
        current_img = Image.open(current_path)
        reference_img = Image.open(reference_path)

        # Check dimensions
        if current_img.size != reference_img.size:
            return VisualRegression(
                scene=test_name,
                test_name=test_name,
                difference_percentage=100.0,
                pixel_diff_count=0,
                description=f"Image dimensions differ: {current_img.size} vs {reference_img.size}",
                reference_path=str(reference_path),
                current_path=current_path,
                diff_path="",
            )

        # Calculate difference
        diff = ImageChops.difference(current_img, reference_img)
        stat = ImageStat.Stat(diff)

        # Calculate difference percentage
        diff_ratio = sum(stat.mean) / (len(stat.mean) * 255)
        diff_percentage = diff_ratio * 100

        if diff_percentage > 1.0:  # 1% threshold
            # Save diff image
            diff_path = self.current_test_dir / f"{test_name}_diff.png"
            diff.save(diff_path)

            # Count different pixels
            diff_array = np.array(diff)
            pixel_diff_count = np.sum(
                diff_array > 10
            )  # Pixels with significant difference

            return VisualRegression(
                scene=test_name,
                test_name=test_name,
                difference_percentage=diff_percentage,
                pixel_diff_count=pixel_diff_count,
                description=f"Visual difference detected: {diff_percentage:.2f}%",
                reference_path=str(reference_path),
                current_path=current_path,
                diff_path=str(diff_path),
            )

        return None

    def _analyze_screenshot_for_bugs(
        self, screenshot_path: str, test_name: str, screenshot_name: str
    ) -> None:
        """Analyze screenshot for common visual bugs."""
        img = Image.open(screenshot_path)
        img_array = np.array(img)

        for bug_type, detect_func in self.bug_patterns.items():
            bug_info = detect_func(img_array, screenshot_name)
            if bug_info:
                print(f"⚠️  {bug_type} detected in {screenshot_name}: {bug_info}")

    def _detect_missing_sprite(self, img_array: np.ndarray, name: str) -> str | None:
        """Detect missing sprites (large transparent or black areas)."""
        # Check for large black rectangles that might be missing sprites
        height, width = img_array.shape[:2]

        # Look for rectangular regions that are completely black
        black_threshold = 10
        is_black = np.all(img_array[:, :, :3] < black_threshold, axis=2)

        # Find large contiguous black regions
        from scipy import ndimage

        labeled, num_features = ndimage.label(is_black)

        for i in range(1, num_features + 1):
            region_mask = labeled == i
            region_size = np.sum(region_mask)

            # If region is larger than 32x32 pixels, might be missing sprite
            if region_size > 1024:
                y_coords, x_coords = np.where(region_mask)
                y_min, y_max = y_coords.min(), y_coords.max()
                x_min, x_max = x_coords.min(), x_coords.max()

                # Check if it's a rectangular region (likely sprite placeholder)
                expected_size = (y_max - y_min + 1) * (x_max - x_min + 1)
                if region_size > expected_size * 0.8:  # 80% filled
                    return f"Possible missing sprite at ({x_min}, {y_min}) size: {x_max - x_min}x{y_max - y_min}"

        return None

    def _detect_z_order_issue(self, img_array: np.ndarray, name: str) -> str | None:
        """Detect z-order rendering issues."""
        # This is simplified - in reality we'd need semantic understanding
        # of what should be in front of what

        # Check if UI elements are behind game elements
        if "ui_" in name:
            # UI should typically be on top, check if it's obscured
            # This would require comparing with expected UI layout
            pass

        return None

    def _detect_clipping_error(self, img_array: np.ndarray, name: str) -> str | None:
        """Detect sprite clipping errors."""
        # Look for sprites cut off at screen edges
        height, width = img_array.shape[:2]

        # Check edges for partial sprites
        edge_threshold = 10

        # Check if non-background pixels touch the edges
        edges = [
            ("top", img_array[:edge_threshold, :]),
            ("bottom", img_array[-edge_threshold:, :]),
            ("left", img_array[:, :edge_threshold]),
            ("right", img_array[:, -edge_threshold:]),
        ]

        for edge_name, edge_pixels in edges:
            # If we find sprite-like patterns at the edge, might be clipping
            non_black = np.any(edge_pixels[:, :, :3] > 50, axis=2)
            if np.sum(non_black) > edge_pixels.shape[0] * edge_pixels.shape[1] * 0.3:
                return f"Possible sprite clipping at {edge_name} edge"

        return None

    def _detect_color_corruption(self, img_array: np.ndarray, name: str) -> str | None:
        """Detect color corruption or palette issues."""
        # Check for unusual color distributions
        unique_colors = len(
            np.unique(img_array.reshape(-1, img_array.shape[2]), axis=0)
        )

        # If very few colors, might indicate palette problem
        if unique_colors < 10:
            return f"Very limited color palette: only {unique_colors} unique colors"

        # Check for color banding
        # This would involve more sophisticated analysis

        return None

    def _detect_ui_misalignment(self, img_array: np.ndarray, name: str) -> str | None:
        """Detect UI element misalignment."""
        if "ui_" not in name:
            return None

        # This would require knowledge of expected UI positions
        # For now, check basic symmetry for centered elements
        height, width = img_array.shape[:2]

        # Check if centered elements are actually centered
        # This is a simplified check

        return None

    def _detect_animation_glitch(self, img_array: np.ndarray, name: str) -> str | None:
        """Detect animation glitches."""
        if "anim_" not in name:
            return None

        # Look for torn sprites or partial frames
        # This would require comparing consecutive frames

        return None

    def _check_sprite_quality(
        self, screen: pygame.Surface, character: str, animation: str
    ) -> list[str]:
        """Check sprite rendering quality."""
        issues = []

        # Get screen as array
        pixels = pygame.surfarray.array3d(screen)

        # Check for transparency issues
        # Gray background should be visible around sprite edges
        gray_count = np.sum(np.all(pixels == [100, 100, 100], axis=2))
        total_pixels = pixels.shape[0] * pixels.shape[1]

        if gray_count < total_pixels * 0.5:  # Less than 50% background visible
            issues.append(
                f"{character} {animation}: Sprite may be too large or have transparency issues"
            )

        return issues

    def _render_score_ui(self, screen: pygame.Surface) -> None:
        """Render score UI for testing."""
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: 1000", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def _render_health_ui(self, screen: pygame.Surface) -> None:
        """Render health UI for testing."""
        # Draw health hearts
        for i in range(3):
            pygame.draw.circle(screen, (255, 0, 0), (50 + i * 40, 50), 15)

    def _render_dialog_ui(self, screen: pygame.Surface) -> None:
        """Render dialog box for testing."""
        dialog_rect = pygame.Rect(100, 400, 600, 150)
        pygame.draw.rect(screen, (0, 0, 0), dialog_rect)
        pygame.draw.rect(screen, (255, 255, 255), dialog_rect, 3)

        font = pygame.font.Font(None, 24)
        text = font.render("This is a test dialog box", True, (255, 255, 255))
        screen.blit(text, (120, 420))

    def _render_menu_buttons(self, screen: pygame.Surface) -> None:
        """Render menu buttons for testing."""
        buttons = ["Start", "Options", "Quit"]

        for i, text in enumerate(buttons):
            button_rect = pygame.Rect(300, 200 + i * 60, 200, 50)
            pygame.draw.rect(screen, (100, 100, 100), button_rect)
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)

            font = pygame.font.Font(None, 36)
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)

    def _check_ui_alignment(self, screen: pygame.Surface, ui_type: str) -> list[str]:
        """Check UI element alignment."""
        issues = []

        # This would involve checking specific UI elements are properly aligned
        # For now, just return empty list

        return issues

    def _detect_animation_glitches(self, frame_paths: list[str]) -> list[str]:
        """Detect glitches in animation sequences."""
        glitches = []

        # Load frames
        frames = [Image.open(path) for path in frame_paths]

        # Check for sudden changes between frames
        for i in range(1, len(frames)):
            prev_frame = np.array(frames[i - 1])
            curr_frame = np.array(frames[i])

            # Calculate frame difference
            diff = np.abs(prev_frame.astype(float) - curr_frame.astype(float))
            avg_diff = np.mean(diff)

            # Large sudden change might indicate glitch
            if avg_diff > 100:  # Threshold
                glitches.append(
                    f"Large change between frames {i - 1} and {i}: {avg_diff:.1f}"
                )

        return glitches

    def _generate_report(self, results: dict[str, any]) -> dict[str, any]:
        """Generate visual test report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(results),
            "total_screenshots": sum(
                len(r.get("screenshots", {})) for r in results.values()
            ),
            "visual_regressions": len(self.regressions),
            "test_results": results,
            "regressions": [
                {
                    "scene": r.scene,
                    "test": r.test_name,
                    "difference": f"{r.difference_percentage:.2f}%",
                    "pixels_changed": r.pixel_diff_count,
                    "description": r.description,
                }
                for r in self.regressions
            ],
        }

        # Save report
        report_path = self.current_test_dir / "visual_test_report.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        # Print summary
        self._print_summary(report)

        return report

    def _print_summary(self, report: dict[str, any]) -> None:
        """Print test summary."""
        print("\n" + "=" * 60)
        print("🎨 VISUAL REGRESSION TEST REPORT")
        print("=" * 60)
        print(f"Total Tests: {report['total_tests']}")
        print(f"Screenshots Captured: {report['total_screenshots']}")
        print(f"Visual Regressions: {report['visual_regressions']}")

        if report["visual_regressions"] > 0:
            print("\n⚠️  Visual Regressions Detected:")
            for regression in report["regressions"]:
                print(
                    f"  - {regression['test']}: {regression['difference']} difference"
                )
                print(f"    {regression['description']}")

        # Count issues by type
        total_issues = 0
        issue_counts = {}

        for test_name, test_result in report["test_results"].items():
            if isinstance(test_result, dict):
                for key in ["issues", "alignment_issues", "animation_issues"]:
                    if key in test_result:
                        issue_counts[key] = issue_counts.get(key, 0) + len(
                            test_result[key]
                        )
                        total_issues += len(test_result[key])

        if total_issues > 0:
            print(f"\n🐛 Other Visual Issues: {total_issues}")
            for issue_type, count in issue_counts.items():
                print(f"  - {issue_type}: {count}")

        print(f"\n📊 Full report saved to: {self.current_test_dir}")
        print("=" * 60)


def main():
    """Run visual regression tests."""
    tester = VisualRegressionTester()
    report = tester.run_visual_tests()

    # Return exit code based on regressions
    if report["visual_regressions"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
