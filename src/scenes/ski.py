import pygame
import time
import random
from src.utils.asset_paths import get_character_sprite_path
from src.utils.attack_character import AttackCharacter
from src.scenes.slope_generator import SlopeGenerator
from src.managers.sound_manager import SoundManager
from src.config.constants import (
    SPRITE_DISPLAY_SIZE,
    COLOR_WHITE,
    COLOR_BLACK,
    COLOR_GREEN,
    COLOR_RED,
    SCENE_HUB_WORLD,
)


class SkiPlayer:
    def __init__(self, x: int, y: int, character_name: str):
        self.x = x
        self.y = y
        self.character_name = character_name

        # Movement
        self.speed = 5
        self.diagonal_speed = 3.5  # Slower when moving diagonally

        # Create animated character
        sprite_path = get_character_sprite_path(character_name.lower())
        self.sprite = AttackCharacter(
            character_name, sprite_path, (SPRITE_DISPLAY_SIZE, SPRITE_DISPLAY_SIZE)
        )

        # Collision rect - smaller than sprite for more forgiving collisions
        self.rect = pygame.Rect(x - 24, y - 24, 48, 48)
        
        # Crash state
        self.is_crashing = False
        self.crash_time = 0
        self.invincible = False
        self.invincible_time = 0

    def handle_input(self, keys, screen_width):
        # Only allow movement if not crashing
        if self.is_crashing:
            return
            
        # Horizontal movement
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed

        # Update position
        self.x += dx

        # Keep player on screen
        self.x = max(32, min(self.x, screen_width - 32))

        # Update rect
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def update(self, dt: float):
        # Update crash state
        if self.is_crashing:
            self.crash_time -= dt
            if self.crash_time <= 0:
                self.is_crashing = False
                self.invincible = True
                self.invincible_time = 2.0  # 2 seconds of invincibility
                
        # Update invincibility
        if self.invincible:
            self.invincible_time -= dt
            if self.invincible_time <= 0:
                self.invincible = False
        
        # Update animation
        self.sprite.update()
    
    def crash(self):
        """Trigger crash state."""
        if not self.invincible and not self.is_crashing:
            self.is_crashing = True
            self.crash_time = 0.5  # Crash animation duration
            return True
        return False

    def draw(self, screen):
        sprite = self.sprite.get_current_sprite()
        
        # Flash during invincibility
        if self.invincible and int(self.invincible_time * 10) % 2 == 0:
            # Make sprite semi-transparent
            sprite = sprite.copy()
            sprite.set_alpha(128)
            
        # Tint red during crash
        if self.is_crashing:
            sprite = sprite.copy()
            sprite.fill((255, 100, 100), special_flags=pygame.BLEND_MULT)
        
        sprite_rect = sprite.get_rect(center=(self.x, self.y))
        screen.blit(sprite, sprite_rect)


