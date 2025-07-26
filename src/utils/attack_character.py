import pygame
import time
from typing import List


class AttackCharacter:
    """Simplified character animation that only shows the attack animation."""

    def __init__(
        self, character_name: str, sprite_path: str, scale: tuple = (128, 128)
    ):
        self.character_name = character_name
        self.scale = scale
        self.attack_frames = self._load_attack_frames(sprite_path)

        # Animation state
        self.current_frame = 0
        self.animation_speed = 0.3  # seconds per frame (slightly slower for attack)
        self.last_frame_time = time.time()

    def _load_attack_frames(self, sprite_path: str) -> List[pygame.Surface]:
        """Load just the attack animation frames (row 2) from the sprite sheet."""
        if not sprite_path:
            return self._create_placeholder_frames()

        try:
            sheet = pygame.image.load(sprite_path)
            if pygame.display.get_surface() is not None:
                sheet = sheet.convert_alpha()
            else:
                # If no display surface, just use the raw surface
                sheet = sheet.convert()

            # Calculate frame dimensions for 3x4 grid (3 rows, 4 columns)
            frame_width = 256  # 1024 / 4 columns
            frame_height = 341  # 1024 / 3 rows

            # Row 2 is the attack animation (0-indexed, bottom row)
            attack_row = 2
            base_y_start = attack_row * frame_height  # y = 2 * 341 = 682

            # Adjust sprite positioning UP by 1/3 of frame height to fix head cutoff
            y_offset = frame_height // 3  # 341 // 3 = 113 pixels up
            y_start = base_y_start - y_offset  # 682 - 113 = 569

            frames = []
            # Extract 3 attack frames (ignoring the 4th frame which is the effect)
            for col in range(3):
                x_start = col * frame_width

                # Extract frame with adjusted positioning
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), (x_start, y_start, frame_width, frame_height))

                # Scale if requested
                if self.scale:
                    frame = pygame.transform.scale(frame, self.scale)

                frames.append(frame)

            return frames if frames else self._create_placeholder_frames()

        except pygame.error as e:
            print(f"Error loading sprite sheet {sprite_path}: {e}")
            return self._create_placeholder_frames()

    def _create_placeholder_frames(self) -> List[pygame.Surface]:
        """Create placeholder frames if sprite loading fails."""
        placeholder = pygame.Surface(self.scale)
        placeholder.fill((255, 0, 255))  # Magenta placeholder
        return [placeholder] * 3

    def update(self):
        """Update the animation frame."""
        current_time = time.time()

        if current_time - self.last_frame_time >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.attack_frames)
            self.last_frame_time = current_time

    def get_current_sprite(self) -> pygame.Surface:
        """Get the current attack animation frame."""
        if self.attack_frames and 0 <= self.current_frame < len(self.attack_frames):
            return self.attack_frames[self.current_frame]

        # Fallback
        fallback = pygame.Surface(self.scale)
        fallback.fill((255, 0, 255))
        return fallback

    def get_frame_count(self) -> int:
        """Get the number of attack frames."""
        return len(self.attack_frames)

    def get_animation_info(self) -> str:
        """Get current animation info for debugging."""
        return f"Attack (Frame {self.current_frame + 1}/{len(self.attack_frames)})"
