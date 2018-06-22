import pygame
import os
from config import ASSETS_DIR, SCREEN

class Enemy(pygame.sprite.Sprite):
    """
        This class is handling properties and methods for enemies
        :returns  any enemy
        """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.area = SCREEN.get_rect()
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/enemy.png"))

