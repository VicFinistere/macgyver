"""
This class is made to construct walls for our maze
"""
import pygame
import os
from config import ASSETS_DIR


class Wall(pygame.sprite.Sprite):
    """
    Wall Class
    """

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/wall.png"))
        # self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = pygame.Rect(pos[0] * 32, pos[1] * 32, 15, 15)
