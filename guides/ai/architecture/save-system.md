# Save System Architecture

## Core SaveManager Usage

The Danger Rose save system provides JSON-based persistence with automatic migration and cross-platform directory handling.

## Basic Save Operations

```python
from src.utils.save_manager import SaveManager

# Initialize save manager (auto-detects OS-specific paths)
save_manager = SaveManager()

# Load existing save or create default
save_data = save_manager.load()

# Update and save data
save_manager.set_setting("master_volume", 0.8)
save_manager.set_selected_character("rose")
save_manager.save()
```

## Save Data Structure

```python
default_save_data = {
    "version": "1.0.0",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T15:45:00",
    
    "player": {
        "selected_character": "danger",
        "total_playtime": 3600
    },
    
    "settings": {
        "master_volume": 0.7,
        "music_volume": 0.7,
        "sfx_volume": 0.7,
        "fullscreen": False,
        "key_bindings": {
            "up": "w", "down": "s", "left": "a", "right": "d",
            "jump": "space", "action": "e"
        }
    },
    
    "progress": {
        "hub_world_unlocked": True,
        "minigames_unlocked": {
            "ski": False, "pool": False, "vegas": False
        },
        "trophies_earned": []
    },
    
    "high_scores": {
        "ski": {
            "danger": {
                "easy": [], "normal": [], "hard": []
            }
        }
    }
}
```

## High Score Management

```python
# Add a new high score
score_data = {
    "score": 1500,
    "player_name": "Danger",
    "character": "danger",
    "game_mode": "ski",
    "difficulty": "normal",
    "time_elapsed": 45.2,
    "date": "2024-01-15"
}

save_manager.add_high_score("ski", "danger", score_data, "normal")

# Retrieve high scores
high_scores = save_manager.get_high_scores("ski", "danger", "normal")
top_score = high_scores[0] if high_scores else None
```

## Cross-Platform Directory Handling

```python
def _get_default_save_directory(self) -> Path:
    try:
        home_path = Path.home()
    except (RuntimeError, KeyError):
        # CI/server fallback
        return Path(tempfile.gettempdir()) / "danger-rose"
    
    if os.name == "nt":  # Windows
        return Path(os.environ.get("APPDATA", home_path / "AppData/Roaming")) / "DangerRose"
    elif platform.system() == "Darwin":  # macOS
        return home_path / "Library/Application Support/DangerRose"
    else:  # Linux
        config_home = os.environ.get("XDG_CONFIG_HOME", home_path / ".config")
        return Path(config_home) / "danger-rose"
```

## Scene Integration Pattern

```python
class GameScene(Scene):
    def __init__(self):
        self.save_manager = SaveManager()
        self.save_data = self.save_manager.load()
        
    def on_enter(self, previous_scene: str, data: dict):
        # Use saved character selection
        self.character = self.save_manager.get_selected_character()
        if not self.character:
            self.character = data.get("selected_character", "danger")
            self.save_manager.set_selected_character(self.character)
            
    def on_exit(self) -> dict:
        # Auto-save progress
        self.save_manager.save()
        return {"last_save_time": self.save_manager.get_last_save_time()}
```

## Save Migration System

```python
def _validate_and_migrate_save_data(self, loaded_data: dict) -> dict:
    save_version = loaded_data.get("version", "0.0.0")
    
    # Deep merge with defaults to handle missing keys
    validated_data = self._deep_merge_dicts(
        self.default_save_data.copy(), 
        loaded_data
    )
    
    # Version-specific migrations
    if save_version < self.SAVE_VERSION:
        # Migrate old high score format
        if "high_scores" in validated_data:
            validated_data["high_scores"] = self._migrate_high_scores(
                validated_data["high_scores"]
            )
        
        validated_data["version"] = self.SAVE_VERSION
    
    return validated_data
```

## Backup and Recovery

```python
def save(self, save_data: dict = None) -> bool:
    try:
        # Create backup before writing
        if self.save_file_path.exists():
            backup_path = self.save_directory / f"{self.SAVE_FILE_NAME}.backup"
            self.save_file_path.replace(backup_path)
        
        # Write new save data
        with open(self.save_file_path, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)
            
        return True
        
    except OSError as e:
        # Restore backup on failure
        backup_path = self.save_directory / f"{self.SAVE_FILE_NAME}.backup"
        if backup_path.exists():
            backup_path.replace(self.save_file_path)
        return False
```