"""Game constants for Danger Rose.

This module contains all game constants used throughout the application.
Constants are organized by category for easy access and maintenance.
"""

# Screen Configuration
# SCREEN_WIDTH = 1920
# SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Window Settings
WINDOW_TITLE = "Danger Rose"
FULLSCREEN_DEFAULT = False

# Sprite Dimensions
SPRITE_SHEET_SIZE = 1024  # Full sprite sheet is 1024x1024
SPRITE_FRAME_WIDTH = 256  # Individual frame width
SPRITE_FRAME_HEIGHT = 341  # Individual frame height
SPRITE_DISPLAY_SIZE = 128  # Display size for sprites in-game
SPRITE_GRID_COLS = 4  # Number of columns in sprite sheet
SPRITE_GRID_ROWS = 3  # Number of rows in sprite sheet

# Animation Timings (in milliseconds)
ANIMATION_DEFAULT_DURATION = 100  # Default frame duration
ANIMATION_IDLE_DURATION = 200  # Idle animation frame duration
ANIMATION_WALK_DURATION = 100  # Walk animation frame duration
ANIMATION_ATTACK_DURATION = 50  # Attack animation frame duration
ANIMATION_HURT_DURATION = 150  # Hurt animation frame duration
ANIMATION_VICTORY_DURATION = 120  # Victory animation frame duration

# Animation Frame Counts
ANIMATION_IDLE_FRAMES = 4
ANIMATION_WALK_FRAMES = 8
ANIMATION_JUMP_FRAMES = 3
ANIMATION_ATTACK_FRAMES = 6
ANIMATION_HURT_FRAMES = 2
ANIMATION_VICTORY_FRAMES = 8

# Game Physics
GRAVITY = 800.0  # Pixels per second squared
JUMP_VELOCITY = -500.0  # Initial jump velocity
PLAYER_SPEED = 300.0  # Player movement speed
PLAYER_ACCELERATION = 1200.0  # Player acceleration
FRICTION = 0.85  # Movement friction coefficient

# UI Constants
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
BUTTON_PADDING = 20
MENU_TRANSITION_SPEED = 5.0  # Seconds for menu transitions

# Colors (RGB)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (60, 100, 180)
COLOR_GREEN = (60, 180, 100)
COLOR_RED = (180, 60, 60)
COLOR_YELLOW = (220, 200, 60)
COLOR_PURPLE = (180, 60, 180)

# Scene Names
SCENE_TITLE = "title"
SCENE_CHARACTER_SELECT = "character_select"
SCENE_HUB_WORLD = "hub_world"
SCENE_SKI_GAME = "ski_game"
SCENE_POOL_GAME = "pool_game"
SCENE_VEGAS_GAME = "vegas_game"
SCENE_SETTINGS = "settings"
SCENE_PAUSE = "pause"

# Audio Settings
DEFAULT_MASTER_VOLUME = 0.7
DEFAULT_MUSIC_VOLUME = 0.5
DEFAULT_SFX_VOLUME = 0.8
AUDIO_FADE_TIME = 500  # Milliseconds for audio fade

# File Paths
CONFIG_FILE = "game_settings.json"
SAVE_FILE = "game_save.json"
HIGH_SCORES_FILE = "high_scores.json"

# Debug Settings
DEBUG_SHOW_FPS = False
DEBUG_SHOW_HITBOXES = False
DEBUG_SHOW_GRID = False
