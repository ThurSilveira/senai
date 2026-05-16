# asteroid.py — Classe dos asteroides

import math
import random
import pygame
from settings import (
    SCREEN_WIDTH,
    ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS,
    RED, DEEP_RED, DARK_GRAY, GRAY, WHITE,
    get_asteroid_speed
)


class Asteroid(pygame.sprite.Sprite):
    """Asteroide com visual detalhado, rotação e brilho."""

    def __init__(self, score=0):
        super().__init__()

        # Raio aleatório para variar o tamanho
        self.radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
        size = self.radius * 2
        pad = 4  # Padding para o glow
        total = size + pad * 2

        # Cria superfície base do asteroide
        self.base_image = pygame.Surface((total, total), pygame.SRCALPHA)
        center = total // 2

        # Desenha forma irregular (polígono em vez de círculo perfeito)
        num_vertices = random.randint(7, 12)
        vertices = []
        for i in range(num_vertices):
            angle = (2 * math.pi * i) / num_vertices
            # Varia o raio para criar forma irregular
            r = self.radius * random.uniform(0.7, 1.0)
            vx = center + r * math.cos(angle)
            vy = center + r * math.sin(angle)
            vertices.append((vx, vy))

        # Preenchimento com gradiente simulado (camadas)
        # Camada externa — mais escura
        pygame.draw.polygon(self.base_image, DARK_GRAY, vertices)
        # Camada interna — mais clara (encolhida)
        inner_vertices = []
        for vx, vy in vertices:
            ix = center + (vx - center) * 0.6
            iy = center + (vy - center) * 0.6
            inner_vertices.append((ix, iy))
        pygame.draw.polygon(self.base_image, GRAY, inner_vertices)

        # Crateras aleatórias
        num_craters = random.randint(1, 3)
        for _ in range(num_craters):
            cx = center + random.randint(-self.radius // 2, self.radius // 2)
            cy = center + random.randint(-self.radius // 2, self.radius // 2)
            cr = random.randint(2, max(3, self.radius // 4))
            pygame.draw.circle(self.base_image, (50, 50, 55), (cx, cy), cr)
            pygame.draw.circle(self.base_image, (70, 70, 75), (cx, cy), cr, 1)

        # Borda vermelha brilhante (dano/calor)
        pygame.draw.polygon(self.base_image, RED, vertices, 2)

        # Ponto de brilho (highlight)
        highlight_x = center - self.radius // 3
        highlight_y = center - self.radius // 3
        pygame.draw.circle(
            self.base_image, (200, 200, 210, 120),
            (highlight_x, highlight_y),
            max(2, self.radius // 5)
        )

        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - total)
        self.rect.bottom = 0

        # Velocidade baseada no score (dificuldade progressiva)
        self.speed = get_asteroid_speed(score)

        # Rotação
        self.angle = 0
        self.rotation_speed = random.uniform(-2, 2)
        self.original_center = self.rect.center

        # Pulsação
        self.pulse_timer = random.uniform(0, math.pi * 2)

    def update(self):
        """Move o asteroide para baixo com rotação."""
        self.rect.y += self.speed

        # Rotação contínua
        self.angle += self.rotation_speed
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=old_center)

        # Timer de pulsação
        self.pulse_timer += 0.08

    def draw_glow(self, screen):
        """Desenha um glow vermelho pulsante ao redor do asteroide."""
        pulse = math.sin(self.pulse_timer)
        glow_alpha = int(25 + 15 * pulse)
        glow_size = self.radius * 2 + 16
        glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        pygame.draw.circle(
            glow_surf,
            (255, 60, 60, glow_alpha),
            (glow_size // 2, glow_size // 2),
            glow_size // 2
        )
        screen.blit(
            glow_surf,
            (self.rect.centerx - glow_size // 2,
             self.rect.centery - glow_size // 2)
        )
