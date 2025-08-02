# Scene System Architecture

## Core Concept

Every game screen is a Scene with standardized lifecycle methods. The SceneManager handles transitions and maintains game state.

## Scene Lifecycle

```python
from abc import ABC, abstractmethod

class Scene(ABC):
    @abstractmethod
    def handle_event(self, event) -> str | None:
        """Process input, return next scene name or None"""
        pass
    
    @abstractmethod  
    def update(self, dt: float) -> None:
        """Update game logic with delta time"""
        pass
    
    @abstractmethod
    def draw(self, screen) -> None:
        """Render scene to screen"""
        pass
    
    def on_enter(self, previous_scene: str, data: dict) -> None:
        """Initialize scene with transition data"""
        pass
        
    def on_exit(self) -> dict:
        """Cleanup and return data for next scene"""
        return {}
```

## Scene Manager

```python
class SceneManager:
    def __init__(self):
        self.scenes = {
            "title": TitleScreen(),
            "character_select": CharacterSelectScreen(),
            "hub": HubWorld(),
            "ski": SkiGame(),
            "pool": PoolGame(),
            "vegas": VegasGame()
        }
        self.current_scene = "title"
        self.scene_data = {}
        
    def transition_to(self, scene_name: str, data: dict = None):
        """Handle scene transition with data passing"""
        if scene_name in self.scenes:
            exit_data = self.scenes[self.current_scene].on_exit()
            self.scene_data.update(exit_data)
            if data:
                self.scene_data.update(data)
                
            self.current_scene = scene_name
            self.scenes[scene_name].on_enter(
                previous_scene, 
                self.scene_data
            )
```

## Scene Flow Examples

### Hub World Navigation
```python
class HubWorld(Scene):
    def handle_event(self, event) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Check if player is near door
                if self.player.near_door("ski"):
                    return "ski"
                elif self.player.near_door("pool"):
                    return "pool"
                elif self.player.near_door("vegas"):
                    return "vegas"
        return None
```

### Game State Preservation
```python
class SkiGame(Scene):
    def on_enter(self, previous_scene: str, data: dict):
        self.character = data.get("selected_character", "danger")
        self.high_scores = data.get("high_scores", {})
        
    def on_exit(self) -> dict:
        return {
            "last_score": self.score,
            "high_scores": self.high_scores,
            "games_played": self.games_played + 1
        }
```

## Common Scene Patterns

### Menu Scenes
```python
class MenuScene(Scene):
    def __init__(self):
        self.selected_option = 0
        self.options = ["Start", "Settings", "Quit"]
        
    def handle_event(self, event) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = max(0, self.selected_option - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_option = min(
                    len(self.options) - 1, 
                    self.selected_option + 1
                )
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option].lower()
        return None
```

### Game Scenes
```python
class GameScene(Scene):
    def __init__(self):
        self.entities = pygame.sprite.Group()
        self.player = None
        self.paused = False
        
    def handle_event(self, event) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
            elif event.key == pygame.K_q and self.paused:
                return "hub"  # Quit to hub
        return None
        
    def update(self, dt: float):
        if not self.paused:
            self.entities.update(dt)
```

## Pause System

```python
class SceneManager:
    def __init__(self):
        self.paused = False
        self.pause_overlay = PauseOverlay()
        
    def handle_event(self, event):
        if self.paused:
            action = self.pause_overlay.handle_event(event)
            if action == "resume":
                self.paused = False
            elif action == "quit":
                return "hub"
        else:
            next_scene = self.current_scene.handle_event(event)
            if next_scene:
                self.transition_to(next_scene)
```

## Debug Scene Transitions

```python
# Environment variable overrides
START_SCENE = os.getenv("START_SCENE", "title")
SKIP_TITLE = os.getenv("SKIP_TITLE", "false").lower() == "true"

class SceneManager:
    def __init__(self):
        initial_scene = START_SCENE if START_SCENE else "title"
        if SKIP_TITLE and initial_scene == "title":
            initial_scene = "hub"
        self.current_scene = initial_scene
```