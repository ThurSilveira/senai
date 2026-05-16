# powerup.py — Itens coletáveis

import random
import pygame
import math
from settings import SCREEN_WIDTH, POWERUP_SPEED, POWERUP_SIZE, GREEN, BLUE, PURPLE, WHITE

class PowerUp(pygame.sprite.Sprite):
    """Itens que dão habilidades especiais ao jogador."""
    
    TYPES = {
        'life': {'color': GREEN, 'label': 'L'},
        'triple': {'color': BLUE, 'label': '3'},
        'spread': {'color': PURPLE, 'label': 'S'}
    }

    def __init__(self, x, y):
        super().__init__()
        
        self.type = random.choice(list(self.TYPES.keys()))
        self.color = self.TYPES[self.type]['color']
        self.label = self.TYPES[self.type]['label']
        
        # Desenho do item: Hexágono ou Círculo com borda e letra
        self.image = pygame.Surface((POWERUP_SIZE, POWERUP_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (POWERUP_SIZE//2, POWERUP_SIZE//2), POWERUP_SIZE//2)
        pygame.draw.circle(self.image, WHITE, (POWERUP_SIZE//2, POWERUP_SIZE//2), POWERUP_SIZE//2, 2)
        
        font = pygame.font.SysFont("Arial", 20, bold=True)
        text = font.render(self.label, True, WHITE)
        text_rect = text.get_rect(center=(POWERUP_SIZE//2, POWERUP_SIZE//2))
        self.image.blit(text, text_rect)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = POWERUP_SPEED
        self.timer = 0

    def update(self):
        # Movimento oscilante lateral suave + descida
        self.timer += 0.05
        self.rect.y += self.speed
        self.rect.x += math.sin(self.timer) * 2
        
        if self.rect.top > 600:
            self.kill()
