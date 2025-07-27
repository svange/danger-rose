from src.scenes.title_screen import TitleScreen
from src.scenes.settings import SettingsScene
from src.scenes.hub import HubWorld
from src.scenes.vegas import VegasGame
from src.config.constants import SCENE_TITLE, SCENE_SETTINGS, SCENE_HUB_WORLD, SCENE_VEGAS_GAME


class SceneManager:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_scene = None
        self.scenes = {}
        self.game_data = {"selected_character": None}

        # Initialize scenes
        self.scenes[SCENE_TITLE] = TitleScreen(screen_width, screen_height)
        self.scenes[SCENE_SETTINGS] = SettingsScene(screen_width, screen_height)
        self.scenes[SCENE_HUB_WORLD] = HubWorld(self)
        self.scenes[SCENE_VEGAS_GAME] = VegasGame(self)
        self.current_scene = self.scenes[SCENE_TITLE]

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
            elif result in ["ski", "pool"]:
                # Temporary: Just print message for minigames
                print(f"Would transition to {result} minigame (not implemented yet)")
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

            # Switch to the new scene
            self.current_scene = self.scenes[scene_name]

            # Call on_enter for the new scene if it has the method
            if hasattr(self.current_scene, "on_enter"):
                self.current_scene.on_enter(previous_scene_name, data)
