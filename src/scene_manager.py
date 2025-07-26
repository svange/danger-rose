from src.scenes.title_screen import TitleScreen
from src.scenes.settings import SettingsScene
from src.config.constants import SCENE_TITLE, SCENE_SETTINGS


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
        self.current_scene = self.scenes[SCENE_TITLE]

    def handle_event(self, event):
        if self.current_scene:
            result = self.current_scene.handle_event(event)

            # Handle scene transitions
            if result == "start_game":
                self.game_data["selected_character"] = (
                    self.current_scene.selected_character
                )
                # For now, just log that we would transition to hub
                print(
                    f"Starting game with character: {self.game_data['selected_character']}"
                )
                # TODO: Transition to hub scene when it's created
            elif result:
                # Handle other scene transitions
                self.switch_scene(result)

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)

    def switch_scene(self, scene_name: str):
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
