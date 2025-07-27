import pygame
import time
from src.utils.asset_paths import get_character_sprite_path
from src.utils.attack_character import AttackCharacter
from src.config.constants import (
    SPRITE_DISPLAY_SIZE,
    COLOR_WHITE,
    COLOR_BLACK,
    COLOR_GREEN,
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
            character_name, 
            sprite_path, 
            (SPRITE_DISPLAY_SIZE, SPRITE_DISPLAY_SIZE)
        )
        
        # Collision rect
        self.rect = pygame.Rect(x, y, 64, 64)
        
    def handle_input(self, keys, screen_width):
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
        # Update animation
        self.sprite.update()
        
    def draw(self, screen):
        sprite = self.sprite.get_current_sprite()
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
            self.screen_width // 2, 
            self.screen_height - 200,
            character_name
        )
        
        # Visual elements
        self.scroll_speed = 200  # Base scrolling speed
        self.scroll_offset = 0
        
        # UI fonts
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.huge_font = pygame.font.Font(None, 96)
        
        # Create slope pattern for visual effect
        self.create_slope_visual()
        
    def create_slope_visual(self):
        """Create a simple visual pattern for the slope."""
        self.slope_surface = pygame.Surface((self.screen_width, self.screen_height * 2))
        self.slope_surface.fill(COLOR_WHITE)
        
        # Add some simple slope markers
        for y in range(0, self.screen_height * 2, 100):
            pygame.draw.line(
                self.slope_surface,
                (200, 200, 255),
                (self.screen_width // 2 - 50, y),
                (self.screen_width // 2 + 50, y),
                3
            )
            
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
        
    def update(self, dt: float):
        if self.state == self.STATE_PLAYING:
            # Update timer
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
            
            # Update scrolling
            self.scroll_offset += self.scroll_speed * dt
            if self.scroll_offset >= self.screen_height:
                self.scroll_offset -= self.screen_height
                
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
        # Draw two copies for seamless scrolling
        y_offset = int(self.scroll_offset)
        screen.blit(self.slope_surface, (0, y_offset - self.screen_height))
        screen.blit(self.slope_surface, (0, y_offset - self.screen_height * 2))
        
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
            "Press ESC to return to hub"
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
        
        # Controls reminder
        controls = self.font.render("ESC: Return to Hub", True, COLOR_BLACK)
        screen.blit(controls, (10, 10))
        
    def draw_game_over_screen(self, screen):
        """Draw the game over state UI."""
        # Overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill(COLOR_BLACK)
        screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.huge_font.render("TIME'S UP!", True, COLOR_WHITE)
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, 250))
        screen.blit(game_over_text, game_over_rect)
        
        # Score placeholder
        score_text = self.big_font.render("Great run!", True, COLOR_GREEN)
        score_rect = score_text.get_rect(center=(self.screen_width // 2, 350))
        screen.blit(score_text, score_rect)
        
        # Options
        options = [
            "Press SPACE to play again",
            "Press ESC to return to hub"
        ]
        
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