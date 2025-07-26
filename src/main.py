import pygame
import sys
import logging
from src.scene_manager import SceneManager
from src.config.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    WINDOW_TITLE,
    COLOR_BLACK,
)
from src.config.game_config import get_config
from src.config.env_config import is_debug


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def game():
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Get configuration
    config = get_config()

    # Game screen setup
    if config.fullscreen:
        screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN
        )
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    # Initialize scene manager
    scene_manager = SceneManager(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle scene events
            scene_manager.handle_event(event)

        # Update game state
        scene_manager.update()

        # Draw everything
        screen.fill(COLOR_BLACK)  # Clear screen
        scene_manager.draw(screen)

        # Show FPS if enabled
        if config.show_fps or is_debug():
            fps = clock.get_fps()
            font = pygame.font.Font(None, 36)
            fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
            screen.blit(fps_text, (10, 10))

        pygame.display.flip()  # Update the display
        clock.tick(FPS)


if __name__ == "__main__":
    game()
