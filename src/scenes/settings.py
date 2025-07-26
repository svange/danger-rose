"""Settings scene for Danger Rose game.

This scene allows players to adjust game settings including
audio, display, controls, and accessibility options.
"""

import pygame
from typing import Optional, Dict, Any
from src.config.constants import (
    COLOR_WHITE,
    COLOR_BLACK,
    COLOR_BLUE,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    SCENE_TITLE,
)
from src.config.game_config import get_config


class SettingsScene:
    """Settings menu scene for configuring game options."""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.config = get_config()

        # UI elements
        self.font_title = pygame.font.Font(None, 72)
        self.font_label = pygame.font.Font(None, 36)
        self.font_button = pygame.font.Font(None, 32)

        # Back button
        self.back_button = pygame.Rect(
            50, self.screen_height - 100, BUTTON_WIDTH, BUTTON_HEIGHT
        )

        # Volume sliders
        self.master_volume_rect = pygame.Rect(
            self.screen_width // 2 - 200, 200, 400, 40
        )
        self.music_volume_rect = pygame.Rect(self.screen_width // 2 - 200, 300, 400, 40)
        self.sfx_volume_rect = pygame.Rect(self.screen_width // 2 - 200, 400, 400, 40)

        # Fullscreen toggle
        self.fullscreen_rect = pygame.Rect(self.screen_width // 2 - 100, 500, 200, 50)

        # State
        self.dragging_slider = None

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle input events.

        Args:
            event: Pygame event to process.

        Returns:
            Scene name to transition to, or None.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Check back button
            if self.back_button.collidepoint(mouse_pos):
                # Save settings before going back
                self.config.save()
                return SCENE_TITLE

            # Check fullscreen toggle
            if self.fullscreen_rect.collidepoint(mouse_pos):
                self.config.fullscreen = not self.config.fullscreen
                # Note: Actual fullscreen toggle would require recreating the display

            # Check volume sliders
            if self.master_volume_rect.collidepoint(mouse_pos):
                self.dragging_slider = "master"
            elif self.music_volume_rect.collidepoint(mouse_pos):
                self.dragging_slider = "music"
            elif self.sfx_volume_rect.collidepoint(mouse_pos):
                self.dragging_slider = "sfx"

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_slider = None

        elif event.type == pygame.MOUSEMOTION and self.dragging_slider:
            # Update volume based on mouse position
            mouse_x = event.pos[0]

            if self.dragging_slider == "master":
                relative_x = mouse_x - self.master_volume_rect.x
                volume = max(0.0, min(1.0, relative_x / self.master_volume_rect.width))
                self.config.master_volume = volume

            elif self.dragging_slider == "music":
                relative_x = mouse_x - self.music_volume_rect.x
                volume = max(0.0, min(1.0, relative_x / self.music_volume_rect.width))
                self.config.music_volume = volume

            elif self.dragging_slider == "sfx":
                relative_x = mouse_x - self.sfx_volume_rect.x
                volume = max(0.0, min(1.0, relative_x / self.sfx_volume_rect.width))
                self.config.sfx_volume = volume

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.config.save()
                return SCENE_TITLE

        return None

    def update(self, dt: float) -> None:
        """Update scene state.

        Args:
            dt: Time delta in seconds.
        """
        # Settings scene doesn't need animation updates
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the settings scene.

        Args:
            screen: Surface to draw on.
        """
        # Clear screen
        screen.fill(COLOR_BLACK)

        # Title
        title_surface = self.font_title.render("Settings", True, COLOR_WHITE)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 80))
        screen.blit(title_surface, title_rect)

        # Volume controls
        self._draw_volume_slider(
            screen,
            "Master Volume",
            self.master_volume_rect,
            self.config.master_volume,
            150,
        )
        self._draw_volume_slider(
            screen,
            "Music Volume",
            self.music_volume_rect,
            self.config.music_volume,
            250,
        )
        self._draw_volume_slider(
            screen, "SFX Volume", self.sfx_volume_rect, self.config.sfx_volume, 350
        )

        # Fullscreen toggle
        fullscreen_text = "Fullscreen: " + ("ON" if self.config.fullscreen else "OFF")
        fullscreen_surface = self.font_label.render(fullscreen_text, True, COLOR_WHITE)
        fullscreen_rect = fullscreen_surface.get_rect(
            center=(self.screen_width // 2, 525)
        )
        screen.blit(fullscreen_surface, fullscreen_rect)
        pygame.draw.rect(screen, COLOR_WHITE, self.fullscreen_rect, 2)

        # Back button
        pygame.draw.rect(screen, COLOR_BLUE, self.back_button)
        pygame.draw.rect(screen, COLOR_WHITE, self.back_button, 2)
        back_text = self.font_button.render("Back", True, COLOR_WHITE)
        back_rect = back_text.get_rect(center=self.back_button.center)
        screen.blit(back_text, back_rect)

        # Instructions
        instructions = [
            "Click and drag sliders to adjust volume",
            "Click fullscreen to toggle",
            "Press ESC or click Back to return",
        ]
        y_offset = self.screen_height - 250
        for instruction in instructions:
            inst_surface = self.font_button.render(instruction, True, COLOR_WHITE)
            inst_rect = inst_surface.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(inst_surface, inst_rect)
            y_offset += 40

    def _draw_volume_slider(
        self,
        screen: pygame.Surface,
        label: str,
        rect: pygame.Rect,
        value: float,
        y_pos: int,
    ) -> None:
        """Draw a volume slider.

        Args:
            screen: Surface to draw on.
            label: Label for the slider.
            rect: Rectangle for the slider track.
            value: Current value (0.0 to 1.0).
            y_pos: Y position for the label.
        """
        # Label
        label_surface = self.font_label.render(label, True, COLOR_WHITE)
        label_rect = label_surface.get_rect(center=(self.screen_width // 2, y_pos))
        screen.blit(label_surface, label_rect)

        # Slider track
        pygame.draw.rect(screen, (60, 60, 60), rect)
        pygame.draw.rect(screen, COLOR_WHITE, rect, 2)

        # Slider fill
        fill_width = int(rect.width * value)
        fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
        pygame.draw.rect(screen, COLOR_BLUE, fill_rect)

        # Slider handle
        handle_x = rect.x + fill_width
        handle_rect = pygame.Rect(handle_x - 5, rect.y - 5, 10, rect.height + 10)
        pygame.draw.rect(screen, COLOR_WHITE, handle_rect)

        # Value text
        value_text = f"{int(value * 100)}%"
        value_surface = self.font_button.render(value_text, True, COLOR_WHITE)
        value_rect = value_surface.get_rect(midleft=(rect.right + 20, rect.centery))
        screen.blit(value_surface, value_rect)

    def on_enter(
        self, previous_scene: Optional[str], data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Called when entering this scene.

        Args:
            previous_scene: Name of the previous scene.
            data: Optional data passed from previous scene.
        """
        # Reload config in case it was changed elsewhere
        self.config = get_config()

    def on_exit(self) -> Dict[str, Any]:
        """Called when leaving this scene.

        Returns:
            Data to pass to the next scene.
        """
        # Save any pending changes
        if self.config.is_modified():
            self.config.save()
        return {}