class SkiGame:
    """Ski minigame scene with 60-second timed runs."""

    # Game states
    STATE_READY = "ready"
    STATE_PLAYING = "playing"
    STATE_GAME_OVER = "game_over"

    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.screen_width = scene_manager.screen_width
        self.screen_height = scene_manager.screen_height

        # Game state
        self.state = self.STATE_READY
        self.game_duration = 60.0  # 60 seconds
        self.time_remaining = self.game_duration
        self.start_time = None

        # Initialize player
        character_name = scene_manager.game_data.get("selected_character") or "Danger"
        self.player = SkiPlayer(
            self.screen_width // 2, self.screen_height - 200, character_name
        )
        
        # Lives system
        self.lives = 3
        self.max_lives = 3

        # Visual elements
        self.scroll_speed = 200  # Base scrolling speed
        self.scroll_offset = 0

        # UI fonts
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.huge_font = pygame.font.Font(None, 96)

        # Create slope generator
        self.slope_generator = SlopeGenerator(self.screen_width, self.screen_height)
        
        # Sound manager
        self.sound_manager = SoundManager()
        
        # Create simple snow texture for background
        self.create_snow_texture()

    def create_snow_texture(self):
        """Create a simple snow texture for the background."""
        self.snow_surface = pygame.Surface((self.screen_width, self.screen_height * 2))
        self.snow_surface.fill(COLOR_WHITE)

        # Add some snow texture details
        for _ in range(200):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height * 2)
            radius = random.randint(1, 3)
            color = (240, 240, 255) if random.random() > 0.5 else (230, 230, 250)
            pygame.draw.circle(self.snow_surface, color, (x, y), radius)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == self.STATE_READY:
                if event.key == pygame.K_SPACE:
                    self.start_game()
                elif event.key == pygame.K_ESCAPE:
                    return SCENE_HUB_WORLD

            elif self.state == self.STATE_PLAYING:
                if event.key == pygame.K_ESCAPE:
                    # Return to hub (could add pause later)
                    return SCENE_HUB_WORLD

            elif self.state == self.STATE_GAME_OVER:
                if event.key == pygame.K_SPACE:
                    # Restart
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    return SCENE_HUB_WORLD

        return None

    def start_game(self):
        """Start the game timer and transition to playing state."""
        self.state = self.STATE_PLAYING
        self.start_time = time.time()
        self.time_remaining = self.game_duration

    def reset_game(self):
        """Reset the game to ready state."""
        self.state = self.STATE_READY
        self.time_remaining = self.game_duration
        self.scroll_offset = 0
        self.player.x = self.screen_width // 2
        self.player.is_crashing = False
        self.player.invincible = False
        self.player.invincible_time = 0
        self.lives = self.max_lives
        self.slope_generator.reset()

    def update(self, dt: float):
        if self.state == self.STATE_PLAYING:
            # Update timer
            elapsed = 0
            if self.start_time:
                elapsed = time.time() - self.start_time
                self.time_remaining = max(0, self.game_duration - elapsed)

                # Check for game over
                if self.time_remaining <= 0:
                    self.state = self.STATE_GAME_OVER

            # Handle player input
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys, self.screen_width)

            # Update player
            self.player.update(dt)
            
            # Check for collisions
            self.check_collisions()

            # Update scrolling
            self.scroll_offset += self.scroll_speed * dt
            if self.scroll_offset >= self.screen_height:
                self.scroll_offset -= self.screen_height
            
            # Update slope generator
            self.slope_generator.update(self.scroll_speed, dt, elapsed)
    
    def check_collisions(self):
        """Check for collisions between player and obstacles."""
        obstacles = self.slope_generator.get_obstacles()
        
        for obstacle in obstacles:
            if self.player.rect.colliderect(obstacle.rect):
                # Try to crash the player
                if self.player.crash():
                    self.lives -= 1
                    
                    # Play crash sound (if available)
                    try:
                        self.sound_manager.play_sfx("assets/sounds/crash.ogg")
                    except:
                        pass  # Sound file not available yet
                    
                    # Check for game over
                    if self.lives <= 0:
                        self.state = self.STATE_GAME_OVER
                    break

    def draw(self, screen):
        # Clear screen with sky color
        screen.fill((135, 206, 235))  # Sky blue

        # Draw scrolling slope
        self.draw_slope(screen)

        # Draw player
        self.player.draw(screen)

        # Draw UI based on state
        if self.state == self.STATE_READY:
            self.draw_ready_screen(screen)
        elif self.state == self.STATE_PLAYING:
            self.draw_game_ui(screen)
        elif self.state == self.STATE_GAME_OVER:
            self.draw_game_over_screen(screen)

    def draw_slope(self, screen):
        """Draw the scrolling slope effect."""
        # Draw snow texture background
        y_offset = int(self.scroll_offset)
        screen.blit(self.snow_surface, (0, y_offset - self.screen_height))
        screen.blit(self.snow_surface, (0, y_offset - self.screen_height * 2))
        
        # Draw obstacles
        self.slope_generator.draw(screen)

    def draw_ready_screen(self, screen):
        """Draw the ready state UI."""
        # Title
        title_text = self.huge_font.render("SKI GAME", True, COLOR_BLACK)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 200))
        screen.blit(title_text, title_rect)

        # Instructions
        instructions = [
            "Race down the mountain for 60 seconds!",
            "",
            "Arrow Keys or A/D to move",
            "Press SPACE to start",
            "Press ESC to return to hub",
        ]

        y = 350
        for instruction in instructions:
            text = self.font.render(instruction, True, COLOR_BLACK)
            text_rect = text.get_rect(center=(self.screen_width // 2, y))
            screen.blit(text, text_rect)
            y += 40

    def draw_game_ui(self, screen):
        """Draw the playing state UI."""
        # Timer
        timer_text = f"Time: {int(self.time_remaining)}"
        timer_surface = self.big_font.render(timer_text, True, COLOR_BLACK)
        timer_rect = timer_surface.get_rect(center=(self.screen_width // 2, 50))

        # Timer background
        bg_rect = timer_rect.inflate(20, 10)
        pygame.draw.rect(screen, COLOR_WHITE, bg_rect)
        pygame.draw.rect(screen, COLOR_BLACK, bg_rect, 3)

        screen.blit(timer_surface, timer_rect)
        
        # Lives display
        self.draw_lives(screen)

        # Controls reminder
        controls = self.font.render("ESC: Return to Hub", True, COLOR_BLACK)
        screen.blit(controls, (10, 10))
    
    def draw_lives(self, screen):
        """Draw the lives indicator."""
        heart_size = 40
        heart_spacing = 10
        start_x = self.screen_width - (self.max_lives * (heart_size + heart_spacing))
        y = 20
        
        for i in range(self.max_lives):
            x = start_x + i * (heart_size + heart_spacing)
            
            # Draw heart shape
            if i < self.lives:
                color = COLOR_RED
                fill = True
            else:
                color = COLOR_BLACK
                fill = False
                
            # Simple heart using circles and polygon
            if fill:
                # Filled heart
                pygame.draw.circle(screen, color, (x + heart_size // 4, y + heart_size // 4), heart_size // 4)
                pygame.draw.circle(screen, color, (x + 3 * heart_size // 4, y + heart_size // 4), heart_size // 4)
                pygame.draw.polygon(screen, color, [
                    (x, y + heart_size // 3),
                    (x + heart_size // 2, y + heart_size),
                    (x + heart_size, y + heart_size // 3)
                ])
            else:
                # Outline heart
                pygame.draw.circle(screen, color, (x + heart_size // 4, y + heart_size // 4), heart_size // 4, 2)
                pygame.draw.circle(screen, color, (x + 3 * heart_size // 4, y + heart_size // 4), heart_size // 4, 2)
                pygame.draw.lines(screen, color, False, [
                    (x, y + heart_size // 3),
                    (x + heart_size // 2, y + heart_size),
                    (x + heart_size, y + heart_size // 3)
                ], 2)

    def draw_game_over_screen(self, screen):
        """Draw the game over state UI."""
        # Overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill(COLOR_BLACK)
        screen.blit(overlay, (0, 0))

        # Game over text based on reason
        if self.lives <= 0:
            game_over_text = self.huge_font.render("CRASHED OUT!", True, COLOR_RED)
            score_text = self.big_font.render("Try to avoid the obstacles!", True, COLOR_WHITE)
        else:
            game_over_text = self.huge_font.render("TIME'S UP!", True, COLOR_WHITE)
            score_text = self.big_font.render("Great run!", True, COLOR_GREEN)
            
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, 250))
        screen.blit(game_over_text, game_over_rect)

        # Score/message
        score_rect = score_text.get_rect(center=(self.screen_width // 2, 350))
        screen.blit(score_text, score_rect)

        # Options
        options = ["Press SPACE to play again", "Press ESC to return to hub"]

        y = 450
        for option in options:
            text = self.font.render(option, True, COLOR_WHITE)
            text_rect = text.get_rect(center=(self.screen_width // 2, y))
            screen.blit(text, text_rect)
            y += 40

    def on_enter(self, previous_scene, data):
        """Called when entering this scene."""
        # Reset to ready state when entering
        self.reset_game()

    def on_exit(self):
        """Called when leaving this scene."""
        return {}
