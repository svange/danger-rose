import pygame
import sys
import logging
from scene_manager import SceneManager


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


def game():
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Game screen setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Danger Rose")

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
        screen.fill((0, 0, 0))  # Clear screen
        scene_manager.draw(screen)

        pygame.display.flip()  # Update the display
        clock.tick(60)


if __name__ == "__main__":
    game()
