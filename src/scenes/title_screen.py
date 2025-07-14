import pygame
from typing import Optional
from src.utils.sprite_loader import load_image
from src.utils.attack_character import AttackCharacter
from src.utils.asset_paths import get_living_room_bg, get_danger_sprite, get_rose_sprite

class CharacterButton:
    def __init__(self, x: int, y: int, character_name: str, sprite_path: str):
        self.x = x
        self.y = y
        self.character_name = character_name
        self.width = 200
        self.height = 300
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.selected = False
        self.hovered = False
        
        # Create attack-only animated character
        self.animated_character = AttackCharacter(character_name, sprite_path, (128, 128))
        
        # Font for character name
        self.font = pygame.font.Font(None, 36)
        self.name_surface = self.font.render(character_name, True, (255, 255, 255))
        
        # Font for animation info
        self.info_font = pygame.font.Font(None, 24)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.animated_character.update()
    
    def draw(self, screen):
        # Draw button background
        color = (100, 150, 255) if self.selected else (80, 120, 200) if self.hovered else (60, 100, 180)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)
        
        # Draw animated character sprite
        sprite = self.animated_character.get_current_sprite()
        sprite_rect = sprite.get_rect(center=(self.rect.centerx, self.rect.centery - 40))
        screen.blit(sprite, sprite_rect)
        
        # Draw character name
        name_rect = self.name_surface.get_rect(center=(self.rect.centerx, self.rect.bottom - 50))
        screen.blit(self.name_surface, name_rect)
        
        # Draw animation info
        animation_info = self.animated_character.get_animation_info()
        info_surface = self.info_font.render(animation_info, True, (200, 200, 200))
        info_rect = info_surface.get_rect(center=(self.rect.centerx, self.rect.bottom - 25))
        screen.blit(info_surface, info_rect)


class TitleScreen:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.selected_character = None
        
        # Load background
        self.background = load_image(get_living_room_bg(), (screen_width, screen_height))
        
        # Create character selection buttons
        button_y = screen_height // 2 - 150
        danger_x = screen_width // 2 - 250
        rose_x = screen_width // 2 + 50
        
        self.danger_button = CharacterButton(danger_x, button_y, "Danger", get_danger_sprite())
        self.rose_button = CharacterButton(rose_x, button_y, "Rose", get_rose_sprite())
        
        # Title text
        self.title_font = pygame.font.Font(None, 72)
        self.title_surface = self.title_font.render("Danger Rose", True, (255, 255, 255))
        
        # Instructions
        self.instruction_font = pygame.font.Font(None, 48)
        self.instruction_surface = self.instruction_font.render("Choose Your Character", True, (255, 255, 255))
        
        # Start button (appears after character selection)
        self.start_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height - 150, 200, 60)
        self.start_font = pygame.font.Font(None, 48)
        self.start_surface = self.start_font.render("Start Game", True, (255, 255, 255))
        
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.danger_button.handle_event(event):
            self.selected_character = "Danger"
            self.danger_button.selected = True
            self.rose_button.selected = False
            return None
            
        if self.rose_button.handle_event(event):
            self.selected_character = "Rose"
            self.rose_button.selected = True
            self.danger_button.selected = False
            return None
        
        # Start button (only clickable if character selected)
        if event.type == pygame.MOUSEBUTTONDOWN and self.selected_character:
            if self.start_button_rect.collidepoint(event.pos):
                return "start_game"
        
        return None
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.danger_button.update(mouse_pos)
        self.rose_button.update(mouse_pos)
    
    def draw(self, screen):
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Draw title
        title_rect = self.title_surface.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(self.title_surface, title_rect)
        
        # Draw instructions
        instruction_rect = self.instruction_surface.get_rect(center=(self.screen_width // 2, 200))
        screen.blit(self.instruction_surface, instruction_rect)
        
        # Draw character buttons
        self.danger_button.draw(screen)
        self.rose_button.draw(screen)
        
        # Draw start button if character selected
        if self.selected_character:
            mouse_pos = pygame.mouse.get_pos()
            button_hovered = self.start_button_rect.collidepoint(mouse_pos)
            button_color = (100, 200, 100) if button_hovered else (80, 160, 80)
            
            pygame.draw.rect(screen, button_color, self.start_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), self.start_button_rect, 3)
            
            start_text_rect = self.start_surface.get_rect(center=self.start_button_rect.center)
            screen.blit(self.start_surface, start_text_rect)
            
            # Show selected character name
            selected_font = pygame.font.Font(None, 36)
            selected_text = selected_font.render(f"Selected: {self.selected_character}", True, (255, 255, 255))
            selected_rect = selected_text.get_rect(center=(self.screen_width // 2, self.screen_height - 200))
            screen.blit(selected_text, selected_rect)