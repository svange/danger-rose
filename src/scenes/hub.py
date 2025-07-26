"""Hub world scene - the main apartment area."""

import pygame
from typing import Optional, Dict, Any
from src.utils.asset_paths import get_living_room_bg
from src.config.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class HubWorld:
    """The main hub world scene where players navigate the apartment."""

    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Load background
        try:
            self.background = pygame.image.load(get_living_room_bg())
            self.background = pygame.transform.scale(
                self.background, (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
        except (pygame.error, FileNotFoundError):
            # Create a simple background if image fails to load
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((50, 30, 20))  # Dark brown color

        # Define room boundaries (for future collision detection)
        self._setup_boundaries()

        # Get selected character from game data
        self.selected_character = self.scene_manager.game_data.get(
            "selected_character", "danger"
        )

    def _setup_boundaries(self):
        """Set up room boundaries and collision areas."""
        # Room boundaries (walls)
        self.boundaries = [
            pygame.Rect(0, 0, SCREEN_WIDTH, 50),  # Top wall
            pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),  # Bottom wall
            pygame.Rect(0, 0, 50, SCREEN_HEIGHT),  # Left wall
            pygame.Rect(SCREEN_WIDTH - 50, 0, 50, SCREEN_HEIGHT),  # Right wall
        ]

        # Interactive areas (for future use)
        self.door_areas = {
            "ski": pygame.Rect(200, 100, 100, 150),  # Ski game door
            "pool": pygame.Rect(400, 100, 100, 150),  # Pool game door
            "vegas": pygame.Rect(600, 100, 100, 150),  # Vegas game door
        }

        # Other interactive areas
        self.trophy_shelf_area = pygame.Rect(100, 200, 150, 100)  # Trophy shelf
        self.couch_area = pygame.Rect(350, 400, 200, 100)  # Save point couch

    def handle_event(self, event) -> Optional[str]:
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "settings"
            # Temporary navigation to test scenes (will be replaced by door interactions)
            elif event.key == pygame.K_1:
                return "ski"
            elif event.key == pygame.K_2:
                return "pool"
            elif event.key == pygame.K_3:
                return "vegas"

        return None

    def update(self, dt: float) -> None:
        """Update the hub world state."""
        # Future: Update character position, animations, etc.
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the hub world."""
        # Draw background
        screen.blit(self.background, (0, 0))

        # Draw temporary UI elements
        title_text = self.font.render("Hub World", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        # Draw selected character info
        char_text = self.small_font.render(
            f"Playing as: {self.selected_character.capitalize()}", True, (255, 255, 255)
        )
        char_rect = char_text.get_rect(topleft=(20, 20))
        screen.blit(char_text, char_rect)

        # Draw temporary instructions
        instructions = [
            "Press 1 - Ski Game",
            "Press 2 - Pool Game",
            "Press 3 - Vegas Game",
            "Press ESC - Settings",
        ]
        y_offset = SCREEN_HEIGHT - 120
        for instruction in instructions:
            inst_text = self.small_font.render(instruction, True, (255, 255, 255))
            inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(inst_text, inst_rect)
            y_offset += 25

        # Debug: Draw door areas (temporary visualization)
        if hasattr(self.scene_manager, "debug_mode") and self.scene_manager.debug_mode:
            for door_name, door_rect in self.door_areas.items():
                pygame.draw.rect(screen, (0, 255, 0), door_rect, 2)
                door_text = self.small_font.render(door_name, True, (0, 255, 0))
                text_rect = door_text.get_rect(center=door_rect.center)
                screen.blit(door_text, text_rect)

    def on_enter(self, previous_scene: Optional[str], data: Dict[str, Any]) -> None:
        """Called when entering the hub world."""
        # Update selected character if coming from character select
        if previous_scene == "character_select" and data.get("selected_character"):
            self.selected_character = data["selected_character"]
            self.scene_manager.game_data["selected_character"] = self.selected_character

    def on_exit(self) -> Dict[str, Any]:
        """Called when leaving the hub world."""
        return {"from_scene": "hub"}
