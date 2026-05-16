# bullet.py — Classe dos projéteis

import math
import pygame
from settings import BULLET_SPEED, BULLET_WIDTH, BULLET_HEIGHT, YELLOW, WHITE


class Bullet(pygame.sprite.Sprite):
    """Projétil disparado pela nave do jogador com suporte a ângulos."""

    def __init__(self, x, y, angle=0):
        super().__init__()

        # Superfície maior para o glow
        glow_pad = 6
        total_w = BULLET_WIDTH + glow_pad * 2
        total_h = BULLET_HEIGHT + glow_pad * 2

        self.original_image = pygame.Surface((total_w, total_h), pygame.SRCALPHA)

        # Glow externo
        glow_rect = pygame.Rect(0, 0, total_w, total_h)
        glow_surf = pygame.Surface((total_w, total_h), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surf, (255, 255, 100, 60), glow_rect)
        self.original_image.blit(glow_surf, (0, 0))

        # Núcleo
        core_rect = pygame.Rect(glow_pad, glow_pad, BULLET_WIDTH, BULLET_HEIGHT)
        pygame.draw.rect(self.original_image, YELLOW, core_rect, border_radius=2)
        center_rect = pygame.Rect(glow_pad + 1, glow_pad, BULLET_WIDTH - 2, BULLET_HEIGHT)
        pygame.draw.rect(self.original_image, WHITE, center_rect, border_radius=1)

        # Rotação baseada no ângulo de disparo
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # Vetor de velocidade
        rad = math.radians(self.angle - 90)
        self.vx = math.cos(rad) * abs(BULLET_SPEED)
        self.vy = math.sin(rad) * abs(BULLET_SPEED)
        
        self.trail_positions = []

    def update(self):
        self.trail_positions.append((self.rect.centerx, self.rect.centery))
        if len(self.trail_positions) > 5:
            self.trail_positions.pop(0)

        # Movimento vetorial
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.bottom < 0 or self.rect.top > 600 or self.rect.left < 0 or self.rect.right > 800:
            self.kill()

    def draw_trail(self, screen):
        for i, (tx, ty) in enumerate(self.trail_positions):
            alpha = int(40 * (i + 1) / len(self.trail_positions))
            size = max(1, int(3 * (i + 1) / len(self.trail_positions)))
            trail_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, (255, 255, 100, alpha), (size, size), size)
            screen.blit(trail_surf, (tx - size, ty - size))
