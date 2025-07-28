from src.scenes.title_screen import TitleScreen
from src.scenes.settings import SettingsScene
from src.scenes.hub import HubWorld
from src.scenes.vegas import VegasGame
from src.scenes.ski import SkiGame
from src.scenes.pool import PoolGame
from src.config.constants import (
    SCENE_TITLE,
    SCENE_SETTINGS,
    SCENE_HUB_WORLD,
    SCENE_VEGAS_GAME,
    SCENE_SKI_GAME,
    SCENE_POOL_GAME,
)
from src.managers.sound_manager import SoundManager
from src.utils.asset_paths import get_music_path
from src.utils.save_manager import SaveManager
import logging

logger = logging.getLogger(__name__)


class SceneManager:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_scene = None
        self.scenes = {}
        self.game_data = {"selected_character": None}

        # Initialize sound manager
        self.sound_manager = SoundManager()

        # Initialize save manager and load save data
        self.save_manager = SaveManager()
        self._load_game_data()

        # Initialize scenes
        self.scenes[SCENE_TITLE] = TitleScreen(
            screen_width, screen_height, self.sound_manager
        )
        self.scenes[SCENE_SETTINGS] = SettingsScene(
            screen_width, screen_height, self.sound_manager
        )
        self.scenes[SCENE_HUB_WORLD] = HubWorld(self)
        self.scenes[SCENE_VEGAS_GAME] = VegasGame(self)
        self.scenes[SCENE_SKI_GAME] = SkiGame(self)
        self.scenes[SCENE_POOL_GAME] = PoolGame(self)
        self.current_scene = self.scenes[SCENE_TITLE]

        # Start title music
        self.sound_manager.play_music(get_music_path("title_theme.wav"), fade_ms=1000)

    def handle_event(self, event):
        if self.current_scene:
            result = self.current_scene.handle_event(event)

            # Handle scene transitions
            if result == "start_game":
                self.game_data["selected_character"] = (
                    self.current_scene.selected_character
                )
                # Transition to hub world
                self.switch_scene(SCENE_HUB_WORLD)
            elif result == "vegas":
                self.switch_scene(SCENE_VEGAS_GAME)
            elif result == "ski":
                self.switch_scene(SCENE_SKI_GAME)
            elif result == "pool":
                self.switch_scene(SCENE_POOL_GAME)
            elif result:
                # Handle other scene transitions
                self.switch_scene(result)

    def update(self, dt: float):
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)

    def switch_scene(self, scene_name: str):
        if scene_name in self.scenes:
            previous_scene_name = None
            data = {}

            # Call on_exit for the current scene if it has the method
            if self.current_scene:
                for name, scene in self.scenes.items():
                    if scene == self.current_scene:
                        previous_scene_name = name
                        break
                if hasattr(self.current_scene, "on_exit"):
                    data = self.current_scene.on_exit()

            # Auto-save when transitioning between gameplay scenes
            if previous_scene_name not in [SCENE_TITLE, SCENE_SETTINGS]:
                self._auto_save()

            # Switch to the new scene
            self.current_scene = self.scenes[scene_name]

            # Call on_enter for the new scene if it has the method
            if hasattr(self.current_scene, "on_enter"):
                self.current_scene.on_enter(previous_scene_name, data)

            # Handle music transitions
            self._handle_music_transition(scene_name)

    def _handle_music_transition(self, scene_name: str):
        """Handle music transitions between scenes."""
        music_map = {
            SCENE_TITLE: "title_theme.wav",
            SCENE_HUB_WORLD: "hub_theme.wav",
            SCENE_SKI_GAME: "ski_theme.wav",
            SCENE_VEGAS_GAME: "vegas_theme.wav",
            SCENE_POOL_GAME: "pool_theme.wav",
        }

        if scene_name in music_map:
            music_file = get_music_path(music_map[scene_name])
            self.sound_manager.crossfade_music(music_file, duration_ms=1000)

    def _load_game_data(self):
        """Load saved game data from disk."""
        save_data = self.save_manager.load()

        # Apply saved settings
        self.sound_manager.set_master_volume(save_data["settings"]["master_volume"])
        self.sound_manager.set_music_volume(save_data["settings"]["music_volume"])
        self.sound_manager.set_sfx_volume(save_data["settings"]["sfx_volume"])

        # Restore game data
        self.game_data["selected_character"] = save_data["player"]["selected_character"]

        logger.info("Game data loaded successfully")

    def _auto_save(self):
        """Automatically save game progress."""
        try:
            # Update save data with current game state
            self.save_manager.set_selected_character(
                self.game_data.get("selected_character")
            )

            # Save to disk
            if self.save_manager.save():
                logger.info("Auto-save completed")
            else:
                logger.warning("Auto-save failed")
        except Exception as e:
            logger.error(f"Error during auto-save: {e}")

    def save_game(self):
        """Manually save the game."""
        self._auto_save()

    def get_save_manager(self):
        """Get the save manager instance for other components to use."""
        return self.save_manager
