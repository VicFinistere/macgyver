import pygame
import os
from config import ASSETS_DIR, WIDTH, HEIGHT
from random import randrange

class Item(pygame.sprite.Sprite):
    """
    This class is handling properties and methods for all kind of item
    :returns  any player without specialities
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/item.png"))
        self.image = pygame.transform.scale(self.image, (32, 32))
        item_rand_x, item_rand_y = randrange(32, WIDTH - 32), randrange(32, HEIGHT - 32)
        self.rect = pygame.Rect(item_rand_x, item_rand_y, 32, 32)

    def get_rect(self):
        return self.rect
