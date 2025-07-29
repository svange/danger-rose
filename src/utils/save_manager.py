"""Save/Load system for Danger Rose game with JSON persistence."""

import json
import os
import platform
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class SaveManager:
    """Manages game save data with JSON persistence and versioning."""

    SAVE_VERSION = "1.0.0"
    SAVE_FILE_NAME = "danger_rose_save.json"

    def __init__(self, save_directory: Optional[Path] = None):
        """Initialize SaveManager.

        Args:
            save_directory: Custom save directory. If None, uses user's app data.
        """
        self.save_directory = save_directory or self._get_default_save_directory()
        self.save_directory.mkdir(parents=True, exist_ok=True)
        self.save_file_path = self.save_directory / self.SAVE_FILE_NAME

        # Default save data structure
        self.default_save_data = {
            "version": self.SAVE_VERSION,
            "created_at": None,
            "updated_at": None,
            "player": {"selected_character": None, "total_playtime": 0},
            "settings": {
                "master_volume": 0.7,
                "music_volume": 0.7,
                "sfx_volume": 0.7,
                "fullscreen": False,
                "key_bindings": {
                    "up": "w",
                    "down": "s",
                    "left": "a",
                    "right": "d",
                    "jump": "space",
                    "action": "e",
                },
            },
            "progress": {
                "hub_world_unlocked": True,
                "minigames_unlocked": {"ski": False, "pool": False, "vegas": False},
                "trophies_earned": [],
            },
            "high_scores": {
                "ski": {"danger": [], "rose": [], "dad": []},
                "pool": {"danger": [], "rose": [], "dad": []},
                "vegas": {"danger": [], "rose": [], "dad": []},
            },
        }

        self._current_save_data = None

    def _get_default_save_directory(self) -> Path:
        """Get the default save directory based on the OS."""
        try:
            home_path = Path.home()
        except (RuntimeError, KeyError):
            # Handle case where home directory cannot be determined (e.g., in CI)
            logger.warning("Could not determine home directory, using temp directory")
            import tempfile

            return Path(tempfile.gettempdir()) / "danger-rose"

        if os.name == "nt":  # Windows
            app_data = os.environ.get("APPDATA")
            if app_data:
                return Path(app_data) / "DangerRose"
            else:
                return home_path / "AppData" / "Roaming" / "DangerRose"
        elif os.name == "posix":  # macOS and Linux
            if platform.system() == "Darwin":  # macOS
                return home_path / "Library" / "Application Support" / "DangerRose"
            else:  # Linux
                config_home = os.environ.get("XDG_CONFIG_HOME")
                if config_home:
                    return Path(config_home) / "danger-rose"
                else:
                    return home_path / ".config" / "danger-rose"
        else:
            # Fallback to home directory
            return home_path / ".danger-rose"

    def load(self) -> Dict[str, Any]:
        """Load save data from file.

        Returns:
            Dict containing save data. Returns default data if no save exists.
        """
        if not self.save_file_path.exists():
            logger.info("No save file found. Creating new save data.")
            self._current_save_data = self.default_save_data.copy()
            self._current_save_data["created_at"] = datetime.now().isoformat()
            return self._current_save_data

        try:
            with open(self.save_file_path, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)

            # Validate and migrate save data if needed
            validated_data = self._validate_and_migrate_save_data(loaded_data)
            self._current_save_data = validated_data
            logger.info("Save data loaded successfully.")
            return validated_data

        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading save file: {e}")
            return self._handle_corrupted_save()

    def save(self, save_data: Optional[Dict[str, Any]] = None) -> bool:
        """Save game data to file.

        Args:
            save_data: Data to save. If None, saves current data.

        Returns:
            True if save successful, False otherwise.
        """
        data_to_save = save_data or self._current_save_data
        if data_to_save is None:
            logger.error("No data to save.")
            return False

        # Update timestamp
        data_to_save["updated_at"] = datetime.now().isoformat()

        try:
            # Create backup of existing save
            if self.save_file_path.exists():
                backup_path = self.save_directory / f"{self.SAVE_FILE_NAME}.backup"
                self.save_file_path.replace(backup_path)

            # Write new save data
            with open(self.save_file_path, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)

            self._current_save_data = data_to_save
            logger.info("Game saved successfully.")
            return True

        except IOError as e:
            logger.error(f"Error saving game: {e}")
            # Restore backup if save failed
            backup_path = self.save_directory / f"{self.SAVE_FILE_NAME}.backup"
            if backup_path.exists():
                backup_path.replace(self.save_file_path)
            return False

    def _validate_and_migrate_save_data(
        self, loaded_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate loaded save data and migrate if from older version.

        Args:
            loaded_data: The loaded save data to validate.

        Returns:
            Validated and potentially migrated save data.
        """
        # Check version
        save_version = loaded_data.get("version", "0.0.0")

        # Deep merge with default data to ensure all keys exist
        validated_data = self._deep_merge_dicts(
            self.default_save_data.copy(), loaded_data
        )

        # Version-specific migrations would go here
        if save_version < self.SAVE_VERSION:
            logger.info(
                f"Migrating save data from version {save_version} to {self.SAVE_VERSION}"
            )
            # Add migration logic here as needed
            validated_data["version"] = self.SAVE_VERSION

        return validated_data

    def _deep_merge_dicts(
        self, base: Dict[str, Any], update: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deep merge two dictionaries, preserving values from update.

        Args:
            base: Base dictionary with default structure.
            update: Dictionary with values to preserve.

        Returns:
            Merged dictionary.
        """
        for key, value in base.items():
            if key in update:
                if isinstance(value, dict) and isinstance(update[key], dict):
                    base[key] = self._deep_merge_dicts(value, update[key])
                else:
                    base[key] = update[key]

        # Add any extra keys from update that aren't in base
        for key in update:
            if key not in base:
                base[key] = update[key]

        return base

    def _handle_corrupted_save(self) -> Dict[str, Any]:
        """Handle corrupted save file by backing it up and creating new save.

        Returns:
            Fresh default save data.
        """
        if self.save_file_path.exists():
            corrupted_path = self.save_directory / f"{self.SAVE_FILE_NAME}.corrupted"
            self.save_file_path.replace(corrupted_path)
            logger.warning(f"Corrupted save backed up to: {corrupted_path}")

        self._current_save_data = self.default_save_data.copy()
        self._current_save_data["created_at"] = datetime.now().isoformat()
        return self._current_save_data

    # Convenience methods for common operations

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        if self._current_save_data is None:
            self.load()
        return self._current_save_data.get("settings", {}).get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""
        if self._current_save_data is None:
            self.load()
        self._current_save_data["settings"][key] = value

    def get_high_scores(self, game: str, character: str) -> list:
        """Get high scores for a specific game and character."""
        if self._current_save_data is None:
            self.load()
        return (
            self._current_save_data.get("high_scores", {})
            .get(game, {})
            .get(character, [])
        )

    def add_high_score(self, game: str, character: str, score: Dict[str, Any]) -> None:
        """Add a high score for a specific game and character.

        Args:
            game: Game name (ski, pool, vegas)
            character: Character name (danger, rose, dad)
            score: Score data dict with at least 'score' and 'date' keys
        """
        if self._current_save_data is None:
            self.load()

        scores = self._current_save_data["high_scores"][game][character]
        scores.append(score)
        # Keep only top 10 scores
        scores.sort(key=lambda x: x.get("score", 0), reverse=True)
        self._current_save_data["high_scores"][game][character] = scores[:10]

    def unlock_minigame(self, game: str) -> None:
        """Unlock a minigame."""
        if self._current_save_data is None:
            self.load()
        if game in self._current_save_data["progress"]["minigames_unlocked"]:
            self._current_save_data["progress"]["minigames_unlocked"][game] = True

    def is_minigame_unlocked(self, game: str) -> bool:
        """Check if a minigame is unlocked."""
        if self._current_save_data is None:
            self.load()
        return self._current_save_data["progress"]["minigames_unlocked"].get(
            game, False
        )

    def set_selected_character(self, character: str) -> None:
        """Set the selected character."""
        if self._current_save_data is None:
            self.load()
        self._current_save_data["player"]["selected_character"] = character

    def get_selected_character(self) -> Optional[str]:
        """Get the selected character."""
        if self._current_save_data is None:
            self.load()
        return self._current_save_data["player"]["selected_character"]

    def get_last_save_time(self) -> Optional[datetime]:
        """Get the last save time as a datetime object."""
        if self._current_save_data is None:
            self.load()

        last_save = self._current_save_data.get("updated_at")
        if last_save:
            try:
                return datetime.fromisoformat(last_save)
            except (ValueError, TypeError):
                return None
        return None
