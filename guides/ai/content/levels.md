# Level and Scene Layout Patterns

Scene layout patterns and hub world design for family-friendly navigation.

## Hub World Structure

```python
class HubScene(Scene):
    def __init__(self):
        # Room layout with logical boundaries
        self.room_bounds = pygame.Rect(50, 50, 700, 500)
        self.boundaries = [
            # Walls (invisible collision rectangles)
            pygame.Rect(0, 0, 800, 50),      # Top wall
            pygame.Rect(0, 550, 800, 50),    # Bottom wall
            pygame.Rect(0, 0, 50, 600),      # Left wall
            pygame.Rect(750, 0, 50, 600),    # Right wall
        ]

        # Interactive objects
        self.doors = [
            Door(100, 300, "ski", "Ski Adventure!"),
            Door(400, 300, "pool", "Pool Party!"),
            Door(700, 300, "vegas", "Vegas Quest!")
        ]

        self.furniture = [
            TrophyShelf(200, 200),
            Couch(400, 400)
        ]

        # Player setup
        self.player = Player(400, 300, "danger")  # Center of room
```

## Door Interaction System

```python
class Door:
    def __init__(self, x: int, y: int, destination: str, label: str):
        self.rect = pygame.Rect(x - 30, y - 40, 60, 80)
        self.destination = destination
        self.label = label

        # Visual feedback
        self.hover_color = COLOR_YELLOW
        self.base_color = COLOR_BROWN
        self.is_highlighted = False

    def check_player_proximity(self, player) -> bool:
        distance = math.sqrt(
            (player.x - self.rect.centerx) ** 2 +
            (player.y - self.rect.centery) ** 2
        )
        self.is_highlighted = distance < DOOR_INTERACTION_DISTANCE
        return self.is_highlighted

    def draw(self, screen: pygame.Surface):
        color = self.hover_color if self.is_highlighted else self.base_color
        pygame.draw.rect(screen, color, self.rect)

        # Draw label when close
        if self.is_highlighted:
            draw_text_with_background(
                screen, self.label, FONT_SMALL,
                (self.rect.centerx, self.rect.top - 20),
                text_color=COLOR_BLACK,
                bg_color=COLOR_WHITE
            )
```

## Room Layout Helper

```python
def create_room_layout(width: int, height: int, wall_thickness: int = 50):
    """Create standard room boundaries for consistent level design."""
    return [
        pygame.Rect(0, 0, width, wall_thickness),                    # Top
        pygame.Rect(0, height - wall_thickness, width, wall_thickness), # Bottom
        pygame.Rect(0, 0, wall_thickness, height),                   # Left
        pygame.Rect(width - wall_thickness, 0, wall_thickness, height)  # Right
    ]

def place_furniture_grid(room_width: int, room_height: int, margin: int = 100):
    """Helper for placing furniture in logical grid positions."""
    positions = []
    for x in [margin, room_width // 2, room_width - margin]:
        for y in [margin, room_height // 2, room_height - margin]:
            positions.append((x, y))
    return positions
```

## Level Progression System

```python
class LevelManager:
    def __init__(self):
        self.completed_levels = set()
        self.current_difficulty = "easy"
        self.unlock_requirements = {
            "pool": [],  # Always available
            "ski": [],   # Always available
            "vegas": ["pool", "ski"]  # Requires completing other games
        }

    def is_level_unlocked(self, level_name: str) -> bool:
        requirements = self.unlock_requirements.get(level_name, [])
        return all(req in self.completed_levels for req in requirements)

    def complete_level(self, level_name: str, score: int):
        self.completed_levels.add(level_name)

        # Save progress
        save_data = {
            "completed_levels": list(self.completed_levels),
            "scores": {level_name: score}
        }
        SaveManager().save_game_state(save_data)
```

## Scene Transition Pattern

```python
def handle_door_interaction(self, player, doors) -> str | None:
    for door in doors:
        if door.check_player_proximity(player):
            # Show interaction prompt
            self.show_interaction_prompt = True
            self.current_door = door

            # Handle space key press
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                # Play door sound
                SoundManager().play_sound("door_open")

                # Return destination scene
                return door.destination

    self.show_interaction_prompt = False
    return None
```

## Multi-Room Level Design

```python
class MultiRoomLevel(Scene):
    def __init__(self):
        self.rooms = {
            "living_room": self._create_living_room(),
            "kitchen": self._create_kitchen(),
            "bedroom": self._create_bedroom()
        }
        self.current_room = "living_room"
        self.room_connections = {
            "living_room": {"right": "kitchen"},
            "kitchen": {"left": "living_room", "up": "bedroom"},
            "bedroom": {"down": "kitchen"}
        }

    def _create_living_room(self):
        return {
            "boundaries": create_room_layout(800, 600),
            "furniture": [
                Couch(400, 400),
                TrophyShelf(100, 200)
            ],
            "exits": [
                RoomExit(750, 300, "right", "kitchen")
            ]
        }

    def change_room(self, direction: str):
        connections = self.room_connections[self.current_room]
        if direction in connections:
            self.current_room = connections[direction]
            self._position_player_for_room_entry(direction)
```

## Kid-Friendly Navigation

```python
def draw_navigation_hints(self, screen: pygame.Surface):
    """Draw helpful navigation hints for young players."""

    # Arrow indicators for doors
    for door in self.doors:
        if door.is_highlighted:
            # Draw bouncing arrow above door
            arrow_y = door.rect.top - 40 + math.sin(time.time() * 3) * 5
            draw_arrow_indicator(screen, door.rect.centerx, arrow_y)

    # Mini-map in corner
    self._draw_mini_map(screen)

    # Breadcrumb trail showing where player came from
    if hasattr(self, 'previous_scene'):
        draw_text_with_background(
            screen, f"← Back to {self.previous_scene.title()}",
            FONT_SMALL, (100, 550),
            text_color=COLOR_BLUE
        )
```
