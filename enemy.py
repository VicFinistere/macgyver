"""
This class is handling properties and methods for enemies
"""
import os
import pygame
from config import ASSETS_DIR


class Enemy(pygame.sprite.Sprite):
    """
        Class Enemy
        :returns  any enemy
        """

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/enemy.png"))
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = pygame.Rect(pos[0] * 32, pos[1] * 32, 32, 32)
