import pygame
from src.utils.sprite_loader import load_image
from src.utils.asset_paths import get_vegas_bg, get_character_sprite_path
from src.utils.attack_character import AttackCharacter
from src.config.constants import (
    SPRITE_DISPLAY_SIZE,
    COLOR_WHITE,
    COLOR_BLACK,
    SCENE_HUB_WORLD,
)


class Camera:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        
    def apply(self, rect):
        return rect.move(-self.x, -self.y)
    
    def update(self, target_rect, level_width):
        # Center camera on target
        self.x = target_rect.centerx - self.width // 2
        
        # Keep camera within level bounds
        self.x = max(0, min(self.x, level_width - self.width))
        
    def apply_to_pos(self, x, y):
        return x - self.x, y - self.y


class Player:
    def __init__(self, x: int, y: int, character_name: str):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.on_ground = True
        self.character_name = character_name
        
        # Player physics constants
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.max_fall_speed = 12
        
        # Create animated character
        sprite_path = get_character_sprite_path(character_name.lower())
        self.sprite = AttackCharacter(
            character_name, 
            sprite_path, 
            (SPRITE_DISPLAY_SIZE, SPRITE_DISPLAY_SIZE)
        )
        
        # Collision rect (smaller than sprite for better feel)
        self.rect = pygame.Rect(x, y, 64, 100)
        
    def handle_input(self, keys):
        # Horizontal movement
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.speed
            
        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False
            
    def update(self, dt: float, ground_y: int):
        # Apply gravity
        if not self.on_ground:
            self.vy += self.gravity
            self.vy = min(self.vy, self.max_fall_speed)
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Ground collision (simple for now)
        if self.y + self.rect.height >= ground_y:
            self.y = ground_y - self.rect.height
            self.vy = 0
            self.on_ground = True
            
        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Update animation
        self.sprite.update()
        
    def draw(self, screen, camera):
        sprite = self.sprite.get_current_sprite()
        screen_x, screen_y = camera.apply_to_pos(self.x, self.y)
        
        # Center sprite on player rect
        sprite_rect = sprite.get_rect(center=(screen_x + self.rect.width // 2, screen_y + self.rect.height // 2))
        screen.blit(sprite, sprite_rect)


class VegasGame:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.screen_width = scene_manager.screen_width
        self.screen_height = scene_manager.screen_height
        
        # Level dimensions
        self.level_width = 3000  # Extended level width for side-scrolling
        self.ground_y = self.screen_height - 100
        
        # Initialize camera
        self.camera = Camera(self.screen_width, self.screen_height)
        
        # Initialize player
        character_name = scene_manager.game_data.get("selected_character") or "Danger"
        self.player = Player(100, self.ground_y - 100, character_name)
        
        # Background layers for parallax
        self.init_backgrounds()
        
        # UI elements
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Game state
        self.reached_boss = False
        self.paused = False
        
    def init_backgrounds(self):
        # Try to load Vegas background, use placeholder if not found
        bg_image = load_image(get_vegas_bg(), (self.screen_width, self.screen_height))
        
        # Check if it's a placeholder (magenta color)
        if bg_image.get_at((0, 0))[:3] == (255, 0, 255):
            # Create custom backgrounds
            self.bg_far = pygame.Surface((self.screen_width, self.screen_height))
            self.bg_far.fill((20, 10, 40))  # Dark purple night sky
            
            # Add some "stars" to the far background
            import random
            for _ in range(100):
                x = random.randint(0, self.screen_width)
                y = random.randint(0, self.screen_height)
                pygame.draw.circle(self.bg_far, (255, 255, 255), (x, y), 1)
            
            self.bg_near = pygame.Surface((self.screen_width, self.screen_height))
            self.bg_near.fill((40, 20, 60))  # Lighter purple for buildings
            
            # Add simple building silhouettes
            building_heights = [200, 300, 250, 280, 320, 240]
            x = 0
            for height in building_heights:
                width = 150
                pygame.draw.rect(self.bg_near, (30, 15, 50), 
                               (x, self.screen_height - height, width, height))
                x += width + 20
        else:
            self.bg_far = bg_image
            self.bg_near = bg_image.copy()
            
        # Ground/street layer
        self.ground_surface = pygame.Surface((self.level_width, 100))
        self.ground_surface.fill((50, 50, 50))  # Dark gray street
        
        # Add some street lines
        for x in range(0, self.level_width, 200):
            pygame.draw.rect(self.ground_surface, (200, 200, 0), (x, 45, 100, 10))
            
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                
            # Return to hub on Q
            if event.key == pygame.K_q:
                return SCENE_HUB_WORLD
                
        return None
        
    def update(self, dt: float):
        if self.paused:
            return
            
        # Handle input
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        # Update player
        self.player.update(dt, self.ground_y)
        
        # Update camera to follow player
        self.camera.update(self.player.rect, self.level_width)
        
        # Check if reached boss arena
        if self.player.x >= self.level_width - 300:
            self.reached_boss = True
            
    def draw(self, screen):
        # Clear screen
        screen.fill((10, 5, 20))  # Very dark purple
        
        # Draw parallax backgrounds
        # Far background (moves slower)
        far_offset = -self.camera.x * 0.3
        screen.blit(self.bg_far, (far_offset % self.screen_width, 0))
        screen.blit(self.bg_far, ((far_offset % self.screen_width) - self.screen_width, 0))
        
        # Near background (moves medium speed)
        near_offset = -self.camera.x * 0.6
        screen.blit(self.bg_near, (near_offset % self.screen_width, 0))
        screen.blit(self.bg_near, ((near_offset % self.screen_width) - self.screen_width, 0))
        
        # Draw ground
        ground_rect = self.ground_surface.get_rect(topleft=(0, self.ground_y))
        screen.blit(self.ground_surface, self.camera.apply(ground_rect))
        
        # Draw player
        self.player.draw(screen, self.camera)
        
        # Draw UI
        self.draw_ui(screen)
        
        # Draw pause overlay
        if self.paused:
            self.draw_pause_overlay(screen)
            
        # Draw boss arena reached message
        if self.reached_boss:
            self.draw_boss_message(screen)
            
    def draw_ui(self, screen):
        # Instructions
        instructions = [
            "Arrow Keys/WASD: Move",
            "Space/Up/W: Jump", 
            "ESC: Pause",
            "Q: Return to Hub"
        ]
        
        y = 10
        for instruction in instructions:
            text = self.font.render(instruction, True, COLOR_WHITE)
            screen.blit(text, (10, y))
            y += 30
            
        # Progress indicator
        progress = min(self.player.x / self.level_width, 1.0)
        progress_text = self.font.render(f"Progress: {int(progress * 100)}%", True, COLOR_WHITE)
        screen.blit(progress_text, (self.screen_width - 200, 10))
        
    def draw_pause_overlay(self, screen):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(COLOR_BLACK)
        screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.big_font.render("PAUSED", True, COLOR_WHITE)
        pause_rect = pause_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(pause_text, pause_rect)
        
    def draw_boss_message(self, screen):
        boss_text = self.big_font.render("Boss Arena Reached!", True, (255, 100, 100))
        boss_rect = boss_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(boss_text, boss_rect)
        
        sub_text = self.font.render("Boss fight coming in Issue #31!", True, COLOR_WHITE)
        sub_rect = sub_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        screen.blit(sub_text, sub_rect)