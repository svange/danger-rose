import pygame
import os
from typing import Optional


def load_image(path: str, scale: Optional[tuple] = None) -> pygame.Surface:
    """Load an image from an absolute path."""
    if not os.path.exists(path):
        # Create a placeholder surface if image doesn't exist
        surface = pygame.Surface((64, 64))
        surface.fill((255, 0, 255))  # Magenta placeholder
        return surface

    try:
        surface = pygame.image.load(path).convert_alpha()
        if scale:
            surface = pygame.transform.scale(surface, scale)
        return surface
    except pygame.error:
        # Create a placeholder surface if loading fails
        surface = pygame.Surface((64, 64))
        surface.fill((255, 0, 255))  # Magenta placeholder
        return surface


def load_sprite_sheet(
    path: str, frame_width: int, frame_height: int, scale: Optional[tuple] = None
) -> list:
    """Load a sprite sheet and return a list of individual frames."""
    if not os.path.exists(path):
        # Create placeholder frames if sprite sheet doesn't exist
        placeholder = pygame.Surface((frame_width, frame_height))
        placeholder.fill((255, 0, 255))  # Magenta placeholder
        return [placeholder]

    try:
        sheet = pygame.image.load(path).convert_alpha()
        frames = []

        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()

        for y in range(0, sheet_height, frame_height):
            for x in range(0, sheet_width, frame_width):
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), (x, y, frame_width, frame_height))

                if scale:
                    frame = pygame.transform.scale(frame, scale)

                frames.append(frame)

        return frames if frames else [pygame.Surface((frame_width, frame_height))]

    except pygame.error:
        # Create placeholder frame if loading fails
        placeholder = pygame.Surface((frame_width, frame_height))
        placeholder.fill((255, 0, 255))  # Magenta placeholder
        return [placeholder]


def load_character_animations(
    path: str,
    frame_width: int = 256,
    frame_height: int = 256,
    scale: Optional[tuple] = None,
) -> dict:
    """Load a character sprite sheet and return animations organized by type."""
    if not os.path.exists(path):
        # Create placeholder animations if sprite sheet doesn't exist
        placeholder = pygame.Surface((frame_width, frame_height))
        placeholder.fill((255, 0, 255))  # Magenta placeholder
        return {
            "walking": [placeholder] * 4,
            "jumping": [placeholder] * 4,
            "attacking": [placeholder] * 3,
        }

    try:
        sheet = pygame.image.load(path).convert_alpha()
        animations = {"walking": [], "jumping": [], "attacking": []}

        # Row 0: Walking animation (4 frames)
        for x in range(0, 4 * frame_width, frame_width):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (x, 0, frame_width, frame_height))
            if scale:
                frame = pygame.transform.scale(frame, scale)
            animations["walking"].append(frame)

        # Row 1: Jumping animation (4 frames)
        for x in range(0, 4 * frame_width, frame_width):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (x, frame_height, frame_width, frame_height))
            if scale:
                frame = pygame.transform.scale(frame, scale)
            animations["jumping"].append(frame)

        # Row 2: Attacking animation (3 frames, ignoring the effect frame)
        for x in range(0, 3 * frame_width, frame_width):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (x, 2 * frame_height, frame_width, frame_height))
            if scale:
                frame = pygame.transform.scale(frame, scale)
            animations["attacking"].append(frame)

        return animations

    except pygame.error:
        # Create placeholder animations if loading fails
        placeholder = pygame.Surface((frame_width, frame_height))
        placeholder.fill((255, 0, 255))  # Magenta placeholder
        return {
            "walking": [placeholder] * 4,
            "jumping": [placeholder] * 4,
            "attacking": [placeholder] * 3,
        }
