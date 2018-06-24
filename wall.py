import pygame
import os
from config import ASSETS_DIR

class Wall(pygame.sprite.Sprite):
    """
        This class is handling properties and methods for enemies
        :returns  any enemy
        """

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/wall.png"))
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)